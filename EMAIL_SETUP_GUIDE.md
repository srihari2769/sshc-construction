# Email Setup Guide for Lucky Draw Notifications

## Gmail Setup (Recommended)

### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com
2. Click on "Security" in the left menu
3. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Click "Generate"
4. Copy the 16-character password (it will look like: `xxxx xxxx xxxx xxxx`)

### Step 3: Update .env File
Open `.env` file and update these lines:

```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  (the app password from step 2)
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 4: Restart the Server
Stop the Flask server (Ctrl+C) and restart it:
```bash
.\venv\Scripts\python.exe app.py
```

## Testing Email

1. Go to Lucky Draw page and purchase a test ticket
2. Go to Admin Panel > Lucky Draw > Tickets
3. Click "Confirm" on a pending ticket
4. Check if email was sent (check terminal for "Email sent to..." message)
5. Check customer's email inbox (and spam folder)

## Troubleshooting

### "SMTP Authentication Error"
- Make sure you're using App Password, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check if MAIL_USERNAME and MAIL_PASSWORD are correct in .env

### "Connection Refused"
- Check MAIL_SERVER is set to `smtp.gmail.com`
- Check MAIL_PORT is set to `587`
- Verify MAIL_USE_TLS is set to `true`

### Email Going to Spam
- Add your sender email to the recipient's contacts
- Check email content is not triggering spam filters
- Verify SPF/DKIM records if using custom domain

## Alternative Email Providers

### Outlook/Hotmail
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Yahoo
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Custom SMTP Server
Update the configuration according to your email provider's SMTP settings.

## Email Template

The confirmation email includes:
- Ticket number in large, bold text
- Customer details
- Series information
- Purchase and confirmation dates
- Beautiful HTML design with gradient header
- Company name from database

## Security Notes

⚠️ **NEVER commit your .env file to Git/GitHub**
- The .env file contains sensitive passwords
- It's already in .gitignore
- Share email credentials securely if needed

---

**Status**: Email system is ready to use once credentials are configured!
