from playwright.sync_api import sync_playwright

SEARCH_TERMS = [
    "cyber-security",
    "cybersecurity",
    "soc",
    "information-security",
    "network-security",
    "ethical-hacking",
    "penetration-testing",
    "vapt"
]


def fetch_internshala_jobs():

    jobs = []
    seen = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for term in SEARCH_TERMS:

            url = (
                f"https://internshala.com/internships/"
                f"{term}-internship/"
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

                    if not title:
                        continue

                    title_lower = title.lower()

                    if (
                        "cyber" in title_lower or
                        "soc" in title_lower or
                        "security" in title_lower or
                        "ethical hacker" in title_lower or
                        "penetration" in title_lower or
                        "vapt" in title_lower
                    ):

                        company = "Unknown"
                        location = "Unknown"
                        stipend = "Unknown"
                        duration = "Unknown"

                        for j in range(
                            i,
                            min(i + 15, len(lines))
                        ):

                            current = lines[j]

                            if (
                                "₹" in current or
                                "/month" in current
                            ):
                                stipend = current.strip()

                            if (
                                "months" in current.lower() or
                                "month" in current.lower()
                            ):
                                duration = current.strip()

                            if (
                                "work from home" in current.lower() or
                                "hyderabad" in current.lower() or
                                "bangalore" in current.lower() or
                                "bengaluru" in current.lower() or
                                "pune" in current.lower() or
                                "chennai" in current.lower() or
                                "mumbai" in current.lower() or
                                "noida" in current.lower()
                            ):
                                location = current.strip()

                        if i + 1 < len(lines):
                            company = lines[i + 1].strip()

                        job_id = (
                            title +
                            company +
                            location
                        )

                        if job_id in seen:
                            continue

                        seen.add(job_id)

                        jobs.append(
                            {
                                "title": title,
                                "company": company,
                                "location": location,
                                "experience": "Internship",
                                "stipend": stipend,
                                "duration": duration,
                                "platform": "Internshala",
                                "url": url,
                                "raw_text": "\n".join(
                                    lines[
                                        i:
                                        min(
                                            i + 25,
                                            len(lines)
                                        )
                                    ]
                                )
                            }
                        )

            except Exception as e:
                print(
                    f"Internshala Error: {e}"
                )

        browser.close()

    print(
        f"\nInternshala jobs fetched: {len(jobs)}"
    )

    return jobs