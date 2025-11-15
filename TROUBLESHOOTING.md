# Troubleshooting Guide
## SSHC Construction Website

This guide helps you solve common issues when setting up and running the website.

---

## Setup Issues

### ❌ Virtual Environment Won't Activate

**Problem**: `.\venv\Scripts\Activate.ps1` shows execution policy error

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

---

### ❌ pip install fails

**Problem**: `pip install -r requirements.txt` shows errors

**Solutions**:

1. **Update pip**:
   ```powershell
   python -m pip install --upgrade pip
   ```

2. **Install Visual C++ Build Tools** (if needed):
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++"

3. **Try installing packages individually**:
   ```powershell
   pip install Flask
   pip install Flask-SQLAlchemy
   pip install Flask-Login
   ```

---

## Database Issues

### ❌ Database Connection Failed

**Problem**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions**:

1. **Check PostgreSQL is running**:
   - Open Services (services.msc)
   - Find "postgresql-x64-XX"
   - Ensure it's running

2. **Verify database exists**:
   ```sql
   -- In psql or pgAdmin
   \l  -- List all databases
   ```

3. **Check credentials in .env**:
   ```env
   DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/sshc_construction
   ```
   - Replace USERNAME with your PostgreSQL username (usually "postgres")
   - Replace PASSWORD with your PostgreSQL password

4. **Test connection**:
   ```powershell
   psql -U postgres -d sshc_construction
   ```

---

### ❌ Database Does Not Exist

**Problem**: `FATAL: database "sshc_construction" does not exist`

**Solution**:

Open pgAdmin or psql and create the database:
```sql
CREATE DATABASE sshc_construction;
```

Or use PowerShell:
```powershell
psql -U postgres -c "CREATE DATABASE sshc_construction;"
```

---

### ❌ Permission Denied

**Problem**: `FATAL: password authentication failed for user "postgres"`

**Solutions**:

1. **Reset PostgreSQL password**:
   - Open pgAdmin
   - Right-click on PostgreSQL server
   - Select "Properties" → "Connection"
   - Update password

2. **Update .env file** with new password:
   ```env
   DATABASE_URL=postgresql://postgres:NEW_PASSWORD@localhost:5432/sshc_construction
   ```

---

## Application Issues

### ❌ ModuleNotFoundError

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:

1. **Ensure virtual environment is activated**:
   - You should see `(venv)` in your terminal prompt
   
2. **If not activated**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Reinstall dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

### ❌ Import Error: app

**Problem**: `ImportError: cannot import name 'app'`

**Solution**:

Make sure you're in the project directory:
```powershell
cd c:\Users\psrih\Documents\sshcbuilders
```

---

### ❌ Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solutions**:

1. **Find process using port 5000**:
   ```powershell
   netstat -ano | findstr :5000
   ```

2. **Kill the process**:
   ```powershell
   taskkill /PID <process_id> /F
   ```

3. **Or use a different port** in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```

---

### ❌ Admin Can't Login

**Problem**: Login fails with correct credentials

**Solutions**:

1. **Verify admin user exists**:
   ```python
   python
   >>> from app import app, db
   >>> from models import User
   >>> with app.app_context():
   ...     admin = User.query.filter_by(email='admin@sshcbuilders.com').first()
   ...     print(admin)
   ```

2. **If no admin exists, create one**:
   ```python
   python init_db.py
   ```

3. **Reset admin password**:
   ```python
   python
   >>> from app import app, db
   >>> from models import User
   >>> with app.app_context():
   ...     admin = User.query.filter_by(email='admin@sshcbuilders.com').first()
   ...     admin.set_password('admin123')
   ...     db.session.commit()
   ```

---

## File Upload Issues

### ❌ File Upload Fails

**Problem**: Images won't upload through admin panel

**Solutions**:

1. **Check upload directory exists**:
   ```powershell
   New-Item -ItemType Directory -Path static\uploads -Force
   ```

2. **Check file size** (max 16MB by default)

3. **Verify file type** (only: png, jpg, jpeg, gif, pdf)

4. **Check permissions**:
   - Ensure `static/uploads` folder is writable

---

## Runtime Errors

### ❌ Template Not Found

**Problem**: `jinja2.exceptions.TemplateNotFound`

**Solution**:

1. **Verify file exists** in correct location:
   ```
   templates/
   ├── admin/
   │   └── dashboard.html
   └── index.html
   ```

2. **Check file name matches** route exactly

---

### ❌ Static Files Not Loading

**Problem**: CSS/JS files not loading (404 errors)

**Solutions**:

1. **Check file paths** in templates:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
   ```

2. **Verify files exist**:
   ```
   static/
   ├── css/
   │   ├── style.css
   │   └── admin.css
   └── js/
       ├── main.js
       └── admin.js
   ```

3. **Clear browser cache**: Ctrl + Shift + R

---

## Performance Issues

### ❌ Website Loads Slowly

**Solutions**:

1. **Check database queries** in console

2. **Optimize images**:
   - Resize large images before upload
   - Use appropriate formats (JPEG for photos, PNG for graphics)

3. **Enable caching** (for production):
   ```python
   # In config.py
   SEND_FILE_MAX_AGE_DEFAULT = 31536000
   ```

---

## Development Issues

### ❌ Changes Not Reflecting

**Problem**: Code changes don't show up

**Solutions**:

1. **Restart Flask server**:
   - Press Ctrl+C to stop
   - Run `python app.py` again

2. **Hard refresh browser**:
   - Ctrl + Shift + R

3. **Check debug mode enabled**:
   ```python
   # In app.py
   app.run(debug=True)
   ```

---

## Database Reset

### Need to Start Fresh?

**Complete database reset**:

1. **Drop database**:
   ```sql
   DROP DATABASE sshc_construction;
   CREATE DATABASE sshc_construction;
   ```

2. **Reinitialize**:
   ```powershell
   python init_db.py
   ```

---

## Getting Help

### Still Having Issues?

1. **Check error messages carefully**
   - Read the full error trace
   - Google the specific error message

2. **Verify all steps in SETUP.md**

3. **Check logs**:
   - Look at terminal output
   - Check browser console (F12)

4. **Review documentation**:
   - README.md - Full documentation
   - SETUP.md - Setup guide
   - PROJECT_SUMMARY.md - Overview

---

## Common Command Reference

### PowerShell Commands
```powershell
# Navigate to project
cd c:\Users\psrih\Documents\sshcbuilders

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Run application
python app.py

# Initialize database
python init_db.py
```

### PostgreSQL Commands
```sql
-- List databases
\l

-- Connect to database
\c sshc_construction

-- List tables
\dt

-- View table structure
\d users

-- View all users
SELECT * FROM users;
```

---

## Environment Variables Check

Verify your `.env` file contains:

```env
SECRET_KEY=<random-string>
DATABASE_URL=postgresql://username:password@localhost:5432/sshc_construction
ADMIN_EMAIL=admin@sshcbuilders.com
ADMIN_PASSWORD=admin123
```

Replace:
- `username` → your PostgreSQL username
- `password` → your PostgreSQL password

---

## Quick Diagnostic

Run this to check your setup:

```powershell
# Check Python version
python --version

# Check PostgreSQL
psql --version

# Check if database exists
psql -U postgres -l | findstr sshc_construction

# Check virtual environment
Get-Command python | Select-Object Source
```

---

**💡 Pro Tip**: Most issues are solved by:
1. Ensuring virtual environment is activated
2. Checking database credentials
3. Verifying PostgreSQL is running
4. Restarting the application

If all else fails, start fresh with a new virtual environment and database!
