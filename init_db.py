"""
Database initialization and seeding script for SSHC Construction Website
Run this script to populate the database with sample data
"""

from app import app, db
from models import User, Project, Service, Testimonial, CompanyInfo
from datetime import datetime, date

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@sshcbuilders.com').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                email='admin@sshcbuilders.com',
                name='Administrator',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Add company info
        company_info = CompanyInfo.query.first()
        if not company_info:
            print("Adding company information...")
            company_info = CompanyInfo(
                company_name='Sri Shanmukha Harayanaraya Constructions',
                tagline='Building Dreams, Creating Legacies',
                about='We are a leading construction company with over 15 years of experience in delivering quality projects. Our commitment to excellence, safety, and customer satisfaction has made us one of the most trusted names in the construction industry. We specialize in residential, commercial, and industrial projects, bringing innovation and expertise to every build.',
                phone='+1 (555) 123-4567',
                email='info@sshcbuilders.com',
                address='123 Construction Avenue, Building City, BC 12345',
                facebook='https://facebook.com/sshcbuilders',
                twitter='https://twitter.com/sshcbuilders',
                linkedin='https://linkedin.com/company/sshcbuilders',
                instagram='https://instagram.com/sshcbuilders'
            )
            db.session.add(company_info)
        
        # Add sample services
        if Service.query.count() == 0:
            print("Adding sample services...")
            services = [
                Service(
                    title='Residential Construction',
                    description='We build quality homes tailored to your lifestyle. From single-family homes to luxury estates, we bring your vision to life with attention to detail and superior craftsmanship.',
                    icon='fa-home',
                    order=1,
                    active=True
                ),
                Service(
                    title='Commercial Buildings',
                    description='Professional construction services for office buildings, retail spaces, and commercial complexes. We deliver projects on time and within budget while maintaining the highest quality standards.',
                    icon='fa-building',
                    order=2,
                    active=True
                ),
                Service(
                    title='Renovations & Remodeling',
                    description='Transform your existing space with our expert renovation and remodeling services. We handle everything from kitchen and bathroom upgrades to complete home makeovers.',
                    icon='fa-tools',
                    order=3,
                    active=True
                ),
                Service(
                    title='Project Management',
                    description='Comprehensive project management services ensuring your construction project runs smoothly from start to finish. We coordinate all aspects to deliver exceptional results.',
                    icon='fa-tasks',
                    order=4,
                    active=True
                ),
                Service(
                    title='Design & Planning',
                    description='Our expert design team works with you to create detailed plans that meet your needs and exceed expectations. We combine functionality with aesthetic appeal.',
                    icon='fa-drafting-compass',
                    order=5,
                    active=True
                ),
                Service(
                    title='Quality Assurance',
                    description='Rigorous quality control processes ensure every project meets our high standards. We inspect every detail to guarantee customer satisfaction and long-lasting results.',
                    icon='fa-check-circle',
                    order=6,
                    active=True
                )
            ]
            db.session.add_all(services)
        
        # Add sample projects
        if Project.query.count() == 0:
            print("Adding sample projects...")
            projects = [
                Project(
                    title='Modern Family Residence',
                    description='A beautiful 3500 sq ft modern family home featuring open floor plans, energy-efficient design, and premium finishes. This project showcases our expertise in contemporary residential construction with sustainable materials and smart home integration.',
                    category='Residential',
                    location='Green Valley Estates',
                    client_name='Johnson Family',
                    completion_date=date(2024, 6, 15),
                    featured=True
                ),
                Project(
                    title='Downtown Office Complex',
                    description='State-of-the-art 8-story office building in the heart of downtown, featuring modern amenities, sustainable design, and efficient workspace solutions. The project includes underground parking, rooftop gardens, and advanced HVAC systems.',
                    category='Commercial',
                    location='Downtown Business District',
                    client_name='Metro Corp',
                    completion_date=date(2024, 8, 30),
                    featured=True
                ),
                Project(
                    title='Luxury Villa Project',
                    description='Exclusive luxury villa with 5 bedrooms, infinity pool, home theater, and panoramic views. Custom designed with premium materials including marble flooring, designer fixtures, and landscaped gardens.',
                    category='Residential',
                    location='Hilltop Heights',
                    client_name='Private Client',
                    completion_date=date(2024, 3, 20),
                    featured=True
                ),
                Project(
                    title='Shopping Center Renovation',
                    description='Complete renovation of a 50,000 sq ft shopping center including facade updates, interior remodeling, and modernization of all systems. Enhanced customer experience with new lighting, flooring, and common areas.',
                    category='Commercial',
                    location='Westside Mall',
                    client_name='Retail Properties Inc',
                    completion_date=date(2024, 5, 10),
                    featured=False
                ),
                Project(
                    title='Industrial Warehouse',
                    description='Construction of a 75,000 sq ft industrial warehouse with high ceilings, loading docks, and advanced security systems. Built to accommodate modern logistics and distribution needs.',
                    category='Industrial',
                    location='Industrial Park West',
                    client_name='Logistics Solutions Ltd',
                    completion_date=date(2024, 7, 25),
                    featured=True
                ),
                Project(
                    title='Townhouse Community',
                    description='Development of 24 modern townhouses featuring contemporary designs, energy-efficient features, and community amenities including a park and walking trails.',
                    category='Residential',
                    location='Parkside Village',
                    client_name='Urban Living Developers',
                    completion_date=date(2024, 9, 15),
                    featured=True
                )
            ]
            db.session.add_all(projects)
        
        # Add sample testimonials
        if Testimonial.query.count() == 0:
            print("Adding sample testimonials...")
            testimonials = [
                Testimonial(
                    client_name='Robert Johnson',
                    company='Johnson Enterprises',
                    content='SSHC Constructions exceeded our expectations in every way. Their attention to detail, professionalism, and commitment to quality made our office building project a complete success. Highly recommended!',
                    rating=5,
                    active=True
                ),
                Testimonial(
                    client_name='Sarah Williams',
                    company='',
                    content='We are absolutely thrilled with our new home! The team was professional, responsive, and delivered exactly what they promised. The quality of workmanship is outstanding. Thank you for making our dream home a reality!',
                    rating=5,
                    active=True
                ),
                Testimonial(
                    client_name='Michael Chen',
                    company='Metro Retail Group',
                    content='The renovation of our shopping center was completed on time and within budget. The project management was excellent, and the end result has significantly improved our property value. Great work!',
                    rating=5,
                    active=True
                ),
                Testimonial(
                    client_name='Emily Rodriguez',
                    company='',
                    content='From initial consultation to final walkthrough, SSHC was professional and transparent. They kept us informed throughout the process and handled every detail with care. Our kitchen remodel is beautiful!',
                    rating=5,
                    active=True
                ),
                Testimonial(
                    client_name='David Thompson',
                    company='Thompson Logistics',
                    content='Outstanding work on our warehouse facility. The construction quality is top-notch, and they completed the project ahead of schedule. Very impressed with their efficiency and expertise.',
                    rating=5,
                    active=True
                ),
                Testimonial(
                    client_name='Jennifer Martinez',
                    company='Urban Developments',
                    content='Working with SSHC on our townhouse community was a pleasure. Their expertise in residential development and commitment to quality made this a successful partnership. Looking forward to future projects together.',
                    rating=5,
                    active=True
                )
            ]
            db.session.add_all(testimonials)
        
        # Commit all changes
        db.session.commit()
        print("\n✓ Database initialized successfully!")
        print("\nAdmin Login Credentials:")
        print("Email: admin@sshcbuilders.com")
        print("Password: admin123")
        print("\n⚠️  Please change the admin password after first login!")
        print("\nYou can now access:")
        print("- Public Website: http://localhost:5000")
        print("- Admin Panel: http://localhost:5000/admin/login")

if __name__ == '__main__':
    init_database()
