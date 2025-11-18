#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database tables
python init_db.py

# Run database migration (make email optional)
python migrate_email_optional.py
