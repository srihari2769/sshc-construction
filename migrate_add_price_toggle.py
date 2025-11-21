"""
Migration script to add show_ticket_price toggle and make ticket_price nullable
"""

import os
import sys
from app import app, db

def run_migration():
    with app.app_context():
        try:
            # Add show_ticket_price column to lucky_draw_settings table
            db.session.execute(db.text("""
                ALTER TABLE lucky_draw_settings 
                ADD COLUMN IF NOT EXISTS show_ticket_price BOOLEAN DEFAULT TRUE;
            """))
            
            # Make ticket_price nullable (remove NOT NULL constraint if exists)
            db.session.execute(db.text("""
                ALTER TABLE lucky_draw_settings 
                ALTER COLUMN ticket_price DROP NOT NULL;
            """))
            
            db.session.commit()
            print("✓ Successfully added show_ticket_price toggle and made ticket_price optional")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    run_migration()
