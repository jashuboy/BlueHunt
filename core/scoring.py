WEIGHTS = {

    # ===============================
    # TARGET ROLES
    # ===============================

    "soc": 40,
    "soc analyst": 40,
    "soc l1": 50,
    "security analyst": 35,
    "cybersecurity analyst": 40,
    "siem analyst": 35,
    "splunk analyst": 35,
    "incident response": 20,
    "incident responder": 20,
    "threat hunting": 25,
    "threat hunter": 25,
    "threat intelligence": 25,
    "dfir": 25,
    "blue team": 20,
    "security operations": 20,

    # ===============================
    # SKILLS
    # ===============================

    "splunk": 20,
    "siem": 20,
    "sysmon": 15,
    "edr": 15,
    "windows": 10,
    "linux": 10,
    "firewall": 10,
    "network security": 10,
    "security monitoring": 15,
    "log analysis": 15,

    # ===============================
    # EXPERIENCE
    # ===============================

    "fresher": 40,
    "0 years": 40,
    "0-1 years": 40,
    "0 to 1 years": 40,
    "1 year": 20,
    "intern": 25,
    "internship": 25,

    # ===============================
    # LOCATIONS
    # ===============================

    "hyderabad": 5,
    "bangalore": 5,
    "bengaluru": 5,
    "pune": 5,
    "chennai": 5,
    "noida": 5,
    "gurgaon": 5,
    "mumbai": 5,
    "remote": 20,
    "india": 5
}


NEGATIVE_WEIGHTS = {

    # ===============================
    # HIGHER SOC LEVELS
    # ===============================

    "l2": -100,
    "level 2": -100,

    "l3": -100,
    "level 3": -100,

    # ===============================
    # SENIORITY
    # ===============================

    "manager": -100,
    "lead": -100,
    "senior": -100,
    "architect": -100,
    "principal": -100,
    "director": -100,
    "staff engineer": -100,
    "head of": -100,
    "vp": -100,
    "vice president": -100,

    # ===============================
    # EXPERIENCE PENALTIES
    # ===============================

    "2 years": 30,
    "2+ years": 20,

    "3 years": 20,
    "3+ years": 10,

    "4 years": -80,
    "4+ years": -90,

    "5 years": -100,
    "5+ years": -100,

    "6 years": -100,
    "6+ years": -100,

    "7 years": -100,
    "7+ years": -100,

    "8 years": -100,
    "8+ years": -100,

    "9 years": -100,
    "10 years": -100
}


BLOCKED_TERMS = [
    "l2",
    "level 2",
    "l3",
    "level 3",
    "manager",
    "lead",
    "senior",
    "architect",
    "principal",
    "director",
    "staff engineer",
    "head of",
    "vp",
    "vice president",
    "social media",
    "data science"
]


def is_blocked_role(job):

    text = (
        job.get("title", "") + " " +
        job.get("raw_text", "")
    ).lower()

    for term in BLOCKED_TERMS:
        if term in text:
            return True

    return False


def calculate_score(job):

    text = (
        job.get("title", "") + " " +
        job.get("raw_text", "") + " " +
        job.get("location", "") + " " +
        job.get("experience", "")
    ).lower()

    score = 0

    matched = []
    negative_matches = []

    # Positive Scoring
    for keyword, weight in WEIGHTS.items():

        if keyword in text:
            score += weight
            matched.append(keyword)

    # Negative Scoring
    for keyword, penalty in NEGATIVE_WEIGHTS.items():

        if keyword in text:
            score += penalty
            negative_matches.append(keyword)

    # Cap score
    score = max(0, min(score, 100))

    # Rating
    if score >= 85:
        rating = "🔥 Excellent Match"

    elif score >= 70:
        rating = "✅ Strong Match"

    elif score >= 50:
        rating = "🟡 Moderate Match"

    else:
        rating = "⚪ Weak Match"

    return (
        score,
        matched,
        negative_matches,
        rating
    )