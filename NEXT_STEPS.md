# 🚀 Next Steps - Complete Setup Guide

## ✅ Completed So Far
- ✓ Virtual environment created
- ✓ All Python dependencies installed (Flask, SQLAlchemy, etc.)
- ✓ All website files created (templates, CSS, JavaScript)
- ✓ Configuration files ready (.env, config.py)

---

## 📋 Remaining Steps

### Step 1: Install PostgreSQL (REQUIRED)

**PostgreSQL is not currently installed on your system.** You need to install it:

#### Download & Install:
1. Visit: https://www.postgresql.org/download/windows/
2. Download the PostgreSQL installer (version 15 or 16 recommended)
3. Run the installer with these settings:
   - **Port**: 5432 (default)
   - **Superuser Password**: `postgres` (or change .env file to match)
   - **Components**: Select all (PostgreSQL Server, pgAdmin, Command Line Tools)

#### Verify Installation:
Open a new PowerShell window and run:
```powershell
psql --version
```
You should see: `psql (PostgreSQL) 15.x` or similar

---

### Step 2: Create the Database

After PostgreSQL is installed, open **pgAdmin** or **SQL Shell (psql)**:

#### Option A: Using pgAdmin (GUI)
1. Open pgAdmin
2. Connect to PostgreSQL server (password: `postgres`)
3. Right-click "Databases" → "Create" → "Database"
4. Database name: `sshc_construction`
5. Click "Save"

#### Option B: Using psql (Command Line)
```powershell
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sshc_construction;

# Exit
\q
```

---

### Step 3: Initialize Database with Sample Data

Run the initialization script:

```powershell
cd c:\Users\psrih\Documents\sshcbuilders
.\venv\Scripts\python.exe init_db.py
```

This will create all tables and populate them with:
- 1 Admin user (admin@sshcbuilders.com / admin123)
- 6 Sample projects
- 6 Services
- 6 Testimonials
- Company information

---

### Step 4: Start the Application

#### Method 1: Using PowerShell Script
```powershell
.\run.ps1
```

#### Method 2: Using Batch File
```cmd
start.bat
```

#### Method 3: Manual Start
```powershell
.\venv\Scripts\python.exe app.py
```

---

## 🌐 Access the Website

Once the app starts, you'll see:
```
 * Running on http://127.0.0.1:5000
```

### Public Website:
- **Home**: http://localhost:5000/
- **About**: http://localhost:5000/about
- **Services**: http://localhost:5000/services
- **Projects**: http://localhost:5000/projects
- **Contact**: http://localhost:5000/contact

### Admin Panel:
- **Login**: http://localhost:5000/admin/login
  - Email: `admin@sshcbuilders.com`
  - Password: `admin123`
- **Dashboard**: http://localhost:5000/admin/dashboard

---

## 🔧 Troubleshooting

### If PostgreSQL installation fails:
1. Try the EDB installer: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Or use the Stack Builder tool
3. Ensure Windows user has admin rights

### If database connection fails:
1. Check PostgreSQL service is running:
   ```powershell
   Get-Service -Name postgresql*
   ```
2. Verify .env file has correct credentials:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sshc_construction
   ```
3. Test connection with pgAdmin

### If port 5000 is already in use:
Edit `.env` file and add:
```
FLASK_RUN_PORT=5001
```
Then access at http://localhost:5001/

---

## 🔐 Important Security Notes

**BEFORE DEPLOYING TO PRODUCTION:**

1. **Change Admin Password** (immediately after first login)
2. **Update SECRET_KEY** in `.env`:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
   Copy the output to .env file

3. **Change Database Password** (if deploying publicly)

4. **Set Debug Mode to False** in production:
   ```
   FLASK_DEBUG=False
   ```

---

## 📚 Quick Reference

### Stop the Application:
Press `Ctrl+C` in the terminal

### Restart After Code Changes:
```powershell
.\venv\Scripts\python.exe app.py
```

### View Database Tables:
```powershell
psql -U postgres -d sshc_construction
\dt  # List all tables
SELECT * FROM "user";  # View users
SELECT * FROM project;  # View projects
```

### Add More Sample Data:
Edit `init_db.py` and run it again

---

## 🎯 Current Status

| Task | Status |
|------|--------|
| Project Structure | ✅ Complete |
| Python Dependencies | ✅ Installed |
| PostgreSQL | ⏳ **Needs Installation** |
| Database Creation | ⏳ Pending |
| Database Init | ⏳ Pending |
| First Run | ⏳ Pending |

---

## 💡 What's Next?

1. **Right Now**: Install PostgreSQL (Step 1 above)
2. **Then**: Create database (Step 2)
3. **Then**: Initialize with sample data (Step 3)
4. **Finally**: Start the application (Step 4)

**Total Time Needed**: ~15-20 minutes (mostly PostgreSQL installation)

---

## 📞 Need Help?

See `TROUBLESHOOTING.md` for common issues and solutions.

---

**Ready to continue?** Install PostgreSQL and let me know when it's done! 🚀
