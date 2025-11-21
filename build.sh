#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations FIRST (before init_db.py)
# These add columns to existing tables

# Run database migration (make email optional)
python migrate_email_optional.py

# Add property documents and settings tables
python migrate_add_documents_and_settings.py

# Add QR code base64 column for persistent storage
python migrate_add_qr_base64.py

# Add refer code column to lucky draw tickets
python migrate_add_refer_code.py

# Add base64 columns for persistent image storage
python migrate_add_image_base64.py

# Add show_ticket_price toggle and make ticket_price optional
python migrate_add_price_toggle.py

# Initialize database tables (creates tables if they don't exist and seeds data)
python init_db.py
