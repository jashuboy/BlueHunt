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
    "DFIR Analyst",
    "Blue Team Analyst",
    "Cybersecurity Intern"
]

LOCATIONS = [
    "India",
    "Hyderabad",
    "Bangalore",
    "Pune",
    "Chennai",
    "Noida",
    "Mumbai",
    "Remote"
]


def fetch_linkedin_jobs():

    jobs = []
    seen = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for role in SEARCH_TERMS:

            for location in LOCATIONS:

                role_query = quote(role)
                location_query = quote(location)

                url = (
                    "https://www.linkedin.com/jobs/search/"
                    f"?keywords={role_query}"
                    f"&location={location_query}"
                )

                print(f"\nOpening {url}")

                try:

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    page.wait_for_timeout(5000)

                    body = page.locator(
                        "body"
                    ).inner_text()

                    lines = body.split("\n")

                    for i in range(len(lines)):

                        title = lines[i].strip()

                        if (
                            "soc" in title.lower()
                            or "cyber" in title.lower()
                            or "security analyst" in title.lower()
                            or "siem" in title.lower()
                        ):

                            company = "Unknown"
                            location_value = location

                            if i + 1 < len(lines):
                                company = lines[i + 1].strip()

                            job_id = (
                                title +
                                company +
                                location_value
                            )

                            if job_id in seen:
                                continue

                            seen.add(job_id)

                            jobs.append(
                                {
                                    "title": title,
                                    "company": company,
                                    "location": location_value,
                                    "experience": "0-1 Years",
                                    "platform": "LinkedIn",
                                    "url": url,
                                    "raw_text": body
                                }
                            )

                except Exception as e:
                    print(
                        f"LinkedIn error: {e}"
                    )

        browser.close()

    print(
        f"\nLinkedIn jobs fetched: {len(jobs)}"
    )

    return jobs