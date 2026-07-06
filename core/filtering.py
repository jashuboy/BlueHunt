TARGET_SKILLS = [
    "soc",
    "splunk",
    "siem",
    "incident response",
    "incident responder",
    "threat hunting",
    "threat hunter",
    "threat intelligence",
    "cybersecurity",
    "security analyst",
    "security operations",
    "dfir",
    "blue team",
    "edr",
    "sysmon",
    "windows",
    "linux",
    "firewall",
    "network security",
    "security monitoring",
    "log analysis"
]

NEGATIVE_TERMS = [
    "manager",
    "architect",
    "director",
    "vp",
    "vice president",
    "principal",
    "head of",
    "lead security architect"
]


def is_relevant(job):

    text = (
        job["title"] + " " +
        job["raw_text"]
    ).lower()

    # Reject clearly senior roles
    for term in NEGATIVE_TERMS:

        if term in text:

            print(
                f"Rejected Senior Role -> {job['title']}"
            )

            return False

    skill_matches = []

    for skill in TARGET_SKILLS:

        if skill in text:
            skill_matches.append(skill)

    # If title itself matches target role keywords
    if (
        "soc" in job["title"].lower()
        or "cyber" in job["title"].lower()
        or "security analyst" in job["title"].lower()
        or "siem" in job["title"].lower()
        or "splunk" in job["title"].lower()
    ):

        print(
            f"Relevant Title Match -> {job['title']}"
        )

        return True

    # Otherwise require at least one matching skill
    if len(skill_matches) >= 1:

        print(
            f"Relevant Skill Match -> "
            f"{job['title']} -> {skill_matches}"
        )

        return True

    print(
        f"No Relevant Skills -> {job['title']}"
    )

    return False