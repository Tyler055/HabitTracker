# 🧠 File Organization App

A web application that helps users organize their files and folders efficiently, with an intuitive interface that supports file selection, exclusion, uploading, and automatic path suggestions.

🚀 Features
✅ File and Folder Selection – Users can select files and folders they want to manage.

🛑 Exclusion of Files/Folders – Users can exclude certain files or folders based on presets or manually defined criteria.

📤 Upload Functionality – After selecting files, users can upload them into the system.

📂 Path Scanning & Suggestions – The app scans file paths and suggests appropriate locations for files. Users can confirm or modify the path.

🔒 Security Features – Provides basic security to prevent unauthorized access to files.

🔄 Redundancy Detection – Detects duplicate files and provides options to manage redundancy.

🌙 Dark Mode – User theme preferences saved locally.

🧪 Test Suite – Testing with Pytest for backend and Jest for frontend.

🛠️ Tech Stack
📦 Backend (Flask)
Flask, Flask-JWT-Extended, Flask-Login, SQLAlchemy, Flask-Mail

SQLite (development) / MySQL (production)

Flask-Migrate + Alembic for migrations

Marshmallow for validation

🎨 Frontend (React + Vite)
React 18, React Router, Axios, Babel, Webpack, Vite

Vanilla CSS + CSS themes

React Spinners for loading states

🔐 Auth & Security
JWT tokens (access/refresh)

BCrypt password hashing

XSS & CORS protection

Role-based middleware (admin, user)

📦 Dependencies
Frontend Dependencies
bash
Copy code
habit-tracker-frontend@1.0.0 C:\School\AI_Habit\frontend
├── @babel/preset-env@7.26.9
├── @babel/preset-react@7.26.3
├── axios@1.8.4
├── babel-loader@8.4.1
├── react-dom@18.3.1
├── react-router-dom@7.4.0
├── react-scripts@5.0.1
├── react-spinners@0.15.0
├── react@18.3.1
├── webpack-cli@6.0.1
├── webpack-dev-server@5.2.1
├── webpack@5.98.0
└── xss-clean@0.1.4
Global Dependencies
bash
Copy code
$ npm list -g --depth=0
C:\Users\tylje\AppData\Roaming\npm
├── jest@29.7.0
├── mongosh@2.4.2
├── npm-check-updates@17.1.15
├── npm@11.2.0
├── serve@14.2.4
└── vite@6.2.2
Backend Dependencies
bash
Copy code

## Core Flask & Extensions

Flask==3.1.0
Flask-Login==0.6.3
Flask-JWT-Extended==4.7.1
Flask-Mail==0.10.0
Flask-Migrate==4.1.0
Flask-Cors==5.0.1
Flask-WTF==1.2.2
flask-marshmallow==1.3.0
Flask-SQLAlchemy==3.1.1
Flask-MySQL==1.6.0
flask-mysql-connector==1.1.0
Flask-PyMongo==3.0.1

## --- ORM / DB Drivers ---

SQLAlchemy==2.0.38
mysql-connector-python==9.2.0
PyMySQL==1.1.1
pymongo==4.11.3
alembic==1.15.1

## --- Serialization / Validation ---

marshmallow==3.26.1
email_validator==2.2.0

## --- Security ---

bcrypt==4.3.0
cryptography==44.0.2
itsdangerous==2.2.0
PyJWT==2.10.1

## --- Utility & Support ---

python-dotenv==1.0.1
click==8.1.8
colorama==0.4.6
Werkzeug==3.1.3
blinker==1.9.0
Jinja2==3.1.6
MarkupSafe==3.0.2
tk==0.1.0

## --- Data / Analysis ---

numpy==2.2.4
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
tzdata==2025.2

## --- HTTP / Requests ---

requests==2.32.3
urllib3==2.3.0
charset-normalizer==3.4.1
idna==3.10
certifi==2025.1.31

## --- Testing ---

pytest==8.3.5
iniconfig==2.0.0
pluggy==1.5.0

## --- Internal / C-Dependencies ---

greenlet==3.1.1
cffi==1.17.1
pycparser==2.22
six==1.17.0
typing_extensions==4.13.0

## --- Templating / Migrations ---

Mako==1.3.9
git-filter-repo==2.47.0

⚙️ Usage
Register or log in with your account.

Select files and folders you wish to organize.

Exclude files/folders based on predefined settings or custom exclusions.

Upload the selected files.

Path scanning will suggest the best locations for files, which you can confirm or modify.

View security settings and track duplicates to manage your file organization effectively.

Toggle between light and dark mode in your preferences.

Future AI Integration:
AI Features (Planned): In the future, AI will be incorporated to assist with automating the file organization process, analyzing file paths, and offering smarter suggestions to users for file placements.

Not Implemented Yet: Currently, there is no AI integration in the app.

Libraries Used:
Flask – Web framework for Python

Flask-JWT-Extended – JSON Web Token support for Flask

Flask-Login – User session management

SQLAlchemy – SQL toolkit and ORM for Python

Flask-Mail – Email support for reminders

Marshmallow – Object serialization/deserialization

React – JavaScript library for building UIs

React Router – Navigation in React

Axios – HTTP client for making requests

React Spinners – Loading animation components

Vite – Next-generation, fast bundler for React

Exclusion Presets:
User-defined exclusions: Users can specify files or folders to always be excluded, either manually or through predefined presets.

Preset Options: Include common system files, temporary files, etc., that can be excluded by default.

Security:
Access Control: The app ensures that files are only accessible to authorized users by restricting access as needed.

JWT Authentication: Token-based authentication to secure sensitive routes and actions.

Password Security: BCrypt hashing to store user passwords securely.

Simplified User Experience:
Single Page or Popup Interface: The app will have a simple, clean interface, either on a single-page website or a popup window for seamless user interaction.

Next Steps:
Current Progress: Continue implementing the basic features for file organization, exclusion, and uploading.

Future Development: Prepare the app for AI integration to assist in smarter file management and automation.

🪪 License
This project is licensed under the BSD 3-Clause License.

This software uses Redis, which is licensed under the BSD 3-Clause License. See LICENSE-REDIS.txt for more details.

📫 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

🙌 Acknowledgments
This project was made possible using the following open-source software and tools:

Redis – In-memory data store (Redis Documentation)

Flask – Web framework for Python (Flask Documentation)

SQLAlchemy – SQL toolkit and ORM for Python (SQLAlchemy Documentation)

Flask-Login – User session management (Flask-Login Documentation)

React – JavaScript library for building UIs (React Documentation)
