# Deployment Guide - Render.com

## ✅ Files Created for Deployment

1. **requirements.txt** - Python dependencies including Gunicorn
2. **build.sh** - Build script for Render
3. **render.yaml** - Render configuration (optional, for Blueprint)

---

## 📋 Deployment Steps

### **Step 1: Push Code to GitHub**

1. Create a new repository on GitHub (e.g., `sshc-construction`)
2. Initialize git in your project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/sshc-construction.git
   git push -u origin main
   ```

3. **Create `.gitignore` file** (if not exists):
   ```
   venv/
   __pycache__/
   *.pyc
   .env
   *.db
   static/uploads/*
   !static/uploads/.gitkeep
   ```

---

### **Step 2: Create Render Account**

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

---

### **Step 3: Create PostgreSQL Database**

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `sshc-postgres`
   - **Database**: `sshc_construction`
   - **User**: `sshc_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (1GB storage, expires in 90 days) or Starter $7/month
3. Click **"Create Database"**
4. **SAVE** the Internal Database URL (you'll need it)

---

### **Step 4: Create Web Service**

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

   **Basic Settings:**
   - **Name**: `sshc-construction`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free or Starter ($7/month)

4. Click **"Advanced"** and add Environment Variables:

   ```
   SECRET_KEY = [Generate a random secret key]
   FLASK_ENV = production
   DATABASE_URL = [Paste Internal Database URL from Step 3]
   
   MAIL_SERVER = smtp.gmail.com
   MAIL_PORT = 587
   MAIL_USE_TLS = true
   MAIL_USERNAME = srimeerastudio@gmail.com
   MAIL_PASSWORD = ckve ypwh xuuu ctjd
   MAIL_DEFAULT_SENDER = srimeerastudio@gmail.com
   
   ADMIN_EMAIL = admin@sshcbuilders.com
   ADMIN_PASSWORD = admin123
   ```

5. Click **"Create Web Service"**

---

### **Step 5: Wait for Deployment**

- Render will automatically:
  1. Clone your repository
  2. Run `build.sh` (install dependencies + setup database)
  3. Start Gunicorn server
  
- Watch the logs for any errors
- First deployment takes 5-10 minutes

---

### **Step 6: Test Your Website**

1. Once deployed, Render gives you a URL like:
   `https://sshc-construction.onrender.com`

2. Visit the URL and test:
   - ✅ Homepage loads
   - ✅ Admin login works
   - ✅ Lucky Draw system works
   - ✅ Email notifications work

---

## 🌐 Step 7: Connect Custom Domain (Namecheap/Hostinger)

### **On Render Dashboard:**

1. Go to your web service → **"Settings"** → **"Custom Domain"**
2. Click **"Add Custom Domain"**
3. Enter your domain: `www.yourdomain.com` or `yourdomain.com`
4. Render will show you DNS records to add

### **On Namecheap:**

1. Login to Namecheap
2. Go to **Domain List** → **Manage** → **Advanced DNS**
3. Add these records:

   **For `www.yourdomain.com`:**
   ```
   Type: CNAME Record
   Host: www
   Value: sshc-construction.onrender.com
   TTL: Automatic
   ```

   **For root domain `yourdomain.com`:**
   ```
   Type: A Record
   Host: @
   Value: [IP provided by Render]
   TTL: Automatic
   ```

4. Save changes

### **On Hostinger:**

1. Login to Hostinger
2. Go to **Domains** → **DNS/Name Servers** → **Manage**
3. Add the same CNAME and A records as above
4. Save changes

### **Back on Render:**

1. Wait for DNS propagation (5 minutes to 48 hours, usually ~1 hour)
2. Click **"Verify DNS Configuration"**
3. Render will automatically provision **FREE SSL certificate** (HTTPS)

---

## 🔧 Important Notes

### **File Uploads:**

Render's free tier has **ephemeral storage** - uploaded files disappear on restart!

**Solutions:**
1. **Use Cloudinary** (Free tier: 25GB):
   - Sign up at cloudinary.com
   - Store images/videos there instead of local filesystem
   
2. **Use AWS S3** or **DigitalOcean Spaces**

3. **Upgrade to Render Persistent Disk** ($1/month for 1GB)

### **Database Backups:**

- Render Free PostgreSQL expires after 90 days
- **Paid plan ($7/month)** includes automatic backups
- Or manually backup using:
  ```bash
  pg_dump [DATABASE_URL] > backup.sql
  ```

### **Environment Variables:**

- NEVER commit `.env` file to GitHub
- Always add sensitive data in Render Dashboard → Environment Variables

---

## 📊 Monitoring & Logs

1. **View Logs**: Render Dashboard → Your Service → Logs
2. **Metrics**: Monitor CPU, Memory, Request count
3. **Alerts**: Set up email alerts for downtime

---

## 🚀 Update Deployment

To deploy changes:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically redeploy! 🎉

---

## 💰 Cost Summary

| Service | Free Tier | Paid Plan |
|---------|-----------|-----------|
| Web Service | ✅ 750 hours/month | $7/month |
| PostgreSQL | ✅ 90 days, 1GB | $7/month |
| SSL Certificate | ✅ Free | ✅ Free |
| Custom Domain | ✅ Free | ✅ Free |
| Bandwidth | ✅ 100GB/month | Unlimited |

**Recommended**: Start with Free, upgrade when needed ($14/month for both)

---

## 🆘 Troubleshooting

### Build Fails:
- Check `build.sh` has execute permissions
- Verify all packages in `requirements.txt` are correct
- Check build logs in Render dashboard

### Database Connection Error:
- Verify `DATABASE_URL` is set correctly
- Check database is in same region as web service
- Ensure database is running

### Static Files Not Loading:
- Verify `static/` folder is in repository
- Check CSS/JS paths are correct
- Clear browser cache

### Email Not Sending:
- Verify Gmail App Password is correct
- Check `MAIL_USERNAME` and `MAIL_PASSWORD` environment variables
- Test email from Render logs

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Status Page**: https://status.render.com

---

**🎉 Your website is now live on Render.com with your custom domain!**
