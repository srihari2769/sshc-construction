from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200))
    client_name = db.Column(db.String(100))
    completion_date = db.Column(db.Date)
    image_url = db.Column(db.String(300))  # Main/thumbnail image
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with media files
    media = db.relationship('ProjectMedia', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.title}>'

class ProjectMedia(db.Model):
    __tablename__ = 'project_media'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    file_url = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'image' or 'video'
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProjectMedia {self.file_type} for Project {self.project_id}>'

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50))
    image_url = db.Column(db.String(300))
    image_base64 = db.Column(db.Text)  # Base64 encoded image (persistent)
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.title}>'

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image_url = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testimonial {self.client_name}>'

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, responded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.name}>'

class CompanyInfo(db.Model):
    __tablename__ = 'company_info'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='Sri Shanmukha Harayanaraya Constructions')
    tagline = db.Column(db.String(300))
    about = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    facebook = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    youtube = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CompanyInfo {self.company_name}>'

class LuckyDrawSeries(db.Model):
    __tablename__ = 'lucky_draw_series'
    
    id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(50), unique=True, nullable=False)  # A, B, C, etc.
    total_tickets = db.Column(db.Integer, default=5000)
    available_tickets = db.Column(db.Integer, default=5000)
    ticket_price = db.Column(db.Integer, default=999)
    active = db.Column(db.Boolean, default=True)
    draw_date = db.Column(db.DateTime)
    winner_ticket = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    tickets = db.relationship('LuckyDrawTicket', backref='series', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LuckyDrawSeries {self.series_name}>'

class LuckyDrawTicket(db.Model):
    __tablename__ = 'lucky_draw_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)  # e.g., A-0001
    series_id = db.Column(db.Integer, db.ForeignKey('lucky_draw_series.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=True)  # Made optional for SMS-only flow
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.Text)
    refer_code = db.Column(db.String(50))  # Optional referral code
    payment_method = db.Column(db.String(20), default='upi')  # upi, qr
    transaction_id = db.Column(db.String(100))
    payment_screenshot = db.Column(db.String(300))  # File path (ephemeral on Render)
    payment_screenshot_base64 = db.Column(db.Text)  # Base64 encoded image (persistent)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_date = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LuckyDrawTicket {self.ticket_number}>'

class PaymentSettings(db.Model):
    __tablename__ = 'payment_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    upi_id = db.Column(db.String(100))
    qr_code_image = db.Column(db.String(300))  # File path (ephemeral on Render)
    qr_code_base64 = db.Column(db.Text)  # Base64 encoded image (persistent)
    payment_instructions = db.Column(db.Text)
    lucky_draw_description = db.Column(db.Text)  # Description about the lucky draw
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentSettings {self.id}>'

class PropertyDocument(db.Model):
    __tablename__ = 'property_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.String(300), nullable=False)
    file_base64 = db.Column(db.Text)  # Base64 encoded file (persistent for images)
    file_type = db.Column(db.String(50))  # pdf, jpg, png, etc.
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyDocument {self.title}>'

class LuckyDrawSettings(db.Model):
    __tablename__ = 'lucky_draw_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_price = db.Column(db.Integer, nullable=True)  # Made optional
    show_ticket_price = db.Column(db.Boolean, default=True)  # Toggle to show/hide price badge
    prize_title = db.Column(db.String(200), default='Premium 3BHK East-Facing Corner Flat')
    prize_description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LuckyDrawSettings {self.id}>'

