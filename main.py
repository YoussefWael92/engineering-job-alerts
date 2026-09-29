import logging

from job_alert.config import COMPANIES
from job_alert.sources import fetch
from job_alert.filtering import matches, score_job
from job_alert.storage import load_seen, save_seen
from job_alert.emailer import send_email


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main():
    seen = load_seen()
    newly_seen = set(seen)
    new_matches = []

for company in COMPANIES:
    logging.info("Starting %s...", company["name"])

    try:
        jobs = fetch(company)
            logging.info("%s: collected %d jobs", company["name"], len(jobs))
        except Exception as exc:
            logging.exception(
                "%s failed: %s",
                company["name"],
                exc,
            )
            continue

        for job in jobs:
            if not matches(job):
                continue

            if job.id in seen:
                continue

            newly_seen.add(job.id)
            new_matches.append((job, score_job(job)))

    if new_matches:
        # Highest relevance first.
        new_matches.sort(key=lambda x: x[1], reverse=True)
        logging.info("Sending %d new matches", len(new_matches))
        send_email(new_matches)
    else:
        logging.info("No new matching jobs.")

    save_seen(newly_seen)


if __name__ == "__main__":
    main()
