# CoinOfVantage — Fund Website

Flask web application for CoinOfVantage, a systematic crypto hedge fund targeting professional investors and family offices in the Benelux. Registered in Liechtenstein.

## Current Stack

- Python 3.11 / Flask
- Jinja2 templates, vanilla CSS + JS
- PythonAnywhere hosting

## Features

- Company information (home, about, strategy)
- Investor portal with TOTP two-factor authentication
- PDF generation *(planned)*
- Financial dashboards *(planned)*

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the development server
python app.py
```

Visit: http://127.0.0.1:5000

## Demo Login

- Email: `john.smith@investor.com`
- Password: `demo1234`
- You will also need the TOTP code from your authenticator app (or use `/login/setup?email=john.smith@investor.com` to enroll).

## Customisation

- **Investor accounts**: replace the `INVESTORS` dict in `app.py` with a real database lookup before going to production.
- **Secret key**: change `app.secret_key` in `app.py` and load it from an environment variable in production.
- **Fund name / branding**: search-replace `CoinOfVantage` / `COINOFVANTAGE` across all files (`app.py`, `base.html`, page titles).
- **Fund terms / team**: edit `templates/strategy.html` and `templates/about.html` directly.

## Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 app:app
```

Use environment variables for all secrets. Currently hosted on PythonAnywhere; planned migration to OVH for GDPR compliance.
