"""
Migration script to add base64 columns for persistent image storage
Adds:
- image_base64 to services table
- payment_screenshot_base64 to lucky_draw_tickets table
- file_base64 to property_documents table
"""

import os
import sys
from app import app, db

def run_migration():
    with app.app_context():
        try:
            # Add image_base64 column to services table
            db.session.execute(db.text("""
                ALTER TABLE services 
                ADD COLUMN IF NOT EXISTS image_base64 TEXT;
            """))
            
            # Add payment_screenshot_base64 column to lucky_draw_tickets table
            db.session.execute(db.text("""
                ALTER TABLE lucky_draw_tickets 
                ADD COLUMN IF NOT EXISTS payment_screenshot_base64 TEXT;
            """))
            
            # Add file_base64 column to property_documents table
            db.session.execute(db.text("""
                ALTER TABLE property_documents 
                ADD COLUMN IF NOT EXISTS file_base64 TEXT;
            """))
            
            db.session.commit()
            print("✓ Successfully added base64 columns for image persistence")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    run_migration()
