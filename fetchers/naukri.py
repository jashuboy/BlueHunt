from playwright.sync_api import sync_playwright
from urllib.parse import quote

SEARCH_TERMS = [
    "SOC Analyst",
    "SOC L1",
    "Security Analyst",
    "Cybersecurity Analyst",
    "SIEM Analyst",
    "Splunk Analyst",
    "Threat Hunter",
    "Threat Intelligence Analyst",
    "Incident Response Analyst",
    "Incident Responder",
    "DFIR Analyst",
    "Blue Team Analyst",
    "Cyber Defense Analyst",
    "Security Monitoring Analyst",
    "Cyber Security Engineer",
    "Information Security Analyst",
    "Cybersecurity Intern",
    "Security Intern",
    "SOC Engineer",
    "Security Operations Center Analyst"
]

SEARCH_URLS = []
for term in SEARCH_TERMS:
    slug = term.lower().replace(" ", "-")
    url = f"https://www.naukri.com/{slug}-jobs?experience=0"
    SEARCH_URLS.append(url)

TARGET_LOCATIONS = [
    "hyderabad",
    "bangalore",
    "bengaluru",
    "pune",
    "chennai",
    "mumbai",
    "noida",
    "gurgaon",
    "remote",
    "india"
]


def fetch_naukri_jobs():
    jobs = []
    seen_jobs = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Correctly apply User Agent using a Browser Context
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for url in SEARCH_URLS:
            try:
                print(f"\nOpening {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(5000)

                body = page.locator("body").inner_text()
                body_lower = body.lower()

                # Corrected blocked request tracking blocks
                if "you don't have permission" in body_lower:
                    print("Naukri blocked request.")
                    continue

                if "access denied" in body_lower:
                    print("Naukri access denied.")
                    continue

                lines = body.split("\n")

                for i in range(len(lines)):
                    line = lines[i].strip()
                    if not line:
                        continue

                    lower = line.lower()
                    if (
                        "soc" in lower or
                        "cyber" in lower or
                        "security analyst" in lower or
                        "siem" in lower or
                        "splunk" in lower or
                        "incident response" in lower
                    ):
                        title = line
                        company = "Unknown"
                        experience = "Unknown"
                        location = "Unknown"

                        # Extract Company
                        if i + 1 < len(lines):
                            company = lines[i + 1].strip()

                        # Experience + Location contextual extraction
                        for j in range(i, min(i + 10, len(lines))):
                            current = lines[j]

                            if "yrs" in current.lower() or "year" in current.lower():
                                experience = current.strip()

                            for loc in TARGET_LOCATIONS:
                                if loc in current.lower():
                                    location = current.strip()
                                    break

                        job_id = title + company + location
                        if job_id in seen_jobs:
                            continue

                        seen_jobs.add(job_id)
                        jobs.append(
                            {
                                "title": title,
                                "company": company,
                                "location": location,
                                "experience": experience,
                                "platform": "Naukri",
                                "url": url,
                                "raw_text": "\n".join(
                                    lines[i : min(i + 20, len(lines))]
                                )
                            }
                        )

            except Exception as e:
                print(f"Naukri Error: {e}")

        browser.close()

    print(f"\nNaukri jobs fetched: {len(jobs)}")
    return jobs
