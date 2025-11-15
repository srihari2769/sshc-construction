# Quick Setup Guide for SSHC Construction Website

## Prerequisites
✓ Python 3.8+ installed
✓ PostgreSQL 12+ installed and running
✓ Internet connection (for downloading packages)

## Setup Steps

### 1. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database
Open pgAdmin or psql and run:
```sql
CREATE DATABASE sshc_construction;
```

### 4. Configure Environment
1. Copy `.env.example` to `.env`
2. Edit `.env` and update:
   - `DATABASE_URL`: Use your PostgreSQL credentials
   - `SECRET_KEY`: Use a random secret key
   - Keep default admin credentials for now

Example DATABASE_URL:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sshc_construction
```

### 5. Initialize Database with Sample Data
```powershell
python init_db.py
```

### 6. Run the Application
```powershell
python app.py
```

### 7. Access the Website
- Public Site: http://localhost:5000
- Admin Panel: http://localhost:5000/admin/login

**Admin Login:**
- Email: admin@sshcbuilders.com
- Password: admin123

## Next Steps
1. Login to admin panel
2. Change admin password in database or code
3. Update company information in Settings
4. Add your own projects, services, and testimonials
5. Customize colors in `static/css/style.css`

## Common Issues

**Virtual environment activation error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Database connection error:**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env file
- Ensure database exists

**Module not found error:**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

## File Structure
```
sshcbuilders/
├── app.py              # Main application
├── models.py           # Database models
├── config.py           # Configuration
├── init_db.py          # Database initialization
├── requirements.txt    # Dependencies
├── .env               # Your settings (create this)
├── static/            # CSS, JS, images
├── templates/         # HTML templates
└── README.md          # Full documentation
```

## Support
See README.md for detailed documentation and troubleshooting.
