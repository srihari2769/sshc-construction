from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Project, ProjectMedia, Service, Testimonial, Contact, CompanyInfo, LuckyDrawSeries, LuckyDrawTicket, PaymentSettings
import os
import random
import string
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def allowed_video(filename):
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm', 'mkv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def send_ticket_confirmation_email(ticket):
    """Send confirmation email to customer when ticket is confirmed"""
    try:
        # Skip if no email provided
        if not ticket.customer_email:
            print("ℹ️ No email provided for this ticket. Skipping email notification.")
            return
        
        # Check email configuration
        if not app.config.get('MAIL_USERNAME'):
            print("❌ ERROR: Email not configured. MAIL_USERNAME is missing.")
            raise ValueError("Email configuration missing: MAIL_USERNAME not set")
        
        if not app.config.get('MAIL_PASSWORD'):
            print("❌ ERROR: Email not configured. MAIL_PASSWORD is missing.")
            raise ValueError("Email configuration missing: MAIL_PASSWORD not set")
        
        print(f"📧 Preparing to send email to: {ticket.customer_email}")
        print(f"📧 Mail server: {app.config.get('MAIL_SERVER')}")
        print(f"📧 Mail port: {app.config.get('MAIL_PORT')}")
        print(f"📧 Mail username: {app.config.get('MAIL_USERNAME')}")
        print(f"📧 TLS enabled: {app.config.get('MAIL_USE_TLS')}")
        
        company_info = CompanyInfo.query.first()
        company_name = company_info.company_name if company_info else "Sri Shanmukha Harayanaraya Constructions"
        
        subject = f"Lucky Draw Ticket {ticket.ticket_number} - Confirmed!"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .ticket-info {{ background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }}
                .ticket-number {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; margin: 20px 0; }}
                .info-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
                .label {{ font-weight: 600; color: #555; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Ticket Confirmed!</h1>
                    <p>Your Lucky Draw ticket has been confirmed</p>
                </div>
                <div class="content">
                    <div class="ticket-number">{ticket.ticket_number}</div>
                    
                    <div class="ticket-info">
                        <h2 style="color: #667eea; margin-top: 0;">Ticket Details</h2>
                        <div class="info-row">
                            <span class="label">Customer Name:</span> {ticket.customer_name}
                        </div>
                        <div class="info-row">
                            <span class="label">Series:</span> {ticket.series.series_name}
                        </div>
                        <div class="info-row">
                            <span class="label">Purchase Date:</span> {ticket.purchase_date.strftime('%d %B %Y at %H:%M')}
                        </div>
                        <div class="info-row">
                            <span class="label">Confirmed Date:</span> {ticket.confirmed_date.strftime('%d %B %Y at %H:%M')}
                        </div>
                        <div class="info-row">
                            <span class="label">Status:</span> <strong style="color: #28a745;">CONFIRMED</strong>
                        </div>
                    </div>
                    
                    <p style="margin-top: 30px;">
                        Congratulations! Your ticket has been successfully confirmed. 
                        Please keep this email for your records. The draw date will be announced soon.
                    </p>
                    
                    <p style="color: #667eea; font-weight: 600;">
                        Good luck! 🍀
                    </p>
                </div>
                <div class="footer">
                    <p>{company_name}</p>
                    <p style="font-size: 12px;">This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        print(f"📧 Creating email message...")
        msg = Message(
            subject=subject,
            sender=app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME'),
            recipients=[ticket.customer_email],
            html=html_body
        )
        
        print(f"📧 Sending email via Flask-Mail...")
        mail.send(msg)
        print(f"✅ SUCCESS: Confirmation email sent to {ticket.customer_email}")
        
    except Exception as e:
        print(f"❌ ERROR sending email: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def send_ticket_sms(ticket):
    """Send SMS notification to customer after ticket purchase"""
    try:
        print(f"📱 Preparing to send SMS to: {ticket.customer_phone}")
        
        # Prepare SMS message
        message = f"🎉 Lucky Draw Ticket Purchased!\n\nTicket: {ticket.ticket_number}\nSeries: {ticket.series.series_name}\nName: {ticket.customer_name}\nStatus: Pending Confirmation\n\nThank you! - SSHC Builders"
        
        # TODO: Integrate with SMS service (Twilio, MSG91, or AWS SNS)
        # For now, just log the message
        print(f"📱 SMS Message:\n{message}")
        print(f"✅ SMS would be sent to: {ticket.customer_phone}")
        
        # When you integrate SMS service, use:
        # - Twilio: https://www.twilio.com/docs/sms/quickstart/python
        # - MSG91: https://msg91.com/
        # - AWS SNS: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sns-examples.html
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR sending SMS: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# Public Routes
@app.route('/')
def index():
    company_info = CompanyInfo.query.first()
    featured_projects = Project.query.filter_by(featured=True).limit(6).all()
    services = Service.query.filter_by(active=True).order_by(Service.order).all()
    testimonials = Testimonial.query.filter_by(active=True).limit(6).all()
    return render_template('index.html', 
                         company_info=company_info,
                         featured_projects=featured_projects,
                         services=services,
                         testimonials=testimonials)

@app.route('/about')
def about():
    company_info = CompanyInfo.query.first()
    return render_template('about.html', company_info=company_info)

@app.route('/services')
def services():
    company_info = CompanyInfo.query.first()
    services = Service.query.filter_by(active=True).order_by(Service.order).all()
    return render_template('services.html', company_info=company_info, services=services)

@app.route('/projects')
def projects():
    company_info = CompanyInfo.query.first()
    category = request.args.get('category', 'all')
    if category == 'all':
        projects = Project.query.order_by(Project.created_at.desc()).all()
    else:
        projects = Project.query.filter_by(category=category).order_by(Project.created_at.desc()).all()
    
    categories = db.session.query(Project.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('projects.html', 
                         company_info=company_info,
                         projects=projects,
                         categories=categories,
                         current_category=category)

@app.route('/project/<int:id>')
def project_detail(id):
    company_info = CompanyInfo.query.first()
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', company_info=company_info, project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    company_info = CompanyInfo.query.first()
    if request.method == 'POST':
        contact = Contact(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),
            subject=request.form.get('subject', ''),
            message=request.form['message']
        )
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', company_info=company_info)

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    projects_count = Project.query.count()
    services_count = Service.query.count()
    contacts_count = Contact.query.filter_by(status='new').count()
    testimonials_count = Testimonial.query.count()
    
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         projects_count=projects_count,
                         services_count=services_count,
                         contacts_count=contacts_count,
                         testimonials_count=testimonials_count,
                         recent_contacts=recent_contacts)

# Admin - Projects
@app.route('/admin/projects')
@login_required
def admin_projects():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def admin_add_project():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Handle main thumbnail image
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f"/static/uploads/{filename}"
        
        completion_date = None
        if request.form.get('completion_date'):
            completion_date = datetime.strptime(request.form['completion_date'], '%Y-%m-%d').date()
        
        # Create project
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            location=request.form.get('location', ''),
            client_name=request.form.get('client_name', ''),
            completion_date=completion_date,
            image_url=image_url,
            featured=bool(request.form.get('featured'))
        )
        db.session.add(project)
        db.session.flush()  # Get project ID
        
        # Handle multiple additional images
        if 'images' in request.files:
            files = request.files.getlist('images')
            for idx, file in enumerate(files):
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().timestamp()}_{idx}_{filename}"
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = f"/static/uploads/{filename}"
                    
                    media = ProjectMedia(
                        project_id=project.id,
                        file_url=file_url,
                        file_type='image',
                        order=idx
                    )
                    db.session.add(media)
        
        # Handle multiple videos
        if 'videos' in request.files:
            files = request.files.getlist('videos')
            for idx, file in enumerate(files):
                if file and file.filename and allowed_video(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().timestamp()}_{idx}_{filename}"
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = f"/static/uploads/{filename}"
                    
                    media = ProjectMedia(
                        project_id=project.id,
                        file_url=file_url,
                        file_type='video',
                        order=idx
                    )
                    db.session.add(media)
        
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', project=None)

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.category = request.form['category']
        project.location = request.form.get('location', '')
        project.client_name = request.form.get('client_name', '')
        
        if request.form.get('completion_date'):
            project.completion_date = datetime.strptime(request.form['completion_date'], '%Y-%m-%d').date()
        
        project.featured = bool(request.form.get('featured'))
        
        # Update main thumbnail image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                project.image_url = f"/static/uploads/{filename}"
        
        # Handle multiple additional images
        if 'images' in request.files:
            files = request.files.getlist('images')
            for idx, file in enumerate(files):
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().timestamp()}_{idx}_{filename}"
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = f"/static/uploads/{filename}"
                    
                    media = ProjectMedia(
                        project_id=project.id,
                        file_url=file_url,
                        file_type='image',
                        order=idx
                    )
                    db.session.add(media)
        
        # Handle multiple videos
        if 'videos' in request.files:
            files = request.files.getlist('videos')
            for idx, file in enumerate(files):
                if file and file.filename and allowed_video(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().timestamp()}_{idx}_{filename}"
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = f"/static/uploads/{filename}"
                    
                    media = ProjectMedia(
                        project_id=project.id,
                        file_url=file_url,
                        file_type='video',
                        order=idx
                    )
                    db.session.add(media)
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', project=project)

