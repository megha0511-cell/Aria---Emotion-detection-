# ARIA – Emotion-Aware Virtual Assistant 🤖

ARIA is an AI-based emotional virtual assistant designed to improve human–computer interaction by understanding user emotions and responding accordingly. The system analyzes text messages from users, detects emotions such as happiness, sadness, anger, or neutrality, and provides appropriate responses in a conversational manner.

This project demonstrates how **Artificial Intelligence (AI)** and **Natural Language Processing (NLP)** can be used to simulate human-like interactions and create more empathetic digital assistants.

---

## 📌 Introduction

In modern human–computer interaction, understanding the emotional state of a user plays an important role in improving user experience. ARIA is a basic intelligent agent capable of detecting emotions from user inputs and responding accordingly.

By analyzing text-based inputs, ARIA can identify emotional states and generate suitable conversational replies, making the interaction more natural and engaging.

---

## 🎯 Objectives

* To develop a basic intelligent agent capable of detecting user emotions.
* To analyze text-based inputs and identify emotional states.
* To provide personalized responses based on detected emotions.
* To improve human–computer interaction by making communication more natural.
* To build a simple and interactive web interface for user interaction.

---

## ⚙️ System Overview

ARIA works through three main stages:

**Input:**
The user sends a text message through the web interface.

**Processing:**
The system analyzes the input using emotion detection techniques or NLP-based models to identify the user's emotional state.

**Output:**
Based on the detected emotion, ARIA generates an appropriate response and displays it to the user.

---

## 🛠️ Technology Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python
* Flask Framework

**Other Technologies**

* NLP-based emotion detection
* Google Generative AI API
* MySQL Database

---

## ✨ Features

* Emotion Detection (Happy, Sad, Angry, Neutral)
* AI-based conversational responses
* Interactive chat interface
* Chat session management
* Chat history storage
* Voice playback of responses
* Song and movie suggestions if the AI cannot generate a response
* Lightweight and fast application

---

## 🗂️ Project Structure

```
ARIA/
│
├── app.py
├── templates/
│     └── index.html
│
├── static/
│     ├── css
│     └── js
│
└── database
      └── aria_db
```

---

## 🚀 How to Run the Project

1. Clone the repository

```
git clone https://github.com/yourusername/ARIA.git
```

2. Navigate to the project folder

```
cd ARIA
```

3. Install required dependencies

```
pip install flask nltk text2emotion mysql-connector-python flask-cors google-generativeai
```

4. Run the application

```
python app.py
```

5. Open the browser and go to

```
http://127.0.0.1:5000
```

---

## 📊 Output

The application provides a chat interface where users can send messages and receive responses from ARIA. The system detects the user's emotion and displays it along with the AI-generated reply.

---

## 🔮 Future Scope

* Integration of machine learning-based emotion detection models
* Speech recognition for voice-based interaction
* Multi-language support
* Deployment on cloud platforms
* More advanced conversational capabilities

---

## 📚 Conclusion

ARIA is a simple yet effective intelligent agent capable of detecting emotions and providing relevant responses. It demonstrates how emotion detection and AI-driven communication can make interactions more human-like and engaging.

The project provides a foundation for developing more advanced conversational agents in the future.

---

## 👩‍💻 Author

**Megha Chavan**
B.Sc. Computer Science
Pillai College of Arts, Commerce & Science

---

⭐ If you like this project, feel free to give it a star on GitHub!
