## ⚖️ Law Agent — Explainable AI Legal Assistant

An explainable, reinforcement-learning–powered legal assistant that helps users understand legal situations, recommended actions, timelines, and court processes through a structured UI and visual explanations.

This is not a chatbot.
It is a decision-support system with memory, feedback, and explainability.

## 🚀 Key Features
### 🧠 Reinforcement Learning + Agent Memory

- Lightweight RL using reward-memory / Q-table style averaging

- State = legal domain + user type + region

- Action = legal route (notice, negotiation, filing)

- Reward = user feedback (👍 / 👎) + engagement time

- Decisions stabilize over time instead of changing randomly

### 💬 Explainable Law Agent Interface (React)

- Clean chatbot-style input

- Structured responses:

- Legal domain

- Recommended action

- Step-by-step guidance

- Estimated timelines

- Legal glossary

- Designed for non-lawyers

### 🎥 Visual Court Process Flow (R3F)

- Animated React Three Fiber visualization

- Shows procedural legal journey:
```
- Notice → Waiting → Filing → Hearing → Order
```
- Highlights current stage

- Helps users understand where they are in the legal process

- Visuals are explanatory, not predictive

### 📄 Document Upload & Parsing

- Upload legal documents (PDFs)

- Text extraction using PyMuPDF / PDF.js

- Parsed content feeds domain classification

- Reduces dependence on user wording

### 📊 Feedback Analytics Dashboard

- Tracks:

- Which legal routes perform best

- Average reward per action

- Usage frequency

- Enables internal monitoring and tuning

- Designed for legal teams and admins

### 🏗️ System Architecture
```
Frontend (React + R3F)
│
├─ ChatPanel (user input)
├─ ResponsePanel (steps, timeline, glossary)
├─ VisualPanel (court process animation)
│
Backend (FastAPI)
│
├─ Domain classification
├─ Decision engine (state → action)
├─ Agent memory (reward-based)
├─ Feedback ingestion
├─ Document parsing
│
Database (SQLite)
└─ Stores agent memory & rewards
```
### 🧪 Reinforcement Learning Design

This system intentionally uses lightweight RL, not deep learning:

- Deterministic and safe for legal use

- No hallucination or unsafe exploration

- Learns preferences, not laws

- Easy to audit and explain

This design is more appropriate for law than black-box models.

### 🛠️ Tech Stack
#### Backend

- Python

- FastAPI

- SQLAlchemy

- SQLite

- PyMuPDF

Frontend

- React (Vite)

- React Three Fiber (R3F)

- Drei

- CSS (custom, product-grade)

▶️ Running the Project Locally
Backend
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on:
```
http://127.0.0.1:8000
```

Frontend

```
npm install
npm run dev
```

Frontend runs on:
```
http://localhost:5173
```

## 🧪 Demo Flow

1. Ask a legal question (e.g. eviction without notice)

2. Agent classifies domain

3. Agent recommends an action

4. Steps, timeline, glossary are shown

5. Animated court process visual explains procedure

6. User gives feedback (👍 / 👎)

7. Agent memory updates

8. Same question stabilizes to better action over time

## 🎯 Why This Is Different

| Traditional Chatbots | Law Agent System |
|---------------------|------------------|
| Free-form text answers | Structured legal response schema (domain, action, steps, timeline, glossary) |
| Stateless per request | Persistent reinforcement-learning memory per legal state |
| Implicit reasoning | Explicit procedural steps and time estimates |
| Text-only interaction | Animated court process visualization (React Three Fiber) |
| Probabilistic text generation | Deterministic action selection from a fixed legal route set |

### 🧠 Design Philosophy

This system intentionally avoids open-ended text generation for legal advice.

Instead, it uses:
- structured decision logic  
- feedback-driven learning  
- procedural explanations  
- visual representations of legal processes  

to ensure **consistency, safety, and user trust**.

## ⚠️ Disclaimer

This system provides informational guidance only.

### 🏁 Status

✅ Core system complete
✅ Explainable
✅ Feedback-driven
✅ Visualized

### 📌 Author

Built as part of an AI systems project focused on safe, explainable decision-making for legal assistance.