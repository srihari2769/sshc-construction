# Sri Shanmukha Harayanaraya Constructions Website
## Project Summary

### Overview
A complete, production-ready construction company website with a powerful admin panel. Built with Python Flask, PostgreSQL, HTML, CSS, and JavaScript.

---

## ✨ Key Features

### Public Website
- **Modern Design**: Responsive, professional layout optimized for all devices
- **Home Page**: Hero section, featured projects showcase, services overview, client testimonials
- **About Page**: Company story, mission, vision, values, and why choose us section
- **Services Page**: Detailed service offerings with icons and descriptions
- **Projects Portfolio**: Filterable project gallery with categories
- **Project Details**: Individual project pages with complete information
- **Contact Form**: Professional contact form with validation
- **Social Media Integration**: Links to all social platforms

### Admin Panel
- **Secure Authentication**: Login system with password hashing
- **Dashboard**: Real-time statistics and recent activity overview
- **Projects Management**: 
  - Add, edit, delete projects
  - Upload project images
  - Set project as featured
  - Categorize projects
  - Track client info and completion dates
- **Services Management**:
  - Create and manage service offerings
  - Set Font Awesome icons
  - Control display order
  - Toggle active/inactive status
- **Testimonials Management**:
  - Add client testimonials
  - 5-star rating system
  - Upload client photos
  - Manage visibility
- **Contact Inquiries**:
  - View all contact form submissions
  - Update status (new/read/responded)
  - Filter by status
  - View full message details
- **Company Settings**:
  - Update company information
  - Manage contact details
  - Configure social media links
  - Edit about section

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Python Flask 3.0 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Form Handling | Flask-WTF |
| Frontend | HTML5, CSS3, JavaScript |
| Icons | Font Awesome 6.4 |
| Responsive Design | CSS Grid, Flexbox |

---

## 📁 Project Structure

```
sshcbuilders/
│
├── app.py                      # Main Flask application
├── models.py                   # Database models (SQLAlchemy)
├── config.py                   # Configuration settings
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation
├── SETUP.md                   # Quick setup guide
├── run.ps1                    # PowerShell startup script
├── start.bat                  # Windows batch startup file
│
├── static/                    # Static files
│   ├── css/
│   │   ├── style.css         # Public website styles
│   │   └── admin.css         # Admin panel styles
│   ├── js/
│   │   ├── main.js           # Public website JavaScript
│   │   └── admin.js          # Admin panel JavaScript
│   └── uploads/              # Uploaded images storage
│       └── .gitkeep
│
└── templates/                 # HTML templates
    ├── base.html             # Public site base template
    ├── index.html            # Home page
    ├── about.html            # About page
    ├── services.html         # Services listing
    ├── projects.html         # Projects gallery
    ├── project_detail.html   # Single project view
    ├── contact.html          # Contact form
    │
    └── admin/                # Admin panel templates
        ├── base.html         # Admin base template
        ├── login.html        # Admin login
        ├── dashboard.html    # Admin dashboard
        ├── projects.html     # Projects management
        ├── project_form.html # Add/Edit project
        ├── services.html     # Services management
        ├── service_form.html # Add/Edit service
        ├── testimonials.html # Testimonials list
        ├── testimonial_form.html
        ├── contacts.html     # Contact inquiries
        └── settings.html     # Company settings
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip package manager

### Installation (5 Steps)

1. **Setup Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Create Database**
   ```sql
   CREATE DATABASE sshc_construction;
   ```

4. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update database credentials
   - Set a secure SECRET_KEY

5. **Initialize Database**
   ```powershell
   python init_db.py
   ```

### Run Application

**Option 1**: Double-click `start.bat`

**Option 2**: PowerShell
```powershell
.\run.ps1
```

**Option 3**: Manual
```powershell
python app.py
```

### Access
- **Public Site**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
- **Default Admin**: admin@sshcbuilders.com / admin123

---

## 📊 Database Schema

### Tables

| Table | Description | Key Fields |
|-------|-------------|------------|
| users | Admin users | id, email, password_hash, is_admin |
| projects | Construction projects | id, title, description, category, image_url, featured |
| services | Service offerings | id, title, description, icon, order, active |
| testimonials | Client reviews | id, client_name, content, rating, active |
| contacts | Contact inquiries | id, name, email, message, status |
| company_info | Company details | id, company_name, about, phone, email, social_links |

---

## 🎨 Customization

### Change Theme Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #ff6b35;      /* Main brand color */
    --secondary-color: #004e89;    /* Secondary color */
    --dark-color: #1a1a2e;         /* Dark elements */
}
```

### Update Company Info
1. Login to admin panel
2. Navigate to Settings
3. Update all company information
4. Save changes

### Add Content
All content management is done through the admin panel:
- No coding required
- Upload images directly
- WYSIWYG content editing

---

## 🔒 Security Features

- ✓ Password hashing with Werkzeug
- ✓ SQL injection protection via SQLAlchemy ORM
- ✓ CSRF protection with Flask-WTF
- ✓ File upload validation
- ✓ Session management
- ✓ Admin-only route protection

---

## 📱 Responsive Design

- ✓ Mobile-first approach
- ✓ Tablet optimization
- ✓ Desktop layouts
- ✓ Touch-friendly navigation
- ✓ Optimized images

---

## 🎯 Features Highlights

### For Visitors
- Easy navigation
- Beautiful project showcase
- Quick contact form
- Social media integration
- Fast loading times

### For Administrators
- Intuitive dashboard
- Simple content management
- No technical knowledge needed
- Real-time statistics
- Efficient workflow

---

## 📈 Sample Data Included

The `init_db.py` script includes:
- 6 Sample projects (residential, commercial, industrial)
- 6 Core services
- 6 Client testimonials
- Complete company information
- Admin user account

---

## 🔧 Maintenance

### Backup Database
```powershell
pg_dump sshc_construction > backup.sql
```

### Update Dependencies
```powershell
pip install --upgrade -r requirements.txt
```

### Reset Admin Password
```python
from app import app, db
from models import User

with app.app_context():
    admin = User.query.filter_by(email='admin@sshcbuilders.com').first()
    admin.set_password('newpassword')
    db.session.commit()
```

---

## 📝 Development Notes

### Built With Best Practices
- MVC architecture pattern
- RESTful routing
- Clean code principles
- Security-first approach
- Scalable structure

### Ready for Production
- Environment-based configuration
- Production-ready file structure
- Error handling
- Logging capabilities
- Database migrations support

---

## 🆘 Support & Troubleshooting

Common issues and solutions are documented in:
- `README.md` - Complete documentation
- `SETUP.md` - Quick setup guide

For database connection issues, verify:
1. PostgreSQL is running
2. Database exists
3. Credentials in `.env` are correct

---

## 📄 License

Proprietary - All rights reserved by Sri Shanmukha Harayanaraya Constructions

---

## ✅ Project Checklist

- [x] Backend application (Flask)
- [x] Database models (SQLAlchemy)
- [x] Admin authentication
- [x] Public website templates
- [x] Admin panel templates
- [x] Responsive CSS styling
- [x] JavaScript functionality
- [x] Image upload support
- [x] Contact form handling
- [x] Sample data seeding
- [x] Documentation
- [x] Setup scripts
- [x] Security features

---

**🎉 The website is complete and ready to use!**

Start building your online presence today with this professional construction website platform.
