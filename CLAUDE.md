# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project Overview

CoinOfVantage is a Flask web application for a systematic crypto hedge fund targeting professional investors and family offices in the Benelux. Registered in Liechtenstein.

**Current stack:**
- Python 3.11 / Flask
- Vanilla CSS + JS (no frontend framework yet)
- No database yet — investor accounts are hardcoded in `app.py`
- Hosted on PythonAnywhere

**Target stack (planned):**
- MariaDB / MySQL with SQLAlchemy
- Bootstrap or Tailwind
- Blueprints-based modular structure
- OVH hosting (for GDPR compliance)

The application contains:
- Company information (home, about, strategy pages)
- Investor portal with TOTP-based authentication
- PDF generation (planned)
- Financial dashboards (planned)

---

# Architecture

## Current state

Single-file Flask app ([app.py](app.py)) with Jinja2 templates and a flat static folder.

**Auth flow (two-step on one form):**
1. `POST /login` — validates email + password + TOTP code simultaneously (not a multi-step wizard). `pyotp.TOTP.verify(..., valid_window=1)` accepts the current and adjacent 30-second windows.
2. `GET /login/setup?email=...` — generates a QR code (base64-encoded PNG) for TOTP enrollment. Accessible without authentication; only used during initial setup.
3. Session stores `investor_email` and `investor_name`. The `@login_required` decorator guards `/portal`.

**Template inheritance:** all pages extend `templates/base.html`, which includes the nav (session-aware), flash messages, footer, and loads `static/css/main.css` + `static/js/main.js`.

**Frontend:** vanilla JS in `main.js` — scroll-triggered fade-in animations via `IntersectionObserver` and auto-dismissing flash messages. Fonts: Cormorant Garamond (headings) + DM Sans (body) from Google Fonts.

## Target Flask structure (when refactoring)

```
/app
  /routes
  /services
  /models
  /templates
  /static
  /utils
```

- Keep routes thin — business logic in services/helpers
- Database queries centralized (no inline SQL everywhere)
- Use Blueprints for modularity
- Separate templates by feature/domain

---

# Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (http://127.0.0.1:5000)
python app.py

# Production
gunicorn -w 4 app:app
```

Demo login: `john.smith@investor.com` / `demo1234`

---

# Key Customisation Points

- **Investor accounts**: replace the `INVESTORS` dict with a real DB lookup before going to production.
- **Secret key**: `app.secret_key` must be changed and loaded from an environment variable in production.
- **Fund name / branding**: `CoinOfVantage` / `COINOFVANTAGE` appears in `base.html`, `app.py` (TOTP issuer), and page titles — search-replace all files.
- **Fund terms / team**: edit `templates/strategy.html` and `templates/about.html` directly.

---

# Development Principles

## Code Style

- Prefer readable and maintainable code over clever code.
- Use clear variable names.
- Keep functions small and focused.
- Avoid duplicated logic.
- Use type hints whenever possible.

## Preferred Libraries

- Flask, SQLAlchemy, WTForms, Pandas, FPDF, Requests

## Avoid

- Overengineering, massive classes, global mutable state, excessive JavaScript

---

# Database Rules

- Never perform destructive database actions without confirmation.
- Always create migrations for schema changes.
- Prefer normalized tables with consistent foreign keys.
- Avoid storing calculated values unless necessary.

---

# Frontend Guidelines

Color palette: dark green, white, light gray — professional finance aesthetic.

- Mobile-first responsive design.
- Use cards and whitespace generously.
- Avoid flashy animations.
- Prefer accessible contrast and typography.

---

# PDF Generation

- Use FPDF with UTF-8 compatibility.
- Use reusable PDF helper functions.
- Financial reports should look professional and minimal.

---

# Security Rules

- Use environment variables for all credentials and secrets.
- Sanitize all user inputs; protect against SQL injection.
- Protect forms with CSRF.
- Validate uploaded files server-side.

---

# Deployment

- PythonAnywhere production hosting, git-based deployment, virtualenv required.
- Before deploying: verify static files, migrations, authentication, PDF generation, and database connections.

---

# AI Assistant Instructions

- Preserve existing architecture; do not rewrite working components unnecessarily.
- Explain major refactors before applying them — prefer incremental improvements.
- When debugging: identify root cause first, then propose the minimal fix.
- Produce production-ready code; avoid placeholders unless requested.
- Include logging where relevant.
