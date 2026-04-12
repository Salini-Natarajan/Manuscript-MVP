# 📝 Manuscript AI: Publication-Ready Formatting Tool

An AI-driven SaaS application that automates the tedious process of formatting raw `.docx` manuscripts into publication-ready documents. Built with Python, Streamlit, and the Google Gemini API.

## 🚀 Live Demo
**[Insert Your Streamlit Cloud URL Here]**

## ✨ Key Features
* **Context-Aware AI Classification:** Uses Google Gemini 1.5 Flash to dynamically read and classify text (Titles, Headings, Captions, Paragraphs) without relying on existing Word metadata.
* **Precision Typography Enforcement:** Automatically applies strict publication rules (Times New Roman, Justified text, 1.5 spacing, 1-inch margins, and colored subheadings).
* **Secure Cloud Authentication:** Features a fully authenticated user login system backed by MongoDB Atlas and `bcrypt` password hashing.
* **Privacy-First Processing:** Documents are processed entirely in memory (`BytesIO`). No raw or processed files are ever saved to the server's hard drive.
* **Modern UI/UX:** A sleek, custom-built Dark Mode interface designed for a professional SaaS experience.

## 🛠️ Tech Stack
* **Frontend:** Streamlit, Custom HTML/CSS
* **Backend:** Python 3
* **AI/LLM:** Google Gemini API (`google-generativeai`)
* **Document Engineering:** `python-docx`
* **Database & Security:** MongoDB Atlas, `pymongo`, `bcrypt`

## 💻 Local Setup & Installation

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Salini-Natarajan/Manuscript-MVP.git](https://github.com/Salini-Natarajan/Manuscript-MVP.git)
   cd Manuscript-MVP