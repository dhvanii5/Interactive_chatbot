# College Chatbot – ADIT Virtual Assistant 🤖

## Overview
A Flask-based chatbot that serves as a **virtual assistant for A. D. Patel Institute of Technology (ADIT)**.  
It helps students, parents, and visitors get instant answers about the college, such as admissions, programs, tuition, and facilities.

This project integrates **Groq LLaMA-3** for natural language processing and **Firebase Authentication** for secure login and signup.

---

## 🚀 Features
- 🔐 **User Authentication** – Secure login/signup via Firebase.  
- 💬 **AI-powered Chat** – Powered by Groq API with **LLaMA3-70B** model.  
- 🎨 **Responsive UI** – Clean and modern chat interface.  
- ⚡ **Session Management** – Server-side sessions using `flask_session`.  
- 🛠 **Custom Prompts** – Chatbot is context-aware with ADIT college data.  

---

## 🛠 Tech Stack

| Component          | Technology Used                         |
| ------------------ | --------------------------------------- |
| Backend            | Flask, Flask-Login, Flask-Session       |
| Frontend           | HTML, CSS, JavaScript                   |
| Authentication     | Firebase Authentication                 |
| AI Integration     | Groq API (LLaMA3-70B-8192)              |
| Deployment         | Localhost or any Flask-supported server |

---

## 📂 Project Structure
project-root/
│
├── config/
│ ├── config.py # Stores API keys and college data
│ ├── firebase_config.py # Firebase initialization & token verification
│
├── templates/
│ ├── index.html # Chat interface
│ ├── login.html # Login page
│
├── static/ # Static CSS, JS, images (if any)
│
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
├── .env # Environment variables
└── README.md # Documentation


---

## ▶️ Running the Project
1. Clone the repository  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
python app.py

