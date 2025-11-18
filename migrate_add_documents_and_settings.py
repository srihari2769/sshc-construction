"""
Migration script to add PropertyDocument and LuckyDrawSettings tables
Run this script to update the database schema
"""
from app import app, db
from models import PropertyDocument, LuckyDrawSettings
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Check if tables already exist
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print("🔄 Starting migration...")
            
            # Create PropertyDocument table if it doesn't exist
            if 'property_documents' not in existing_tables:
                print("📄 Creating property_documents table...")
                db.create_all()
                print("✅ property_documents table created successfully")
            else:
                print("✓ property_documents table already exists")
            
            # Create LuckyDrawSettings table if it doesn't exist
            if 'lucky_draw_settings' not in existing_tables:
                print("⚙️ Creating lucky_draw_settings table...")
                db.create_all()
                print("✅ lucky_draw_settings table created successfully")
            else:
                print("✓ lucky_draw_settings table already exists")
            
            # Initialize default settings if table is empty
            settings = LuckyDrawSettings.query.first()
            if not settings:
                print("📝 Creating default lucky draw settings...")
                settings = LuckyDrawSettings(
                    ticket_price=999,
                    prize_title='Premium 3BHK East-Facing Corner Flat',
                    prize_description='Win a Premium 3BHK East-Facing Corner Flat ✨ TUDA Approved ✨ Spacious 1360 sq. ft. ✨ Worth ₹51,00,000'
                )
                db.session.add(settings)
                db.session.commit()
                print("✅ Default settings created")
            else:
                print("✓ Lucky draw settings already exist")
            
            print("🎉 Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate()
