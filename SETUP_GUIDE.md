# 🤖 JobHunt Bot — Setup Guide for Pavan Alapati
## Daily WhatsApp job alerts at 9 AM IST — Free, No server needed

---

## What You Need (All Free)
- GitHub account (free) → runs the bot
- Twilio account (free) → sends WhatsApp
- Your WhatsApp phone number

---

## STEP 1 — Create GitHub Account & Repo (5 min)

1. Go to https://github.com → Sign up (free)
2. Click "New repository"
3. Name it: `jobhunt-bot`
4. Set to **Private** (important!)
5. Click "Create repository"

Upload these files to the repo:
- `job_search.py`
- `requirements.txt`
- `.github/workflows/jobhunt.yml`   ← this exact folder structure

---

## STEP 2 — Setup Twilio WhatsApp (10 min)

1. Go to https://www.twilio.com → Sign up FREE
2. No credit card needed for sandbox
3. After login → go to **Messaging → Try it out → Send a WhatsApp message**
4. You will see a sandbox number like: `+1 415 523 8886`
5. **From your WhatsApp**, send this message to that number:
   ```
   join <your-sandbox-word>
   ```
   (Twilio shows you the exact word, like "join apple-mango")
6. You'll get a reply: "You are now connected" ✅

7. From Twilio dashboard, copy:
   - **Account SID** (starts with AC...)
   - **Auth Token** (click to reveal)

---

## STEP 3 — Add Secrets to GitHub (3 min)

In your GitHub repo:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these 3:

| Secret Name | Value |
|-------------|-------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `MY_WHATSAPP_NUMBER` | `whatsapp:+919533852285` |

---

## STEP 4 — Test It Now (2 min)

1. In your GitHub repo → click **Actions** tab
2. Click **"JobHunt Bot — Daily Search"**
3. Click **"Run workflow"** → **"Run workflow"** (green button)
4. Wait 2-3 minutes
5. Check your WhatsApp! 📲

---

## STEP 5 — It Runs Automatically Forever!

The cron `30 3 * * *` = every day 3:30 AM UTC = **9:00 AM IST**

GitHub Actions gives you **2,000 free minutes/month**.
This bot uses ~3 minutes per day = 90 min/month. Well within free tier! ✅

---

## What the WhatsApp Message Looks Like

```
🤖 JobHunt Bot — 27 Mar 2026
━━━━━━━━━━━━━━━━━━
✅ Found 12 Angular jobs matching your profile!
📍 Hyderabad + Remote | 8+ Years exp
━━━━━━━━━━━━━━━━━━

1. Senior Angular Developer
🏢 TCS Digital
🔗 Via Naukri
👉 https://naukri.com/job/...

2. Frontend Lead Angular Ionic
🏢 Infosys BPM
🔗 Via Indeed
👉 https://indeed.co.in/job/...
...
━━━━━━━━━━━━━━━━━━
📎 Apply with: Pavan_Alapati_Resume.docx
⏰ Next search: Tomorrow 9:00 AM IST
```

---

## Troubleshooting

**Bot ran but no WhatsApp received?**
- Check GitHub Actions logs (Actions tab → click the run → see logs)
- Make sure you sent "join ..." to Twilio sandbox from your WhatsApp first

**"No jobs found" message every day?**
- Naukri/Indeed changed their HTML structure (happens occasionally)
- Message Pavan or check the jobs_found.json artifact in Actions

**Twilio sandbox expires?**
- Free sandbox is active as long as you message it once every 72 hours
- For permanent: upgrade Twilio ($1/month) and use WhatsApp Business API

---

## Customise Keywords

Edit `job_search.py` line 20 — `SEARCH_KEYWORDS` list:
```python
SEARCH_KEYWORDS = [
    "Senior Angular Developer",
    "Angular Ionic Developer",
    "Frontend Developer Angular",
    # Add more here...
]
```

---

## Total Cost: ₹0/month 🎉
- GitHub Actions: Free (2000 min/month)
- Twilio Sandbox: Free
- Server: None needed
