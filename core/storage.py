import os
import pandas as pd

DB_FILE = "data/jobs_database.xlsx"


COLUMNS = [
    "title",
    "company",
    "location",
    "experience",
    "platform",
    "url",
    "score",
    "rating",
    "matched_skills"
]


def initialize_database():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DB_FILE):

        df = pd.DataFrame(columns=COLUMNS)

        df.to_excel(
            DB_FILE,
            index=False
        )


def job_exists(job_url):

    initialize_database()

    df = pd.read_excel(DB_FILE)

    return job_url in df["url"].values


def save_job(
    job,
    score,
    rating,
    matched
):

    initialize_database()

    df = pd.read_excel(DB_FILE)

    new_row = {
        "title": job["title"],
        "company": job["company"],
        "location": job["location"],
        "experience": job["experience"],
        "platform": job["platform"],
        "url": job["url"],
        "score": score,
        "rating": rating,
        "matched_skills": ", ".join(matched)
    }

    df = pd.concat(
        [
            df,
            pd.DataFrame([new_row])
        ],
        ignore_index=True
    )

    df.to_excel(
        DB_FILE,
        index=False
    )