import re
from .config import KEYWORDS, ROLE_KEYWORDS, PREFERRED_LOCATIONS, MIN_SCORE


def clean_html(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or "")).strip()


def score_job(job):
    title = (job.title or "").lower()
    location = (job.location or "").lower()
    description = clean_html(job.description).lower()

    score = 0

    # Title matches are more valuable than description-only matches.
    for keyword in KEYWORDS:
        if keyword.lower() in title:
            score += 5
        elif keyword.lower() in description:
            score += 2

    for keyword in ROLE_KEYWORDS:
        if keyword.lower() in title:
            score += 3
        elif keyword.lower() in description[:5000]:
            score += 1

    for loc in PREFERRED_LOCATIONS:
        if loc.lower() in location or loc.lower() in title:
            score += 3

    # Penalize obviously senior roles so the inbox stays useful.
    senior_terms = [
        "senior", "staff", "principal", "director", "manager",
        "lead architect", "10+ years", "8+ years"
    ]
    for term in senior_terms:
        if term in title:
            score -= 8

    return score


def matches(job):
    return score_job(job) >= MIN_SCORE
