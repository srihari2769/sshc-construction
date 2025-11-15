from app import app, db

def add_description_column():
    """Add lucky_draw_description column to payment_settings table"""
    with app.app_context():
        try:
            # Add the column to the database
            db.session.execute(db.text(
                "ALTER TABLE payment_settings ADD COLUMN IF NOT EXISTS lucky_draw_description TEXT"
            ))
            db.session.commit()
            print("✅ Column 'lucky_draw_description' added successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_description_column()
