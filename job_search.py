"""
JobHunt Bot — Pavan Alapati
Searches Naukri, Indeed India, LinkedIn public listings daily
Sends WhatsApp alert with matching jobs
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from twilio.rest import Client
import time

# ── CONFIG ────────────────────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN  = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"   # Twilio sandbox number
MY_WHATSAPP_NUMBER   = os.environ["MY_WHATSAPP_NUMBER"]  # e.g. whatsapp:+919533852285

SEARCH_KEYWORDS = [
    "Senior Angular Developer",
    "Angular Ionic Developer",
    "Frontend Developer Angular",
    "Angular 19 Developer",
    "Angular Hybrid Mobile Developer",
]

LOCATION = "Hyderabad"
EXPERIENCE_MIN = 8  # years

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# ── SCRAPERS ──────────────────────────────────────────────────────────────────

def search_naukri(keyword: str) -> list[dict]:
    """Search Naukri public search page"""
    jobs = []
    try:
        # Naukri public search URL (no login needed)
        query = keyword.replace(" ", "-").lower()
        url = f"https://www.naukri.com/{query}-jobs-in-hyderabad"
        
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [Naukri] Status {resp.status_code} for '{keyword}'")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Naukri job cards
        cards = soup.select("article.jobTuple") or soup.select("[class*='jobTuple']") or soup.select(".job-container")
        
        for card in cards[:8]:  # top 8 per keyword
            try:
                title_el = card.select_one("a.title") or card.select_one("[class*='title']")
                company_el = card.select_one("a.subTitle") or card.select_one("[class*='companyInfo']")
                exp_el = card.select_one("span.ellipsis") or card.select_one("[class*='experience']")
                link_el = card.select_one("a[href*='naukri.com']") or title_el

                title   = title_el.get_text(strip=True)   if title_el   else "N/A"
                company = company_el.get_text(strip=True)  if company_el else "N/A"
                exp     = exp_el.get_text(strip=True)      if exp_el     else "N/A"
                link    = link_el.get("href", "")          if link_el    else url

                if not link.startswith("http"):
                    link = "https://www.naukri.com" + link

                jobs.append({
                    "title":   title,
                    "company": company,
                    "exp":     exp,
                    "link":    link,
                    "portal":  "Naukri",
                    "keyword": keyword
                })
            except Exception:
                continue

        print(f"  [Naukri] '{keyword}' → {len(jobs)} jobs")
    except Exception as e:
        print(f"  [Naukri] Error: {e}")
    return jobs


def search_indeed(keyword: str) -> list[dict]:
    """Search Indeed India public search page"""
    jobs = []
    try:
        q = keyword.replace(" ", "+")
        url = f"https://in.indeed.com/jobs?q={q}&l=Hyderabad%2C+Telangana&explvl=senior_level"
        
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [Indeed] Status {resp.status_code}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.job_seen_beacon") or soup.select("[class*='jobCard']")

        for card in cards[:8]:
            try:
                title_el   = card.select_one("h2.jobTitle span") or card.select_one("h2")
                company_el = card.select_one("[data-testid='company-name']") or card.select_one(".companyName")
                link_el    = card.select_one("h2.jobTitle a") or card.select_one("a[id^='job_']")

                title   = title_el.get_text(strip=True)   if title_el   else "N/A"
                company = company_el.get_text(strip=True)  if company_el else "N/A"
                href    = link_el.get("href", "")          if link_el    else ""
                link    = f"https://in.indeed.com{href}" if href.startswith("/") else href or url

                jobs.append({
                    "title":   title,
                    "company": company,
                    "exp":     "8+ yrs",
                    "link":    link,
                    "portal":  "Indeed",
                    "keyword": keyword
                })
            except Exception:
                continue

        print(f"  [Indeed] '{keyword}' → {len(jobs)} jobs")
    except Exception as e:
        print(f"  [Indeed] Error: {e}")
    return jobs


def search_foundit(keyword: str) -> list[dict]:
    """Search Foundit (ex-Monster India)"""
    jobs = []
    try:
        q = keyword.replace(" ", "%20")
        url = f"https://www.foundit.in/srp/results?query={q}&location=Hyderabad&experience=8"

        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [Foundit] Status {resp.status_code}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("[class*='jobCard']") or soup.select("[class*='card-apply']")

        for card in cards[:6]:
            try:
                title_el   = card.select_one("[class*='title']") or card.select_one("h3")
                company_el = card.select_one("[class*='company']")
                link_el    = card.select_one("a")

                title   = title_el.get_text(strip=True)   if title_el   else "N/A"
                company = company_el.get_text(strip=True)  if company_el else "N/A"
                href    = link_el.get("href", "")          if link_el    else ""
                link    = f"https://www.foundit.in{href}" if href.startswith("/") else href or url

                jobs.append({
                    "title":   title,
                    "company": company,
                    "exp":     "8+ yrs",
                    "link":    link,
                    "portal":  "Foundit",
                    "keyword": keyword
                })
            except Exception:
                continue

        print(f"  [Foundit] '{keyword}' → {len(jobs)} jobs")
    except Exception as e:
        print(f"  [Foundit] Error: {e}")
    return jobs


# ── DEDUP + FILTER ─────────────────────────────────────────────────────────────

def deduplicate(jobs: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for j in jobs:
        key = (j["title"].lower()[:40], j["company"].lower()[:30])
        if key not in seen:
            seen.add(key)
            unique.append(j)
    return unique


def is_relevant(job: dict) -> bool:
    """Basic relevance filter"""
    title_lower = job["title"].lower()
    relevant_terms = ["angular", "frontend", "front-end", "ionic", "mobile", "capacitor"]
    skip_terms = ["java backend", "python", "data engineer", "devops", "qa", "tester",
                  "android native", "ios native", "flutter", "react native only"]
    
    has_relevant = any(t in title_lower for t in relevant_terms)
    has_skip = any(t in title_lower for t in skip_terms)
    return has_relevant and not has_skip


# ── WHATSAPP ──────────────────────────────────────────────────────────────────

def send_whatsapp(jobs: list[dict]):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    today = datetime.now().strftime("%d %b %Y")

    if not jobs:
        body = (
            f"🤖 *JobHunt Bot — {today}*\n\n"
            "No new Angular jobs found today matching your profile.\n"
            "Will check again tomorrow at 9 AM! 💪"
        )
        client.messages.create(
            body=body,
            from_=TWILIO_WHATSAPP_FROM,
            to=MY_WHATSAPP_NUMBER
        )
        print("WhatsApp sent: No jobs today")
        return

    # Split into chunks (WhatsApp has 1600 char limit)
    chunks = []
    
    # Header message
    header = (
        f"🤖 *JobHunt Bot — {today}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✅ Found *{len(jobs)} Angular jobs* matching your profile!\n"
        f"📍 Hyderabad + Remote | 8+ Years exp\n"
        f"━━━━━━━━━━━━━━━━━━\n"
    )
    chunks.append(header)

    # Job messages (3 per WhatsApp message)
    job_messages = []
    for i, j in enumerate(jobs[:15], 1):  # max 15 jobs
        msg = (
            f"*{i}. {j['title']}*\n"
            f"🏢 {j['company']}\n"
            f"🔗 Via {j['portal']}\n"
            f"👉 {j['link'][:80]}\n"
        )
        job_messages.append(msg)

    # Group into batches of 4
    for i in range(0, len(job_messages), 4):
        batch = job_messages[i:i+4]
        chunks.append("\n".join(batch))

    # Footer
    footer = (
        "━━━━━━━━━━━━━━━━━━\n"
        "📎 Apply with: *Pavan_Alapati_Resume.docx*\n"
        "⏰ Next search: Tomorrow 9:00 AM IST\n"
        "_JobHunt Bot by Pavan_"
    )
    chunks.append(footer)

    # Send each chunk
    for chunk in chunks:
        client.messages.create(
            body=chunk,
            from_=TWILIO_WHATSAPP_FROM,
            to=MY_WHATSAPP_NUMBER
        )
        time.sleep(1)  # avoid rate limit

    print(f"✅ WhatsApp sent: {len(chunks)} messages, {len(jobs)} jobs")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*50}")
    print(f"JobHunt Bot — {datetime.now().strftime('%d %b %Y %H:%M')} IST")
    print(f"{'='*50}\n")

    all_jobs = []

    for keyword in SEARCH_KEYWORDS:
        print(f"\n🔍 Searching: '{keyword}'")
        all_jobs += search_naukri(keyword)
        time.sleep(2)  # polite delay
        all_jobs += search_indeed(keyword)
        time.sleep(2)
        all_jobs += search_foundit(keyword)
        time.sleep(2)

    print(f"\n📊 Raw results: {len(all_jobs)} jobs")

    # Filter & deduplicate
    relevant = [j for j in all_jobs if is_relevant(j)]
    unique   = deduplicate(relevant)

    print(f"✅ After filter+dedup: {len(unique)} unique relevant jobs\n")

    for j in unique:
        print(f"  • {j['title']} @ {j['company']} [{j['portal']}]")

    # Save results to JSON (GitHub Actions artifact)
    with open("jobs_found.json", "w") as f:
        json.dump({
            "date": datetime.now().isoformat(),
            "total": len(unique),
            "jobs": unique
        }, f, indent=2)

    # Send WhatsApp
    print("\n📲 Sending WhatsApp...")
    send_whatsapp(unique)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
