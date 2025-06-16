# VoltGuard

## 🔌 Overview

**VoltGuard** is a smart electricity usage tracker web app built with Flask. It allows users to log in, input their electrical appliances, customize usage hours and watts, and get real-time calculations of energy cost, category-based breakdowns, and estimated solar savings. The app supports secure login via Auth0 and integrates a chatbot powered by Google Gemini for energy advice.

---

## ✨ Features

- 🔐 Secure login with Auth0 (Google or manual credentials).
- 📊 Track device usage and electricity cost per day.
- 🗂 Categorize and manage appliances by type.
- 🧮 Live calculation of total usage and costs.
- ☀️ Solar savings estimates.
- 💬 AI Chatbot (VoltBot) for recommendations.
- 📈 Pie chart visualization by usage category.

---

## 🖼️ Screenshots

### 1. Main Dashboard  
Displays the main dashboard where users can input electricity rates, add appliances by category, view usage in a detailed table, and get solar savings estimates. The layout is split into sections for usability.

<img src="https://github.com/FortuneDayZ/VoltGuard/blob/main/ScreenShots/MainPage1.png?raw=true" width="250" />

### 2. Appliance Added Confirmation  
Shows the updated appliance list after adding an item. Users can see usage metrics like kWh/day and cost, and have options to edit or remove entries.

<img src="https://github.com/FortuneDayZ/VoltGuard/blob/main/ScreenShots/Added.png?raw=true" width="250" />

### 3. Chatbot Interface (VoltBot)  
The built-in assistant "VoltBot" can be toggled on demand. It provides personalized energy-saving tips based on current appliances, usage, and rates.

<img src="https://github.com/FortuneDayZ/VoltGuard/blob/main/ScreenShots/ChatBot.png?raw=true" width="250" />

### 4. Dashboard with Chatbot Active  
Illustrates the dashboard while the chatbot is active. Users can chat with VoltBot while interacting with other features like rate selection or the appliance list.

<img src="https://github.com/FortuneDayZ/VoltGuard/blob/main/ScreenShots/MainPageWithChatbot.png?raw=true" width="250" />

### 5. Login Screen  
Allows users to sign in via Google or with a username and password. The design is simple and clearly directs users into the main VoltGuard app.

<img src="https://github.com/FortuneDayZ/VoltGuard/blob/main/ScreenShots/Login.png?raw=true" width="250" />

---

## 🧰 Requirements

- Python 3.x
- PostgreSQL database
- Dependencies listed in `requirements.txt`

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/FortuneDayZ/VoltGuard
cd VoltGuard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the following variables (you can refer to the sample already included in your repo):

```env
# Auth0
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_CALLBACK_URL=http://127.0.0.1:5000/callback

# Google Gemini API
key=your-gemini-api-key

# Flask
FLASK_SECRET=your-random-secret

# PostgreSQL
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DATABASE_URL=postgresql://user:password@host:port/dbname
```

> ⚠️ **Important:** Never share your `.env` file publicly. Replace all placeholders above with your actual credentials.

### 5. Initialize Database

The database tables will be auto-created when the app runs for the first time.

### 6. Start the App

```bash
python main.py
#or 
python3 main.py
```

Visit the app in your browser at:

```
http://127.0.0.1:5000/
```

---

## 🗂 Project Structure

```
VoltGuard/
├── main.py                 # Main Flask app
├── templates/
│   ├── index.html          # Main UI
│   └── login.html          # Login page
├── .env                    # Environment config (not committed)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ✅ Usage

1. Log in using Google or manual credentials.
2. Select or enter your electricity rate.
3. Add electrical devices and categorize them.
4. Get cost analysis and solar savings.
5. Ask VoltBot for energy tips!

---

## 🧠 VoltBot AI

The chatbot is powered by **Google Gemini** (API). Make sure you:
- Include your API key in the `.env` file (`key=your_api_key`)
- Use the correct model endpoint inside your JavaScript code

---

## 🛠 Troubleshooting

- Double-check your `.env` keys are correct.
- If login fails, confirm Auth0 settings (allowed callback URLs, etc.)
- If PostgreSQL fails, test your `DATABASE_URL` connection string.

---

## 📄 License

MIT — feel free to use, modify, and deploy with credit.
