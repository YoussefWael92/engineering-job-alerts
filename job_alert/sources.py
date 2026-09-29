import json
import re
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .models import Job

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; EngineeringJobAlertBot/1.0; "
        "+https://github.com/)"
    )
}


def get_json(url, params=None):
    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def greenhouse(company):
    board = company["board"]
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
    data = get_json(url, params={"content": "true"})
    jobs = []
    for j in data.get("jobs", []):
        jobs.append(Job(
            id=f"greenhouse:{board}:{j.get('id')}",
            company=company["name"],
            title=j.get("title", ""),
            location=(j.get("location") or {}).get("name", ""),
            url=j.get("absolute_url", ""),
            description=j.get("content", "") or "",
            posted_at=j.get("updated_at"),
            source="greenhouse",
        ))
    return jobs


def smartrecruiters(company):
    identifier = company["identifier"]
    jobs = []
    offset = 0
    limit = 100

    while True:
        url = f"https://api.smartrecruiters.com/v1/companies/{identifier}/postings"
        data = get_json(url, params={"limit": limit, "offset": offset})
        content = data.get("content", [])

        for j in content:
            loc = j.get("location") or {}
            location = ", ".join(
                x for x in [
                    loc.get("city"),
                    loc.get("region"),
                    loc.get("country"),
                ] if x
            )

            # Fetch full posting details for better filtering.
            description = ""
            try:
                detail_url = (
                    f"https://api.smartrecruiters.com/v1/companies/"
                    f"{identifier}/postings/{j.get('id')}"
                )
                detail = get_json(detail_url)
                description = (
                    detail.get("jobAd", {}).get("sections", {}).get("jobDescription", "")
                    or detail.get("jobAd", {}).get("sections", {}).get("qualifications", "")
                    or json.dumps(detail)
                )
            except Exception:
                description = json.dumps(j)

            jobs.append(Job(
                id=f"smartrecruiters:{identifier}:{j.get('id')}",
                company=company["name"],
                title=j.get("name", ""),
                location=location,
                url=j.get("ref", "") or
                    f"https://careers.smartrecruiters.com/{identifier}/{j.get('id')}",
                description=description,
                posted_at=j.get("releasedDate"),
                source="smartrecruiters",
            ))

        total = int(data.get("totalFound", len(content)) or 0)
        offset += len(content)
        if not content or offset >= total:
            break

    return jobs


def recruitee(company):
    subdomain = company["subdomain"]
    url = f"https://{subdomain}.recruitee.com/api/offers/"
    data = get_json(url)
    jobs = []

    # Recruitee has returned different wrapper shapes over time.
    offers = data.get("offers", data if isinstance(data, list) else [])

    for j in offers:
        slug = j.get("slug") or ""
        job_url = f"https://{subdomain}.recruitee.com/o/{slug}"
        locations = j.get("locations") or []
        if isinstance(locations, list):
            location = ", ".join(
                str(x.get("city") or x.get("name") or x)
                if isinstance(x, dict) else str(x)
                for x in locations
            )
        else:
            location = str(locations)

        description = (
            j.get("description")
            or j.get("description_html")
            or j.get("requirements")
            or ""
        )

        jobs.append(Job(
            id=f"recruitee:{subdomain}:{j.get('id') or slug}",
            company=company["name"],
            title=j.get("title", ""),
            location=location,
            url=job_url,
            description=description,
            posted_at=j.get("created_at") or j.get("published_at"),
            source="recruitee",
        ))

    return jobs


def html_fallback(company):
    url = company["url"]
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    jobs = []

    # Prefer JSON-LD JobPosting objects.
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text()
        try:
            obj = json.loads(raw)
        except Exception:
            continue

        objects = obj if isinstance(obj, list) else [obj]
        for item in objects:
            if not isinstance(item, dict):
                continue
            if item.get("@type") != "JobPosting":
                continue

            loc = item.get("jobLocation", "")
            if isinstance(loc, list):
                loc = loc[0] if loc else ""
            if isinstance(loc, dict):
                address = loc.get("address", {})
                if isinstance(address, dict):
                    loc = ", ".join(
                        str(x) for x in [
                            address.get("addressLocality"),
                            address.get("addressRegion"),
                            address.get("addressCountry"),
                        ] if x
                    )

            jobs.append(Job(
                id=f"jsonld:{company['name']}:{item.get('url') or item.get('title')}",
                company=company["name"],
                title=item.get("title", ""),
                location=str(loc),
                url=urljoin(url, item.get("url", "")),
                description=item.get("description", "") or "",
                posted_at=item.get("datePosted"),
                source="jsonld",
            ))

    if jobs:
        return jobs

    # Generic link fallback. This is deliberately broad but filtered later.
    for a in soup.find_all("a", href=True):
        text = " ".join(a.get_text(" ", strip=True).split())
        href = urljoin(url, a["href"])

        if len(text) < 8 or len(text) > 180:
            continue

        if not re.search(
            r"\b(intern|internship|engineer|engineering|designer|developer|"
            r"verification|embedded|firmware|hardware|semiconductor|graduate|"
            r"student|technical|research|scientist|technician)\b",
            text,
            re.I,
        ):
            continue

        jobs.append(Job(
            id=f"link:{company['name']}:{href}",
            company=company["name"],
            title=text,
            location="",
            url=href,
            description="",
            source="html",
        ))

    # Deduplicate links.
    seen = set()
    unique = []
    for job in jobs:
        if job.url in seen:
            continue
        seen.add(job.url)
        unique.append(job)

    return unique


def fetch(company):
    kind = company["type"]
    if kind == "disabled":
        return []
    if kind == "greenhouse":
        return greenhouse(company)
    if kind == "smartrecruiters":
        return smartrecruiters(company)
    if kind == "recruitee":
        return recruitee(company)
    if kind == "html":
        return html_fallback(company)
    raise ValueError(f"Unknown source type: {kind}")
