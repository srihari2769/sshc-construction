"""
Database Migration Script
Adds ProjectMedia table for supporting multiple images and videos per project
"""
from app import app
from models import db, ProjectMedia

def migrate_database():
    with app.app_context():
        print("Creating new tables...")
        
        # Create only the new ProjectMedia table
        db.create_all()
        
        print("✓ Migration completed successfully!")
        print("\nNew features:")
        print("- Multiple images per project")
        print("- Multiple videos per project")
        print("- Media management in admin panel")

if __name__ == '__main__':
    migrate_database()
