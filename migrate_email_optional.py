"""
Migration script to make customer_email optional in lucky_draw_tickets table
Runs automatically during Render deployment via build.sh
"""

from app import app, db
from sqlalchemy import inspect, text

def migrate_email_optional():
    """Make customer_email nullable in lucky_draw_tickets table"""
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            # Check if table exists
            if 'lucky_draw_tickets' not in inspector.get_table_names():
                print("ℹ️ Table lucky_draw_tickets does not exist yet. Skipping migration.")
                return
            
            # Check if column is already nullable
            columns = inspector.get_columns('lucky_draw_tickets')
            email_column = next((col for col in columns if col['name'] == 'customer_email'), None)
            
            if email_column and email_column.get('nullable', False):
                print("✅ customer_email is already nullable. Migration not needed.")
                return
            
            print("🔧 Making customer_email nullable...")
            
            # PostgreSQL: Alter column to allow NULL
            with db.engine.connect() as conn:
                conn.execute(text(
                    "ALTER TABLE lucky_draw_tickets ALTER COLUMN customer_email DROP NOT NULL"
                ))
                conn.commit()
            
            print("✅ Successfully made customer_email nullable!")
            print("   Email is now optional for Lucky Draw tickets")
            
        except Exception as e:
            print(f"⚠️ Migration info: {e}")
            print("   This is normal if the table doesn't exist yet or column is already nullable.")

if __name__ == '__main__':
    print("Running database migration: Make email optional...")
    migrate_email_optional()
