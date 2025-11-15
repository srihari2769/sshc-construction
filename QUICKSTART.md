# 🚀 Quick Start - SSHC Construction Website

## Get Started in 5 Minutes!

### Step 1: Open PowerShell in Project Folder
```powershell
cd c:\Users\psrih\Documents\sshcbuilders
```

### Step 2: Run the Easy Startup Script
**Option A - Double Click**: 
- Just double-click `start.bat` file

**Option B - PowerShell**:
```powershell
.\run.ps1
```

The script will:
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Set up configuration
- ✓ Initialize database with sample data
- ✓ Start the website

### Step 3: Update Database Credentials

When prompted, edit the `.env` file and change:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/sshc_construction
```
Replace `YOUR_PASSWORD` with your PostgreSQL password.

### Step 4: Create PostgreSQL Database

Open pgAdmin or psql and run:
```sql
CREATE DATABASE sshc_construction;
```

### Step 5: Access Your Website! 🎉

- **Public Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

**Login with:**
- Email: `admin@sshcbuilders.com`
- Password: `admin123`

---

## ⚡ Manual Setup (If Needed)

If the script doesn't work, follow these manual steps:

### 1. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Requirements
```powershell
pip install -r requirements.txt
```

### 3. Setup Database
```sql
-- In PostgreSQL
CREATE DATABASE sshc_construction;
```

### 4. Configure .env
Copy `.env.example` to `.env` and update database URL.

### 5. Initialize Database
```powershell
python init_db.py
```

### 6. Run Application
```powershell
python app.py
```

---

## 📝 What's Included?

✅ Complete public website (Home, About, Services, Projects, Contact)  
✅ Full-featured admin panel  
✅ 6 sample projects  
✅ 6 core services  
✅ 6 client testimonials  
✅ Responsive design  
✅ Image upload support  
✅ Contact form management  
✅ Company settings  

---

## 🎯 First Steps After Login

1. **Change Admin Password** (Important!)
2. Go to **Settings** → Update company information
3. Go to **Projects** → Add your real projects (delete samples)
4. Go to **Services** → Customize your services
5. Go to **Testimonials** → Add real client reviews
6. Check **Contacts** to see form submissions

---

## 📚 Need Help?

- **Setup Guide**: `SETUP.md`
- **Full Documentation**: `README.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

---

## 🎨 Customize Your Website

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #ff6b35;     /* Your brand color */
    --secondary-color: #004e89;   /* Accent color */
}
```

### Update Logo/Company Name
Go to Admin Panel → Settings

---

## ⚠️ Important Notes

1. **PostgreSQL must be installed and running**
2. **Python 3.8+ required**
3. **Change default admin password after first login**
4. **Update `.env` with your database credentials**

---

## 🛑 Common Issues

**Issue**: Virtual environment won't activate  
**Fix**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue**: Database connection error  
**Fix**: Check PostgreSQL is running and credentials in `.env` are correct

**Issue**: Module not found  
**Fix**: Make sure virtual environment is activated (you see `(venv)` in terminal)

---

## ✨ You're All Set!

Your construction website is ready to go. Start customizing it through the admin panel!

**Happy Building! 🏗️**
