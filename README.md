# Habit Tracker Flask App

This is a web application built with Flask to help users track their habits and monitor progress over time. It allows users to create, update, and manage habits with features like streak tracking, notifications, and reminders.

## Features
- **User Authentication**: Login, registration, and password management using Flask-Login.
- **Habit Tracking**: Add, update, and delete habits. Each habit is tied to a user.
- **Streak Tracking**: Track the streak of habit completions.
- **Motivational Quotes**: Display random motivational quotes to encourage users.
- **User Preferences**: Set theme preferences (light/dark mode).
- **Reminders**: Set up reminders for habits and receive notifications (optional).

## Tech Stack
- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (for local development)
- **Authentication**: Flask-Login
- **Environment Variables**: Loaded with `dotenv` for sensitive data (e.g., API keys, database URI)

## Setup Instructions

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- dotenv
- SQLite or MySQL (for production)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/habit-tracker-flask.git
   cd habit-tracker-flask
