import logging
import time

from core.filtering import is_relevant
from core.scoring import calculate_score, is_blocked_role
from core.storage import job_exists, save_job
from core.telegram_bot import send_job_notification

from fetchers.foundit import fetch_foundit_jobs
from fetchers.linkedin import fetch_linkedin_jobs
from fetchers.naukri import fetch_naukri_jobs
from fetchers.internshala import fetch_internshala_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_bluehunt():

    total_start = time.time()

    jobs = []

    fetch_times = {}
    fetch_counts = {}

    # ===============================
    # Foundit
    # ===============================

    start = time.time()

    try:
        foundit_jobs = fetch_foundit_jobs()
        jobs.extend(foundit_jobs)
        fetch_counts["Foundit"] = len(foundit_jobs)

    except Exception as e:
        logging.error(f"[Foundit] Failed: {e}")
        fetch_counts["Foundit"] = 0

    fetch_times["Foundit"] = time.time() - start

    # ===============================
    # LinkedIn
    # ===============================

    start = time.time()

    try:
        linkedin_jobs = fetch_linkedin_jobs()
        jobs.extend(linkedin_jobs)
        fetch_counts["LinkedIn"] = len(linkedin_jobs)

    except Exception as e:
        logging.error(f"[LinkedIn] Failed: {e}")
        fetch_counts["LinkedIn"] = 0

    fetch_times["LinkedIn"] = time.time() - start

    # ===============================
    # Naukri
    # ===============================

    start = time.time()

    try:
        naukri_jobs = fetch_naukri_jobs()
        jobs.extend(naukri_jobs)
        fetch_counts["Naukri"] = len(naukri_jobs)

    except Exception as e:
        logging.error(f"[Naukri] Failed: {e}")
        fetch_counts["Naukri"] = 0

    fetch_times["Naukri"] = time.time() - start

    # ===============================
    # Internshala
    # ===============================

    start = time.time()

    try:
        internshala_jobs = fetch_internshala_jobs()
        jobs.extend(internshala_jobs)
        fetch_counts["Internshala"] = len(internshala_jobs)

    except Exception as e:
        logging.error(f"[Internshala] Failed: {e}")
        fetch_counts["Internshala"] = 0

    fetch_times["Internshala"] = time.time() - start

    logging.info(f"Total raw jobs fetched: {len(jobs)}")

    sent_count = 0
    duplicate_count = 0
    filtered_count = 0
    blocked_count = 0
    weak_count = 0
    saved_count = 0
    
    saved_by_platform = {
        "Foundit": 0,
        "LinkedIn": 0,
        "Naukri": 0,
        "Internshala": 0
    }

    alerts_by_platform = {
        "Foundit": 0,
        "LinkedIn": 0,
        "Naukri": 0,
        "Internshala": 0
    }

    for job in jobs:

        if job_exists(job["url"]):
            print(f"Duplicate -> {job['title']}")
            duplicate_count += 1
            continue

        if not is_relevant(job):
            print(f"Filtered -> {job['title']}")
            filtered_count += 1
            continue

        if is_blocked_role(job):
            blocked_count += 1
            continue

        score, matched, negative_matches, rating = calculate_score(job)

        if score < 50:
            weak_count += 1
            continue

        save_job(job, score, rating, matched)
        saved_count += 1
        saved_by_platform[job["platform"]] += 1

        if score >= 70:
            send_job_notification(
                job,
                score,
                matched,
                negative_matches,
                rating
            )
            sent_count += 1
            alerts_by_platform[job["platform"]] += 1

    total_runtime = (time.time() - total_start) / 60

    print("\n")
    print("=" * 50)
    print("           BLUEHUNT EXECUTION SUMMARY")
    print("=" * 50)

    print()

    print("Platform Performance")
    print("-" * 50)

    print(
        f"Foundit      : {fetch_counts['Foundit']:>4} jobs | "
        f"{fetch_times['Foundit']:.2f} sec"
    )

    print(
        f"LinkedIn     : {fetch_counts['LinkedIn']:>4} jobs | "
        f"{fetch_times['LinkedIn']:.2f} sec"
    )

    print(
        f"Naukri       : {fetch_counts['Naukri']:>4} jobs | "
        f"{fetch_times['Naukri']:.2f} sec"
    )

    print(
        f"Internshala  : {fetch_counts['Internshala']:>4} jobs | "
        f"{fetch_times['Internshala']:.2f} sec"
    )

    print()

    print("Pipeline Summary")
    print("-" * 50)

    print(f"Total Fetched       : {len(jobs)}")
    print(f"Duplicates Skipped  : {duplicate_count}")
    print(f"Filtered (Rules)    : {filtered_count}")
    print(f"Blocked Roles       : {blocked_count}")
    print(f"Weak Scores (<50)   : {weak_count}")
    print(f"Saved to Database   : {saved_count}")
    print(f"Telegram Alerts     : {sent_count}")

    print()
    
    print("Jobs Saved by Platform")
    print("-" * 50)

    for platform, count in saved_by_platform.items():
        print(f"{platform:<13}: {count}")

    print()

    print("Telegram Alerts by Platform")
    print("-" * 50)

    for platform, count in alerts_by_platform.items():
        print(f"{platform:<13}: {count}")

    print(f"Total Runtime       : {total_runtime:.2f} minutes")

    print("=" * 50)


if __name__ == "__main__":
    run_bluehunt()