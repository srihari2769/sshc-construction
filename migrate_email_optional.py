"""
Migration script to make customer_email optional in lucky_draw_tickets table
Run this after deploying to Render or on your local database
"""

from app import app, db
from sqlalchemy import inspect

def migrate_email_optional():
    """Make customer_email nullable in lucky_draw_tickets table"""
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check if table exists
        if 'lucky_draw_tickets' not in inspector.get_table_names():
            print("❌ Table lucky_draw_tickets does not exist!")
            return
        
        try:
            # PostgreSQL: Alter column to allow NULL
            db.engine.execute(
                "ALTER TABLE lucky_draw_tickets ALTER COLUMN customer_email DROP NOT NULL"
            )
            print("✅ Successfully made customer_email nullable!")
            print("   Email is now optional for Lucky Draw tickets")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            print("   You may need to run this SQL manually:")
            print("   ALTER TABLE lucky_draw_tickets ALTER COLUMN customer_email DROP NOT NULL;")

if __name__ == '__main__':
    print("Making customer_email optional in lucky_draw_tickets...")
    migrate_email_optional()
