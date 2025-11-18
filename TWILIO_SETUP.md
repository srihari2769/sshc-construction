# Twilio SMS Setup Guide

## 🎯 Your Twilio Credentials

Your Twilio credentials are stored in the `.env` file (not committed to GitHub for security).

**Find your credentials at:** https://www.twilio.com/console

---

## 📱 Step 1: Get a Twilio Phone Number

### **Option A: Free Trial Phone Number** (Recommended for Testing)

1. Go to https://www.twilio.com/console
2. Login with your account
3. Click **"Get a Trial Number"** button
4. You'll get a free phone number (e.g., `+1 555 123 4567`)
5. **Copy this number** - you'll need it for Render

**Trial Limitations:**
- Can only send SMS to verified phone numbers
- Messages will have "Sent from your Twilio trial account" prefix
- Perfect for testing!

### **How to Verify Phone Numbers (Trial Account):**
1. Go to https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Click **"Add a verified number"**
3. Enter the Indian phone number you want to test (e.g., `+919876543210`)
4. Enter the verification code sent to that number
5. Now you can send SMS to this number!

---

### **Option B: Buy a Phone Number** (For Production)

**Cost:** ~$1-2/month + $0.0079 per SMS to India

1. Go to https://console.twilio.com/us1/develop/phone-numbers/manage/buy
2. Select country: **United States** (cheapest)
3. Check "SMS" capability
4. Click **"Search"**
5. Choose any number and click **"Buy"**
6. Confirm purchase

---

## 🚀 Step 2: Add to Render Environment Variables

1. Go to Render Dashboard → Your Web Service
2. Click **"Environment"** tab
3. Add these variables:

```bash
TWILIO_ACCOUNT_SID = your-account-sid-from-twilio-console
TWILIO_AUTH_TOKEN = your-auth-token-from-twilio-console
TWILIO_PHONE_NUMBER = +15551234567
```

**Replace `+15551234567` with your actual Twilio number!**

4. Click **"Save Changes"**
5. Service will auto-redeploy

---

## 📋 Step 3: Phone Number Format

Your customers can enter phone numbers in any format:
- `9876543210` → Auto-converted to `+919876543210`
- `09876543210` → Auto-converted to `+919876543210`
- `919876543210` → Auto-converted to `+919876543210`
- `+919876543210` → Used as-is

The system automatically adds India country code (+91) if missing.

---

## 💰 Pricing (India)

### **Trial Account:**
- **Free** trial credit: $15-20
- Can send ~2000 SMS to India

### **Paid Account:**
- **SMS Cost:** $0.0079 per message to India (₹0.66)
- **Phone Number:** $1/month
- **No minimum commitment**

**Example:**
- 1000 SMS/month = $7.90 + $1 = **$8.90/month** (₹740)
- Much cheaper than other providers!

---

## 🧪 Testing

### **Test SMS from Console:**
1. Go to https://console.twilio.com/us1/develop/sms/try-it-out/send-an-sms
2. From: Your Twilio number
3. To: Verified phone number (with +91)
4. Message: Test message
5. Click **"Send"**

If successful, you're ready to go!

---

## ✅ After Setup Checklist

- [ ] Got Twilio phone number
- [ ] Added phone number to Render environment variables
- [ ] Verified at least one test phone number (for trial)
- [ ] Tested SMS from Twilio console
- [ ] Service redeployed on Render

---

## 🔍 Troubleshooting

### **Error: "The number +919876543210 is unverified"**
**Solution:** On trial account, verify the number first:
https://console.twilio.com/us1/develop/phone-numbers/manage/verified

### **Error: "From phone number not valid"**
**Solution:** Check `TWILIO_PHONE_NUMBER` in Render has your actual Twilio number with country code (e.g., `+15551234567`)

### **SMS not received:**
1. Check Render logs for errors
2. Check Twilio console logs: https://console.twilio.com/us1/monitor/logs/sms
3. Verify phone number format includes +91
4. Ensure phone number is verified (trial account)

---

## 📊 Monitor SMS

View all sent SMS:
https://console.twilio.com/us1/monitor/logs/sms

Shows:
- Status (delivered, failed, sent)
- Phone numbers
- Message content
- Errors (if any)

---

**Ready to test!** Just add the Twilio phone number to Render and your SMS notifications will work! 🎉
