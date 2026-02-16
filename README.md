# VulnLab Web App (Build → Break → Fix)

A local-first security learning project: build a realistic mini web app, introduce vulnerabilities in controlled commits, then patch and document them.

## Finalized Stack

- **Python 3.12**
- **Flask**
- **SQLite**
- **Docker / Docker Compose**

## Current App Modules

- Authentication (register/login/logout)
- User profile (bio + avatar upload)
- Notes CRUD (access-controlled)
- Basic admin panel

## Quick Start

### Docker (recommended)

```bash
docker compose up --build
```

Then open: `http://localhost:5000`

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py init-db
flask --app run.py create-admin
flask --app run.py seed-lab
python run.py
```

Then open: `http://localhost:5000`

## Default Workflow

1. Initialize/run the app.
2. Register users and create baseline data.
3. Add a vulnerability scenario in a dedicated change.
4. Write a report in `reports/` with PoC + impact + remediation.
5. Patch and add regression checks in `tests-security/`.

## Repository Layout

```text
.
├── app/                    # Flask app source
├── docker/                 # Dockerfile
├── reports/                # vulnerability write-ups
├── patches/                # optional patch notes
├── tests-security/         # regression/security checks
├── screenshots/            # PoC screenshots
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## Disclaimer

Intentionally vulnerable variants should be used **only** in local labs or authorized environments.
