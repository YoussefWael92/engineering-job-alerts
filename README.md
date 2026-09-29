# Personal Engineering Job Alert Bot

A free GitHub Actions job monitor that checks selected company career sites,
filters for engineering roles, remembers jobs already seen, and emails only new matches.

## Companies included in the starter configuration

- Siemens
- Analog Devices
- STMicroelectronics
- Bosch
- NVIDIA
- Intel
- GlobalFoundries
- Synopsys
- SI-Vision
- Mixel / Silvaco
- Si-Ware Systems
- InfiniLink (manual URL placeholder; verify the exact careers page)

The collector supports:
- SmartRecruiters public postings API
- Recruitee careers API
- Greenhouse job boards
- HTML/JSON-LD fallback for company career pages

## Important

The bot does not apply to jobs. It only collects public postings and sends you the
company's application link.

For GitHub Actions, use a PUBLIC repository if you want the standard hosted runner
to be free. Do not put your email password in the repository.

## Setup

### 1. Create a GitHub repository

Create a public repo, e.g. `engineering-job-alerts`.

Upload this project.

### 2. Add GitHub Secrets

Repository -> Settings -> Secrets and variables -> Actions -> New repository secret

Add:

- `MAIL_USERNAME` = your Gmail address
- `MAIL_APP_PASSWORD` = a Gmail App Password
- `MAIL_TO` = the address where you want the alerts

Do not use your normal Gmail password.

### 3. Run it manually once

Actions -> Engineering Job Alerts -> Run workflow.

The first successful run creates `data/jobs.json` in the repository.

### 4. Enable the schedule

The workflow is configured to run every 30 minutes.

GitHub scheduled workflows use UTC unless a timezone is explicitly specified.
The workflow below uses `Africa/Cairo`.

### 5. Customize your targets

Edit:

`job_alert/config.py`

Change:
- keywords
- locations
- minimum relevance score
- companies

## How matching works

The first version uses deterministic keyword scoring, not AI.

A job receives points for title/description matches. Internship/student/new-grad
roles get extra points. Senior-only roles are penalized.

This keeps the bot free and predictable.

## Data storage

`data/jobs.json` stores the IDs of jobs already processed.

The bot commits this file back to the repository after each run.

If you delete the file, the next run will treat matching jobs as new.

## Adding a company

Prefer finding the company's ATS first.

Examples:

### SmartRecruiters

```python
{
    "name": "Bosch",
    "type": "smartrecruiters",
    "identifier": "BoschGroup",
    "locations": ["egypt", "cairo"],
}
```

### Recruitee

```python
{
    "name": "Si-Ware Systems",
    "type": "recruitee",
    "subdomain": "siwaresystems",
}
```

### Greenhouse

```python
{
    "name": "Example",
    "type": "greenhouse",
    "board": "example",
}
```

### HTML fallback

```python
{
    "name": "Example",
    "type": "html",
    "url": "https://example.com/careers",
}
```

## Notes

Some large-company career sites are JavaScript-heavy or change their site structure.
For those companies, the HTML connector may need a company-specific adapter later.
The architecture is deliberately separated so those adapters can be added without
changing the filtering/email/database logic.
