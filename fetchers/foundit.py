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

    slug = (
        term.lower()
        .replace("/", " ")
        .replace("&", " ")
        .replace(" ", "-")
    )

    query = quote(term.lower())

    url = (
        f"https://www.foundit.in/search/"
        f"{slug}-jobs"
        f"?query={query}"
        f"&experienceRanges=0~0"
        f"&experience=0"
        f"&queryDerived=true"
    )

    SEARCH_URLS.append(url)


INDIAN_LOCATIONS = [
    "hyderabad",
    "bangalore",
    "bengaluru",
    "pune",
    "chennai",
    "noida",
    "gurgaon",
    "mumbai",
    "india",
    "remote"
]


def fetch_foundit_jobs():
    jobs = []
    seen_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for search_url in SEARCH_URLS:
            print(f"\nOpening {search_url}")
            page.goto(search_url, wait_until="domcontentloaded")
            page.wait_for_timeout(7000)

            cards = page.locator("a[href*='/job/']")
            total_cards = cards.count()
            print(f"Cards found: {total_cards}")

            for i in range(total_cards):
                try:
                    card = cards.nth(i)
                    href = card.get_attribute("href")

                    if not href:
                        continue

                    if href in seen_urls:
                        continue

                    if href.startswith("/"):
                        href = "https://www.foundit.in" + href

                    seen_urls.add(href)
                    title = card.inner_text().strip()

                    # Open job page for richer extraction
                    job_page = browser.new_page()
                    try:
                        job_page.goto(
                            href,
                            wait_until="domcontentloaded",
                            timeout=30000
                        )
                        job_page.wait_for_timeout(3000)
                        page_text = job_page.locator("body").inner_text()
                    except Exception:
                        page_text = ""
                    finally:
                        job_page.close()

                    lower = page_text.lower()
                    company = "Unknown"
                    location = "Unknown"
                    experience = "Unknown"
                    lines = page_text.split("\n")

                    # Corrected and aligned lines iterator
                    for idx, line in enumerate(lines):
                        if line.strip() == title.strip():
                            if idx + 1 < len(lines):
                                company = lines[idx + 1].strip()
                            if idx + 2 < len(lines):
                                location = lines[idx + 2].strip()
                            if idx + 3 < len(lines):
                                next_line = lines[idx + 3].strip()
                                if next_line == "India":
                                    location = f"{location} India"
                            break

                    # Experience extraction
                    if (
                        "fresher" in lower or
                        "0-1 years" in lower or
                        "0 to 1 years" in lower or
                        "1 year" in lower
                    ):
                        experience = "0-1 Years"

                    jobs.append(
                        {
                            "title": title,
                            "company": company,
                            "location": location,
                            "experience": experience,
                            "raw_text": page_text,
                            "url": href,
                            "platform": "Foundit"
                        }
                    )

                except Exception as e:
                    print(f"Error: {e}")

        browser.close()

    print(f"\nFINAL JOB COUNT: {len(jobs)}")
    return jobs
