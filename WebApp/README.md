# 🌱 Habit Tracker Web App (Flask)

**Habit Tracker** is a clean, responsive web application designed to help users build and maintain positive habits. Built with Python and Flask, this app offers streak tracking, motivational quotes, theme customization, and more — all in a secure, lightweight environment.

---

## 🚀 Try It Out

You can clone and run the project locally using the steps below, or deploy it to your own server using Heroku, Render, or any cloud service.

---

## 🌟 Features

- ✅ **User Accounts & Authentication** – Sign up, log in, and manage your personal habit list securely.
- ✅ **Streak Tracking** – Stay motivated by watching your streaks grow.
- ✅ **Add/Edit/Delete Habits** – Full CRUD support per habit.
- ✅ **Motivational Quotes** – Randomly displayed quotes to keep you going.
- ✅ **Customizable Theme** – Supports light and dark mode preferences per user.
- ✅ **Reminder Support** – Optional reminder scheduling (custom or recurring).
- ✅ **Data Privacy** – No external tracking or analytics.
- ✅ **Responsive Design** – Optimized for desktop, tablet, and mobile.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python), SQLAlchemy, Flask-Login
- **Frontend**: HTML, CSS (Bootstrap or custom), JavaScript
- **Database**: SQLite (default) or MySQL/PostgreSQL (production-ready)
- **Utilities**: Flask-WTF (forms), dotenv (env management)

---

## 🧑‍💻 Setup Instructions

### Prerequisites

- Python 3.9+
- `pip` installed
- Virtual environment (recommended)

### Installation

```bash
git clone https://github.com/yourusername/flask-habit-tracker.git
cd flask-habit-tracker
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env      # Add your secrets, DB URI, etc.
flask db upgrade          # Apply database migrations
flask run
