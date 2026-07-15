<p align="center">
<img src="assets/banner.png" width="900">
</p>
<h1 align="center">
 BlueHunt
</h1>
 <p align="center">
  <strong>Automated Cybersecurity Job Acquisition Pipeline</strong>
</p>

<p align="center">
  Automating cybersecurity job discovery through intelligent multi-platform aggregation,
  filtering, scoring, and real-time notifications.
</p>

<p align="center">

 ![Python](https://img.shields.io/badge/Python-3.13-blue)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-orange)
</p>


## 📌 Problem Statement
As a cybersecurity fresher, I experienced the challenge of identifying relevant opportunities despite having the required technical skills.
Cybersecurity jobs are distributed across multiple platforms, and manually searching, filtering, and tracking suitable opportunities consumes a significant amount of time every day.
To solve this problem, I built **BlueHunt**, an automated cybersecurity job acquisition pipeline that aggregates job postings from multiple platforms and filters them based on cybersecurity skills, experience requirements, role seniority, and location preferences.
Although BlueHunt currently supports a small number of carefully selected sources, these platforms collectively cover the majority of entry-level cybersecurity opportunities relevant to my target roles.

Challenges include:

- Duplicate job postings across multiple platforms.
- Large numbers of irrelevant or senior-level positions.
- Missing newly posted opportunities.
- Manual tracking of applied jobs.
- Time wasted switching between multiple job platforms.

BlueHunt automates this entire process.
## Workflow

1. Fetch jobs from supported platforms.
2. Extract structured job information.
3. Filter irrelevant and senior-level roles.
4. Score jobs based on skill relevance.
5. Remove duplicate entries.
6. Store unique jobs in Excel.
7. Send Telegram notifications for high-quality matches.


## ⚡Features
- ✅ Multi-platform cybersecurity job scraping
- ✅ SOC and Cybersecurity focused scoring engine
- ✅ Fresher-friendly job prioritization
- ✅ Senior role filtering
- ✅ Environment variable based secret management
- ✅ Duplicate job detection
- ✅ Telegram notifications for strong matches
- ✅ Persistent job database using Excel
- ✅ Automated scheduling using Windows Task Scheduler
- ✅ Experience-aware ranking engine
- ✅ Location-aware filtering for Indian cybersecurity roles

# 📊 Project Highlights

- 🔍 Aggregates jobs from **4 platforms**
- 🎯 Uses **20+ cybersecurity search keywords**
- 📈 Prioritizes entry-level SOC and Cybersecurity roles
- 🚫 Automatically filters senior positions
- 🔁 Eliminates duplicate postings
- 📬 Sends Telegram alerts for high-quality matches
- ⏰ Supports scheduled execution via Windows Task Scheduler

## 🌐 Supported Platforms
Currently supported:

- LinkedIn
- Naukri
- Foundit
- Internshala

---

# 🏗 Architecture

![Architecture/Workflow](assets/architecture_workflow.png)


---

# 🛠 Tech Stack

| Category | Technologies |
|----------|-------------|
| Language | Python |
| Browser Automation | Playwright |
| Data Processing | Pandas |
| Storage | OpenPyXL |
| Notifications | Telegram Bot API |
| Scheduling | Windows Task Scheduler |
| Environment Management | python-dotenv |
| Version Control | Git, GitHub |

---
# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/jashuboy/BlueHunt.git
cd BlueHunt
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install Playwright Browsers

```bash
playwright install
```

## Configure Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```

---

# ▶ Usage

Run manually:

```bash
python main.py
```

Or configure:

```text
Windows Task Scheduler
```

to automate scans at scheduled intervals.

---
# 📷 Assets
# Telegram Alert
![Telegram Alert](assets/telegram_alert.png)
# Job Database
![Excel Database](assets/excel_database.png)
# Target Roles
![Target Roles](assets/scoring_1.png)
# Skills and Experience
![Skills and Experience](assets/scoring_2.png)
# Locations
![Locations](assets/scoring_3.png)
# Negative Weights
![Negative Weights](assets/scoring_4.png)
# Experience Penalties
![Experience Penalties](assets/scoring_5.png)
# Blocked Terms
![Blocked Terms](assets/scoring_6.png)

---

# 📂 Project Structure

```text
BlueHunt/
│
├── assets/
│   ├── architecture_workflow.png
│   ├── banner.png
│   ├── blocked_terms.png
│   ├── excel_database.png
│   ├── experience_penalties.png
│   ├── locations.png
│   ├── negative_weights.png
│   ├── skills.png
│   ├── target_roles.png
│   └── telegram_alert.png
│
├── core/
│   ├── filtering.py          # Rule-based filtering engine
│   ├── scheduler.py          # Scheduled execution utilities
│   ├── scoring.py            # Rule-based scoring engine
│   ├── storage.py            # Excel database management
│   └── telegram_bot.py       # Telegram notification service
│
├── data/
│   └── jobs_database.xlsx    # Stores unique job postings
│
├── fetchers/
│   ├── foundit.py
│   ├── internshala.py
│   ├── linkedin.py
│   └── naukri.py
│
├── .env                      # Environment variables
├── .gitattributes
├── .gitignore
├── config.py                 # Project configuration
├── LICENSE
├── main.py                   # BlueHunt pipeline entry point
├── README.md
├── requirements.txt
└── run_bluehunt.bat          # Windows launcher
```

---

# 🔮 Future Improvements

- AI-powered Resume Match Engine
- AI-based resume tailoring
- Company whitelist and blacklist
- Daily job digest notifications
- Application tracking dashboard
- Interview preparation recommendations

---

# 👨‍💻 Author

**Jashwanth Dola**

- LinkedIn: https://www.linkedin.com/in/jashwanthdola/
- GitHub: https://github.com/jashuboy

---

# ⭐ Support

If you found this project useful, consider giving it a star.
