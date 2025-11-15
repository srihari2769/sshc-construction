# PostgreSQL Installation Guide for Windows

## Quick Install (Recommended)

### Step 1: Download PostgreSQL

Visit: **https://www.postgresql.org/download/windows/**

Click "Download the installer" → Select **Windows x86-64** (latest version 15 or 16)

### Step 2: Run the Installer

1. **Double-click** the downloaded `.exe` file
2. Click **Next** through the welcome screen
3. **Installation Directory**: Keep default (`C:\Program Files\PostgreSQL\15`)
4. **Select Components**: Check ALL boxes:
   - ✓ PostgreSQL Server
   - ✓ pgAdmin 4
   - ✓ Stack Builder
   - ✓ Command Line Tools
5. **Data Directory**: Keep default
6. **Password**: Enter `postgres` (or choose your own - must update .env file)
7. **Port**: Keep default `5432`
8. **Locale**: Keep default
9. Click **Next** and **Finish**

### Step 3: Verify Installation

Open a **NEW PowerShell window**:

```powershell
psql --version
```

Expected output: `psql (PostgreSQL) 15.x` or `psql (PostgreSQL) 16.x`

### Step 4: Test Connection

```powershell
# Connect to PostgreSQL
psql -U postgres

# You'll be prompted for password (enter: postgres)
# If successful, you'll see: postgres=#

# Type \q to exit
\q
```

## Create the Database

### Option A: Using pgAdmin (Easiest)

1. Open **pgAdmin 4** from Start menu
2. Enter master password if prompted
3. Expand **Servers** → **PostgreSQL 15** (or 16)
4. Enter password: `postgres`
5. Right-click **Databases** → **Create** → **Database...**
6. Database name: `sshc_construction`
7. Click **Save**

### Option B: Using Command Line

```powershell
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sshc_construction;

# Verify
\l

# Exit
\q
```

## Update .env File (If Needed)

If you used a different password, edit `.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/sshc_construction
```

Replace `YOUR_PASSWORD` with your actual password.

## Troubleshooting

### "psql is not recognized"

**Solution**: Add PostgreSQL to PATH

1. Open **System Environment Variables**:
   - Press `Win + R`
   - Type: `sysdm.cpl`
   - Go to **Advanced** tab → **Environment Variables**

2. Under **System variables**, find and edit **Path**

3. Click **New** and add:
   ```
   C:\Program Files\PostgreSQL\15\bin
   ```
   (Adjust version number if different)

4. Click **OK** on all windows

5. **Restart PowerShell** and try again

### PostgreSQL service not starting

1. Open **Services** (`Win + R` → `services.msc`)
2. Find **postgresql-x64-15** (or your version)
3. Right-click → **Start**
4. Set **Startup type** to **Automatic**

### Connection refused

1. Check service is running (see above)
2. Verify port 5432 is not blocked by firewall
3. Check `pg_hba.conf` file (should allow local connections)

### Can't remember password

1. Edit `pg_hba.conf`:
   - Location: `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`
   - Change `md5` to `trust` for local connections
   - Restart PostgreSQL service
2. Connect and change password:
   ```sql
   ALTER USER postgres PASSWORD 'new_password';
   ```
3. Change `trust` back to `md5` in `pg_hba.conf`
4. Restart service again

## Alternative: PostgreSQL via Stack Builder

If installer fails, use Stack Builder:

1. Run **Stack Builder** from Start menu
2. Select your PostgreSQL installation
3. Follow wizard to install PostgreSQL server
4. Same configuration as above

## Ready to Continue?

Once PostgreSQL is installed and database is created, return to `NEXT_STEPS.md` and proceed to **Step 3: Initialize Database**.
