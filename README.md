# Earnings and Expense Tracker

**Project by:** Rajasanjithh and Raja Chellam

A Flask-based expense tracker project with registration/login pages and an expense-tracking interface.

## Features
- User registration and login
- Monthly budget and expense tracking interface
- Expense charts and PDF export libraries in the frontend
- SQLite database created locally by the Flask application

## Requirements
- Python 3.10 or newer
- pip

## Run locally
1. Open a terminal in this project folder.
2. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the app: `python app.py`
5. Open the local address printed by Flask in your browser.

## Before public deployment
This repository is prepared for source-code sharing, not production deployment. Review authentication and security before deploying publicly: use password hashing, set a strong `SECRET_KEY` through an environment variable, enable HTTPS, and configure a production server. Do not commit databases or real user data.
