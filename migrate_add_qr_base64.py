"""
Migration script to add qr_code_base64 column to payment_settings table
This allows QR code to persist across deployments on Render
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("🔄 Adding qr_code_base64 column to payment_settings...")
            
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('payment_settings')]
            
            if 'qr_code_base64' not in columns:
                # Add the new column
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE payment_settings ADD COLUMN qr_code_base64 TEXT'))
                    conn.commit()
                print("✅ qr_code_base64 column added successfully")
            else:
                print("✓ qr_code_base64 column already exists")
            
            print("🎉 Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate()