@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_project(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return jsonify({'success': True})

@app.route('/admin/media/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_media(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    media = ProjectMedia.query.get_or_404(id)
    db.session.delete(media)
    db.session.commit()
    return jsonify({'success': True})

# Admin - Services
@app.route('/admin/services')
@login_required
def admin_services():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services.html', services=services)

@app.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
def admin_add_service():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f"/static/uploads/{filename}"
        
        service = Service(
            title=request.form['title'],
            description=request.form['description'],
            icon=request.form.get('icon', 'fa-building'),
            image_url=image_url,
            order=int(request.form.get('order', 0)),
            active=bool(request.form.get('active', True))
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_form.html', service=None)

@app.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_service(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.title = request.form['title']
        service.description = request.form['description']
        service.icon = request.form.get('icon', 'fa-building')
        service.order = int(request.form.get('order', 0))
        service.active = bool(request.form.get('active'))
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                service.image_url = f"/static/uploads/{filename}"
        
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_form.html', service=service)

@app.route('/admin/services/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_service(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return jsonify({'success': True})

# Admin - Testimonials
@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
@login_required
def admin_add_testimonial():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f"/static/uploads/{filename}"
        
        testimonial = Testimonial(
            client_name=request.form['client_name'],
            company=request.form.get('company', ''),
            content=request.form['content'],
            rating=int(request.form.get('rating', 5)),
            image_url=image_url,
            active=bool(request.form.get('active', True))
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=None)

@app.route('/admin/testimonials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_testimonial(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'POST':
        testimonial.client_name = request.form['client_name']
        testimonial.company = request.form.get('company', '')
        testimonial.content = request.form['content']
        testimonial.rating = int(request.form.get('rating', 5))
        testimonial.active = bool(request.form.get('active'))
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                testimonial.image_url = f"/static/uploads/{filename}"
        
        db.session.commit()
        flash('Testimonial updated successfully!', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

@app.route('/admin/testimonials/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_testimonial(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Testimonial deleted successfully!', 'success')
    return jsonify({'success': True})

# Admin - Contacts
@app.route('/admin/contacts')
@login_required
def admin_contacts():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    status = request.args.get('status', 'all')
    if status == 'all':
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    else:
        contacts = Contact.query.filter_by(status=status).order_by(Contact.created_at.desc()).all()
    
    return render_template('admin/contacts.html', contacts=contacts, current_status=status)

@app.route('/admin/contacts/<int:id>/status', methods=['POST'])
@login_required
def admin_update_contact_status(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    contact = Contact.query.get_or_404(id)
    contact.status = request.json.get('status', 'new')
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/contacts/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_contact(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return jsonify({'success': True})

# Admin - Company Info
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    company_info = CompanyInfo.query.first()
    if not company_info:
        company_info = CompanyInfo()
        db.session.add(company_info)
        db.session.commit()
    
    if request.method == 'POST':
        company_info.company_name = request.form['company_name']
        company_info.tagline = request.form.get('tagline', '')
        company_info.about = request.form.get('about', '')
        company_info.phone = request.form.get('phone', '')
        company_info.email = request.form.get('email', '')
        company_info.address = request.form.get('address', '')
        company_info.facebook = request.form.get('facebook', '')
        company_info.twitter = request.form.get('twitter', '')
        company_info.linkedin = request.form.get('linkedin', '')
        company_info.instagram = request.form.get('instagram', '')
        company_info.youtube = request.form.get('youtube', '')
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', company_info=company_info)

# Lucky Draw - Public Routes
@app.route('/lucky-draw')
def lucky_draw():
    company_info = CompanyInfo.query.first()
    active_series = LuckyDrawSeries.query.filter_by(active=True).all()
    payment_settings = PaymentSettings.query.first()
    return render_template('lucky_draw.html', company_info=company_info, active_series=active_series, payment_settings=payment_settings)

@app.route('/lucky-draw/purchase', methods=['POST'])
def purchase_ticket():
    # Get form data
    customer_name = request.form['customer_name']
    customer_email = request.form['customer_email']
    customer_phone = request.form['customer_phone']
    customer_address = request.form.get('customer_address', '')
    payment_method = request.form['payment_method']
    transaction_id = request.form.get('transaction_id', '')
    
    # Handle payment screenshot upload
    payment_screenshot = ''
    if 'payment_screenshot' in request.files:
        file = request.files['payment_screenshot']
        print(f"DEBUG: File received: {file.filename if file else 'No file'}")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"payment_{datetime.now().timestamp()}_{filename}"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)
            payment_screenshot = f"/static/uploads/{filename}"
            print(f"DEBUG: File saved at: {upload_path}")
            print(f"DEBUG: Payment screenshot path: {payment_screenshot}")
        else:
            print(f"DEBUG: File validation failed or no filename")
    else:
        print("DEBUG: No payment_screenshot in request.files")
    
    # Get random available series (jumbled selection)
    available_series = LuckyDrawSeries.query.filter(
        LuckyDrawSeries.active == True,
        LuckyDrawSeries.available_tickets > 0
    ).all()
    
    if not available_series:
        flash('Sorry, no tickets available at the moment!', 'error')
        return redirect(url_for('lucky_draw'))
    
    # Random selection from available series
    selected_series = random.choice(available_series)
    
    # Generate random ticket number (jumbled system)
    # Get all existing ticket numbers for this series
    existing_tickets = LuckyDrawTicket.query.filter_by(series_id=selected_series.id).all()
    used_numbers = set(int(ticket.ticket_number.split('-')[1]) for ticket in existing_tickets)
    
    # Generate a random ticket number from 1 to total_tickets that hasn't been used
    available_numbers = [num for num in range(1, selected_series.total_tickets + 1) if num not in used_numbers]
    
    if not available_numbers:
        flash('Sorry, no tickets available in the selected series!', 'error')
        return redirect(url_for('lucky_draw'))
    
    # Pick a random ticket number from available numbers
    random_ticket_num = random.choice(available_numbers)
    ticket_number = f"{selected_series.series_name}-{random_ticket_num:04d}"
    
    # Create ticket
    ticket = LuckyDrawTicket(
        ticket_number=ticket_number,
        series_id=selected_series.id,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        customer_address=customer_address,
        payment_method=payment_method,
        transaction_id=transaction_id,
        payment_screenshot=payment_screenshot,
        status='pending'
    )
    
    db.session.add(ticket)
    selected_series.available_tickets -= 1
    db.session.commit()
    
    # Send SMS notification to customer
    try:
        send_ticket_sms(ticket)
    except Exception as e:
        print(f"Warning: SMS notification failed: {e}")
        # Don't fail the purchase if SMS fails
    
    flash(f'Ticket {ticket_number} purchased successfully! You will receive an SMS confirmation shortly. Waiting for admin confirmation.', 'success')
    return redirect(url_for('lucky_draw'))

# Admin - Lucky Draw Management
@app.route('/admin/lucky-draw')
@login_required
def admin_lucky_draw():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    series = LuckyDrawSeries.query.order_by(LuckyDrawSeries.series_name).all()
    return render_template('admin/lucky_draw_series.html', series=series)

@app.route('/admin/lucky-draw/series/add', methods=['GET', 'POST'])
@login_required
def admin_add_series():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        series = LuckyDrawSeries(
            series_name=request.form['series_name'].upper(),
            total_tickets=int(request.form['total_tickets']),
            available_tickets=int(request.form['total_tickets']),
            ticket_price=int(request.form['ticket_price']),
            active=bool(request.form.get('active'))
        )
        db.session.add(series)
        db.session.commit()
        flash('Series added successfully!', 'success')
        return redirect(url_for('admin_lucky_draw'))
    
    return render_template('admin/lucky_draw_series_form.html', series=None)

@app.route('/admin/lucky-draw/series/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_series(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    series = LuckyDrawSeries.query.get_or_404(id)
    
    if request.method == 'POST':
        series.series_name = request.form['series_name'].upper()
        series.total_tickets = int(request.form['total_tickets'])
        series.ticket_price = int(request.form['ticket_price'])
        series.active = bool(request.form.get('active'))
        
        db.session.commit()
        flash('Series updated successfully!', 'success')
        return redirect(url_for('admin_lucky_draw'))
    
    return render_template('admin/lucky_draw_series_form.html', series=series)

@app.route('/admin/lucky-draw/series/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_series(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    series = LuckyDrawSeries.query.get_or_404(id)
    db.session.delete(series)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/lucky-draw/tickets')
@login_required
def admin_lucky_draw_tickets():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    status = request.args.get('status', '')
    query = LuckyDrawTicket.query
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(LuckyDrawTicket.purchase_date.desc()).all()
    return render_template('admin/lucky_draw_tickets.html', tickets=tickets, current_status=status)

@app.route('/admin/lucky-draw/tickets/confirm/<int:id>', methods=['POST'])
@login_required
def admin_confirm_ticket(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    ticket = LuckyDrawTicket.query.get_or_404(id)
    ticket.status = 'confirmed'
    ticket.confirmed_date = datetime.utcnow()
    db.session.commit()
    
    # Send notifications to customer
    email_sent = False
    sms_sent = False
    
    # Send email notification if email is provided
    if ticket.customer_email:
        try:
            print(f"🎫 Ticket {ticket.ticket_number} confirmed. Attempting to send email...")
            send_ticket_confirmation_email(ticket)
            email_sent = True
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"❌ Email sending failed: {error_msg}")
    
    # Send SMS notification
    try:
        sms_sent = send_ticket_sms(ticket)
    except Exception as e:
        print(f"⚠️ SMS sending failed: {e}")
    
    # Show appropriate success message
    if email_sent and sms_sent:
        flash(f'Ticket {ticket.ticket_number} confirmed! Email & SMS sent to customer.', 'success')
    elif email_sent:
        flash(f'Ticket {ticket.ticket_number} confirmed! Email sent to {ticket.customer_email}', 'success')
    elif sms_sent:
        flash(f'Ticket {ticket.ticket_number} confirmed! SMS sent to {ticket.customer_phone}', 'success')
    else:
        flash(f'Ticket {ticket.ticket_number} confirmed! (Notifications may have failed)', 'warning')
    
    return jsonify({'success': True})

@app.route('/admin/lucky-draw/tickets/cancel/<int:id>', methods=['POST'])
@login_required
def admin_cancel_ticket(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    ticket = LuckyDrawTicket.query.get_or_404(id)
    series = ticket.series
    
    ticket.status = 'cancelled'
    series.available_tickets += 1  # Return ticket to pool
    db.session.commit()
    
    flash(f'Ticket {ticket.ticket_number} cancelled successfully!', 'success')
    return jsonify({'success': True})

@app.route('/admin/lucky-draw/tickets/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_ticket(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    ticket = LuckyDrawTicket.query.get_or_404(id)
    series = ticket.series
    ticket_number = ticket.ticket_number
    
    # Return ticket to available pool if it was confirmed or pending
    if ticket.status in ['confirmed', 'pending']:
        series.available_tickets += 1
    
    db.session.delete(ticket)
    db.session.commit()
    
    flash(f'Ticket {ticket_number} deleted successfully!', 'success')
    return jsonify({'success': True})

@app.route('/admin/lucky-draw/tickets/view/<int:id>')
@login_required
def admin_view_ticket(id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    ticket = LuckyDrawTicket.query.get_or_404(id)
    
    ticket_data = {
        'ticket_number': ticket.ticket_number,
        'series': ticket.series.series_name,
        'customer_name': ticket.customer_name,
        'customer_email': ticket.customer_email,
        'customer_phone': ticket.customer_phone,
        'customer_address': ticket.customer_address,
        'payment_method': ticket.payment_method,
        'transaction_id': ticket.transaction_id,
        'payment_screenshot': ticket.payment_screenshot,
        'status': ticket.status,
        'purchase_date': ticket.purchase_date.strftime('%d %b %Y %H:%M'),
        'confirmed_date': ticket.confirmed_date.strftime('%d %b %Y %H:%M') if ticket.confirmed_date else None
    }
    
    return jsonify({'success': True, 'ticket': ticket_data})

@app.route('/admin/lucky-draw/payment-settings', methods=['GET', 'POST'])
@login_required
def admin_payment_settings():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    payment_settings = PaymentSettings.query.first()
    if not payment_settings:
        payment_settings = PaymentSettings()
        db.session.add(payment_settings)
        db.session.commit()
    
    if request.method == 'POST':
        payment_settings.upi_id = request.form.get('upi_id', '')
        payment_settings.payment_instructions = request.form.get('payment_instructions', '')
        payment_settings.lucky_draw_description = request.form.get('lucky_draw_description', '')
        
        # Handle QR code upload
        if 'qr_code_image' in request.files:
            file = request.files['qr_code_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"qr_{datetime.now().timestamp()}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                payment_settings.qr_code_image = f"/static/uploads/{filename}"
        
        db.session.commit()
        flash('Payment settings updated successfully!', 'success')
        return redirect(url_for('admin_payment_settings'))
    
    return render_template('admin/payment_settings.html', payment_settings=payment_settings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        if not admin:
            admin = User(
                email=app.config['ADMIN_EMAIL'],
                name='Administrator',
                is_admin=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
        
        # Create default company info if not exists
        company_info = CompanyInfo.query.first()
        if not company_info:
            company_info = CompanyInfo(
                company_name='Sri Shanmukha Harayanaraya Constructions',
                tagline='Building Dreams, Creating Legacies',
                about='We are a leading construction company dedicated to delivering quality projects on time.',
                phone='+1 234 567 890',
                email='info@sshcbuilders.com',
                address='123 Construction Ave, City, State 12345'
            )
            db.session.add(company_info)
        
        db.session.commit()
    
    # Use PORT environment variable for production (Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

