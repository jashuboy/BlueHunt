from core.filtering import is_relevant
from core.scoring import calculate_score, is_blocked_role
from core.storage import job_exists, save_job
from core.telegram_bot import send_job_notification
from fetchers.foundit import fetch_foundit_jobs
from fetchers.internshala import fetch_internshala_jobs
from fetchers.linkedin import fetch_linkedin_jobs
from fetchers.naukri import fetch_naukri_jobs


def run_bluehunt():
    jobs = []

    # Fetch listings from multiple platforms
    jobs.extend(fetch_foundit_jobs())
    jobs.extend(fetch_naukri_jobs())
    jobs.extend(fetch_linkedin_jobs())
    jobs.extend(fetch_internshala_jobs())

    print(f"Total jobs fetched: {len(jobs)}")

    sent_count = 0
    duplicate_count = 0
    filtered_count = 0

    for job in jobs:
        if job_exists(job["url"]):
            duplicate_count += 1
            continue

        print(f"\nChecking relevance -> {job['title']}")
        if not is_relevant(job):
            print(f"Filtered -> {job['title']}")
            filtered_count += 1
            continue

        # Correctly aligned execution block
        score, matched, negative_matches, rating = calculate_score(job)

        if is_blocked_role(job):
            print(f"Skipping blocked role -> {job['title']}")
            continue

        # Ignore weak jobs
        if score < 50:
            print(f"Weak score ignored -> {job['title']} ({score})")
            continue

        # Store useful jobs only
        save_job(job, score, rating, matched)

        # Notify only for good matches
        if score >= 70:
            send_job_notification(job, score, matched, negative_matches, rating)
            sent_count += 1

    print("\n========== BLUEHUNT SUMMARY ==========")
    print(f"Fetched Jobs : {len(jobs)}")
    print(f"Duplicates Skipped: {duplicate_count}")
    print(f"Filtered Jobs : {filtered_count}")
    print(f"Telegram Alerts : {sent_count}")
    print("=======================================")


if __name__ == "__main__":
    run_bluehunt()
