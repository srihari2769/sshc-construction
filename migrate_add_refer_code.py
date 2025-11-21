"""
Migration script to add refer_code column to lucky_draw_tickets table
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("🔄 Adding refer_code column to lucky_draw_tickets...")
            
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('lucky_draw_tickets')]
            
            if 'refer_code' not in columns:
                # Add the new column
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE lucky_draw_tickets ADD COLUMN refer_code VARCHAR(50)'))
                    conn.commit()
                print("✅ refer_code column added successfully")
            else:
                print("✓ refer_code column already exists")
            
            print("🎉 Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate()
