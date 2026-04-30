# 📄 Manuscript AI

> AI-driven SaaS that turns raw academic manuscripts into publication-ready documents — in seconds.

---

## 🧩 The Problem

Authors and editorial teams spend **hours** manually formatting `.docx` files to meet strict academic journal guidelines. Wrong fonts. Missed line spacing. Misaligned figures. Human error is inevitable, and it delays publication and increases costs.

**Manuscript AI eliminates this entirely.**

---

## ✨ The Solution

Upload your raw manuscript → AI understands its structure → formatting rules are applied automatically → download a publication-ready file.

Zero manual intervention. Zero formatting errors.

---

## 🔑 Key Features

- 🧠 **Context-Aware AI** — Google Gemini dynamically identifies titles, subheadings, captions, and body text without relying on existing metadata
- 🎨 **Precision Formatting** — enforces typography (Times New Roman, exact pt sizes), layout (1.5 spacing, 1-inch margins), and alignment (justified text, centered figures/tables)
- ☁️ **Secure Cloud Architecture** — authenticated user dashboard backed by MongoDB; memory-only file processing for data privacy
- ⚡ **One-Click Download** — get your formatted `.docx` in seconds

---

## 🛠️ How It Works

```
1. UPLOAD   → Raw .docx parsed into memory
2. ANALYZE  → Text chunks sent to Gemini for structural classification
3. EXECUTE  → python-docx rewrites internal XML to match target specs
4. DELIVER  → Download publication-ready file instantly
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| AI / LLM | Google Gemini API |
| Document Processing | python-docx |
| Backend | Python / FastAPI |
| Database | MongoDB |
| Auth | JWT / Session-based |

---

## 🗺️ Roadmap

- [x] Core formatting engine (Phase 1)
- [x] User authentication + dashboard (Phase 2)
- [ ] Automated reference parsing — IEEE, APA citation matching (Phase 3)
- [ ] Multi-format export — simultaneous `.docx` + `.pdf` output
- [ ] User history dashboard — cloud repository of formatted manuscripts

---

## 🚀 Getting Started

```bash
git clone https://github.com/Salini-Natarajan/Manuscript-MVP.git
cd Manuscript-MVP

pip install -r requirements.txt

# Add your Gemini API key to .env
echo "GEMINI_API_KEY=your_key_here" > .env

python app.py
```

---

## 👩‍💻 Built By

**Salini N** — AIML Student, KPR Institute of Engineering and Technology
[LinkedIn](https://linkedin.com/in/salininatarajan) · [GitHub](https://github.com/Salini-Natarajan)
