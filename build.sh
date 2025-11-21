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

# Add property documents and settings tables
python migrate_add_documents_and_settings.py

# Add QR code base64 column for persistent storage
python migrate_add_qr_base64.py

# Add refer code column to lucky draw tickets
python migrate_add_refer_code.py
