# Sri Shanmukha Harayanaraya Constructions Website

A complete construction company website with an admin panel built using Python Flask, HTML, CSS, JavaScript, and PostgreSQL.

## Features

### Public Website
- **Home Page**: Hero section, featured projects, services, testimonials
- **About Page**: Company information, mission, vision, and values
- **Services Page**: Detailed list of construction services
- **Projects Page**: Portfolio with filterable categories
- **Contact Page**: Contact form with validation

### Admin Panel
- **Dashboard**: Overview statistics and recent contacts
- **Projects Management**: Add, edit, delete, and feature projects
- **Services Management**: Manage service offerings
- **Testimonials Management**: Control client testimonials
- **Contacts Management**: View and manage contact inquiries
- **Company Settings**: Update company information and social media links

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd c:\Users\psrih\Documents\sshcbuilders
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Setup PostgreSQL Database

#### Create Database
Open PostgreSQL command line (psql) or pgAdmin and run:

```sql
CREATE DATABASE sshc_construction;
```

#### Create Database User (Optional)
```sql
CREATE USER sshc_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sshc_construction TO sshc_user;
```

### 6. Configure Environment Variables

Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

Edit `.env` file and update the following:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-to-something-random
FLASK_APP=app.py
FLASK_ENV=development

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/sshc_construction

# Admin Credentials (default - change after first login)
ADMIN_EMAIL=admin@sshcbuilders.com
ADMIN_PASSWORD=admin123

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

**Important**: Replace:
- `username` with your PostgreSQL username (default: `postgres`)
- `password` with your PostgreSQL password
- `your-secret-key-here-change-this` with a random secret key

### 7. Create Upload Directory

```powershell
New-Item -ItemType Directory -Path static\uploads -Force
```

### 8. Initialize Database

The application will automatically create all database tables on first run. Simply start the application:

```powershell
python app.py
```

The first time you run the app, it will:
- Create all database tables
- Create a default admin user
- Set up initial company information

### 9. Access the Application

- **Public Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

**Default Admin Credentials**:
- Email: `admin@sshcbuilders.com`
- Password: `admin123`

**⚠️ IMPORTANT**: Change the admin password immediately after first login!

## Project Structure

```
sshcbuilders/
├── static/
│   ├── css/
│   │   ├── style.css          # Public website styles
│   │   └── admin.css          # Admin panel styles
│   ├── js/
│   │   ├── main.js            # Public website scripts
│   │   └── admin.js           # Admin panel scripts
│   └── uploads/               # Uploaded images
├── templates/
│   ├── admin/
│   │   ├── base.html          # Admin base template
│   │   ├── login.html         # Admin login
│   │   ├── dashboard.html     # Admin dashboard
│   │   ├── projects.html      # Projects management
│   │   ├── project_form.html  # Add/Edit project
│   │   ├── services.html      # Services management
│   │   ├── service_form.html  # Add/Edit service
│   │   ├── testimonials.html  # Testimonials management
│   │   ├── testimonial_form.html
│   │   ├── contacts.html      # Contact inquiries
│   │   └── settings.html      # Company settings
│   ├── base.html              # Public base template
│   ├── index.html             # Home page
│   ├── about.html             # About page
│   ├── services.html          # Services page
│   ├── projects.html          # Projects listing
│   ├── project_detail.html    # Project details
│   └── contact.html           # Contact page
├── app.py                      # Main application
├── models.py                   # Database models
├── config.py                   # Configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .env.example               # Environment example
└── README.md                  # This file
```

## Usage

### Running the Application

Development mode:
```powershell
python app.py
```

Production mode (use a production server like Gunicorn):
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Admin Panel Guide

1. **Login**: Navigate to `/admin/login` and use admin credentials
2. **Dashboard**: View statistics and recent activities
3. **Add Projects**: Click "Projects" → "Add New Project"
   - Upload project images
   - Set category, location, client info
   - Mark as featured to show on home page
4. **Add Services**: Click "Services" → "Add New Service"
   - Choose Font Awesome icon
   - Set display order
5. **Manage Testimonials**: Add client reviews with ratings
6. **View Contacts**: Monitor and respond to contact form submissions
7. **Update Settings**: Configure company info and social media links

### Customization

#### Update Company Information
- Login to admin panel
- Go to Settings
- Update company name, tagline, contact info, and social media links

#### Change Theme Colors
Edit `static/css/style.css` and modify CSS variables:
```css
:root {
    --primary-color: #ff6b35;
    --secondary-color: #004e89;
    --dark-color: #1a1a2e;
}
```

#### Add More Services/Projects
Use the admin panel to add content without touching code.

## Database Schema

### Tables
- **users**: Admin users with authentication
- **projects**: Construction projects portfolio
- **services**: Service offerings
- **testimonials**: Client testimonials
- **contacts**: Contact form submissions
- **company_info**: Company information and settings

## Security Notes

1. **Change Default Credentials**: Immediately after first login
2. **Use Strong Secret Key**: Generate a random secret key for production
3. **HTTPS**: Use HTTPS in production
4. **Database Backups**: Regular backups of PostgreSQL database
5. **File Upload Security**: Only allowed file types can be uploaded

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Verify database credentials in `.env`
- Check if database exists: `psql -l`

### Import Error
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### File Upload Issues
- Check `static/uploads` directory exists and is writable
- Verify `MAX_CONTENT_LENGTH` in config

### Admin Can't Login
- Verify admin user was created (check database)
- Reset password using Python shell:
```python
from app import app, db
from models import User

with app.app_context():
    admin = User.query.filter_by(email='admin@sshcbuilders.com').first()
    admin.set_password('newpassword')
    db.session.commit()
```

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add templates in `templates/`
3. Update models in `models.py` if needed
4. Run migrations if database schema changes

### Database Migrations
For schema changes, use Flask-Migrate:
```powershell
pip install Flask-Migrate
```

## Support

For issues or questions, please contact the development team.

## License

Proprietary - All rights reserved by Sri Shanmukha Harayanaraya Constructions

## Credits

Developed for Sri Shanmukha Harayanaraya Constructions
