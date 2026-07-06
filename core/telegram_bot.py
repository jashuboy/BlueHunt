import requests
from config import BOT_TOKEN, CHAT_ID


def send_job_notification(
    job,
    score,
    matched,
    negative_matches,
    rating
):

    message = f"""
🚨 BlueHunt Alert

🎯 Role:
{job['title']}

🏢 Company:
{job['company']}

📍 Location:
{job['location']}

💼 Experience:
{job['experience']}

🌐 Platform:
{job['platform']}

📊 Score:
{score}/100

🏅 Rating:
{rating}

✅ Matched Skills:
{", ".join(matched) if matched else "None"}

❌ Negative Indicators:
{", ".join(negative_matches) if negative_matches else "None"}

🔗 Apply:
{job['url']}
"""

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }

    try:

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=payload,
            timeout=30
        )

        if response.status_code == 200:
            print(f"Telegram sent -> {job['title']}")

        else:
            print(
                f"Telegram failed -> "
                f"{response.status_code} -> "
                f"{response.text}"
            )

    except Exception as e:
        print(f"Telegram Exception: {e}")