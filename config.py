import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RUN_TIMES = ["06:00", "18:00"]

TARGET_ROLES = [
    "SOC Analyst",
    "SOC L1",
    "Cybersecurity Analyst",
    "Security Analyst",
    "SIEM Analyst",
    "Splunk Analyst",
    "Threat Hunter",
    "Incident Response Analyst",
    "Incident Responder",
    "DFIR Analyst",
    "Blue Team Analyst",
    "Cybersecurity Intern"
]

MAX_EXPERIENCE = 1
