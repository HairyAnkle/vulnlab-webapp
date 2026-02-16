# VulnLab Web App (Build → Break → Fix)

> **Purpose:** A personal learning project for aspiring pentesters / web security folks.  
> **Format:** I build a realistic small web app, intentionally introduce common vulnerabilities, then **patch** them with secure implementations and **write professional reports** for each finding.

⚠️ **Educational Use Only:** This project is designed to run **locally in a lab environment**. Do not deploy the intentionally vulnerable versions to the public internet.

---

## What’s Inside

### App Modules (Realistic Mini-App)
- Authentication (register/login/logout)
- User profile
- Notes (CRUD)
- Avatar upload
- Basic admin panel

### Security Learning Goals
- Reproduce vulnerabilities in a controlled environment
- Document impact + exploitation steps
- Apply correct remediations
- Add regression checks to avoid reintroducing issues

---

## Planned Vulnerabilities (Vuln → Patch)

Each vulnerability will have:
- A **PoC** (proof of concept) and reproduction steps
- A short **impact analysis**
- A **fix** (secure refactor)
- Optional: regression test / security check

### Target Vulnerability Set
- **IDOR / Broken Access Control** (e.g., predictable note IDs)
- **Stored XSS** (notes/comments)
- **CSRF** (state-changing actions without token)
- **Weak Session / Auth Issues** (session config, brute-force controls)
- **File Upload Issues** (MIME validation, extension handling, path safety)
- **SQL Injection** *(only where raw SQL is used; later patched with parameterized queries)*
- **SSRF** *(URL preview/fetch feature; patched with allowlist + network restrictions)*

> I’ll track these in Git commits and/or PR-style changes so the “before vs after” is clear.

---

## Tech Stack (Planned)
You can choose either stack; I’ll commit the final selection once implemented:

- **Option A:** Node.js + Express + SQLite  
- **Option B:** Python + Flask/FastAPI + SQLite  

**Containerized with Docker** for easy local setup.

---

## Repository Structure (Planned)

```
.
├── app/                    # application source code
├── docker/                 # Dockerfile(s), compose, environment templates
├── reports/                # writeups for each vuln (PoC + impact + fix)
│   ├── IDOR.md
│   ├── Stored-XSS.md
│   ├── CSRF.md
│   └── ...
├── patches/                # optional: patch notes or diffs (if needed)
├── tests-security/         # regression tests / security checks
├── screenshots/            # PoC screenshots (redacted if needed)
└── README.md
```

---

## Setup (Placeholder — will update once code lands)

### Using Docker (recommended)
```bash
# 1) clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2) run
docker compose up --build
```

### Manual (non-docker)
```bash
# Steps will be added once the stack is finalized.
```

---

## How to Use (Learning Workflow)

1. Start the app locally  
2. Pick a vulnerability from `/reports/`  
3. Reproduce the issue (follow PoC steps)  
4. Checkout the patch commit (or “fixed” branch)  
5. Compare “vulnerable vs fixed” and run tests

---

## Reporting Standard

Reports aim to be readable like real pentest findings:
- **Title / Summary**
- **Affected endpoint(s)**
- **Severity** (simple rating or CVSS-style reasoning)
- **Steps to reproduce**
- **Impact**
- **Recommendation**
- **Patch summary**
- **References** (OWASP links, etc.)

---

## Roadmap

- [ ] Implement base app modules (auth, notes, profile, upload, admin)
- [ ] Add vulnerability #1 (IDOR) + report + patch
- [ ] Add vulnerability #2 (Stored XSS) + report + patch
- [ ] Add CSRF scenarios + fixes
- [ ] Harden sessions + add rate limiting + account lockout logic
- [ ] Secure file upload handling
- [ ] Add SSRF feature + safe remediation
- [ ] Add regression tests & security checks
- [ ] Record a short demo video (2–3 minutes)

---

## Disclaimer

This repository contains intentionally vulnerable code **for educational purposes**.  
Use only in environments you own or have explicit permission to test.

---

## License
Choose one:
- MIT (simple and common), or
- Apache-2.0

*(I’ll add the actual LICENSE file when you pick.)*
