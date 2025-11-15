from app import app, db
from models import LuckyDrawSeries, PaymentSettings

def migrate_lucky_draw():
    """Create Lucky Draw tables and initialize series A-Z"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Lucky Draw tables created successfully!")
        
        # Check if series already exist
        existing_series = LuckyDrawSeries.query.first()
        if existing_series:
            print("Series already initialized. Skipping...")
            return
        
        # Initialize A-Z series (26 series)
        print("Initializing A-Z series...")
        for i in range(26):
            series_name = chr(65 + i)  # A=65 in ASCII
            series = LuckyDrawSeries(
                series_name=series_name,
                total_tickets=5000,
                available_tickets=5000,
                ticket_price=999,
                active=True
            )
            db.session.add(series)
        
        # Create default payment settings
        payment_settings = PaymentSettings(
            upi_id='',
            qr_code_image='',
            payment_instructions='Please complete the payment and upload the screenshot for verification.',
            lucky_draw_description=''
        )
        db.session.add(payment_settings)
        
        db.session.commit()
        print("Successfully initialized 26 series (A-Z) with 5000 tickets each at ₹999!")
        print("Default payment settings created!")

if __name__ == '__main__':
    migrate_lucky_draw()
