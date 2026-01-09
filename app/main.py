from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List, Optional
import fitz  # PyMuPDF
import re

# -----------------------------
# DATABASE SETUP
# -----------------------------
DATABASE_URL = "sqlite:///./law_agent.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------
# AGENT MEMORY MODEL
# -----------------------------
class AgentMemory(Base):
    __tablename__ = "agent_memory"

    state_key = Column(String, primary_key=True)
    action_key = Column(String, primary_key=True)
    total_reward = Column(Float, default=0.0)
    times_used = Column(Integer, default=0)
    avg_reward = Column(Float, default=0.0)

Base.metadata.create_all(bind=engine)

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="Law Agent Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DB DEPENDENCY
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# INPUT SCHEMAS
# -----------------------------
class DecideRequest(BaseModel):
    user_type: str
    region: str
    user_input: str
    candidate_actions: List[str]

class FeedbackRequest(BaseModel):
    state_key: str
    action_key: str
    vote: Optional[str] = None
    time_spent: int = 0
    follow_up: bool = False

# -----------------------------
# DOMAIN CLASSIFIER
# -----------------------------
def classify_domain(text: str) -> str:
    text = text.lower()

    if "rent" in text or "tenant" in text or "landlord" in text:
        return "rent_dispute"
    if "divorce" in text or "marriage" in text:
        return "family_law"
    if "job" in text or "salary" in text or "termination" in text:
        return "employment_law"

    return "general_legal"

# -----------------------------
# STATE KEY BUILDER
# -----------------------------
def build_state_key(user_type: str, region: str, domain: str) -> str:
    return f"{domain}|{user_type}|{region}".lower()

# -----------------------------
# REWARD CALCULATOR
# -----------------------------
def calculate_reward(vote: Optional[str], time_spent: int, follow_up: bool) -> float:
    reward = 0.0
    if vote == "up":
        reward += 1.0
    elif vote == "down":
        reward -= 1.0
    if time_spent > 60:
        reward += 0.5
    if follow_up:
        reward += 0.3
    return reward

# -----------------------------
# MEMORY UPDATE
# -----------------------------
def update_agent_memory(db: Session, state_key: str, action_key: str, reward: float):
    record = db.query(AgentMemory).filter(
        AgentMemory.state_key == state_key,
        AgentMemory.action_key == action_key
    ).first()

    if record is None:
        record = AgentMemory(
            state_key=state_key,
            action_key=action_key,
            total_reward=reward,
            times_used=1,
            avg_reward=reward
        )
        db.add(record)
    else:
        record.total_reward += reward
        record.times_used += 1
        record.avg_reward = record.total_reward / record.times_used

    db.commit()

# -----------------------------
# ACTION SELECTION
# -----------------------------
def select_best_action(db: Session, state_key: str, candidate_actions: List[str]) -> str:
    memories = db.query(AgentMemory).filter(
        AgentMemory.state_key == state_key
    ).all()

    scores = {m.action_key: m.avg_reward for m in memories}

    best_action = candidate_actions[0]
    best_score = scores.get(best_action, 0.0)

    for action in candidate_actions:
        score = scores.get(action, 0.0)
        if score > best_score:
            best_score = score
            best_action = action

    return best_action

# -----------------------------
# PDF PARSER
# -----------------------------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# -----------------------------
# LEGAL FACT EXTRACTOR
# -----------------------------
def extract_legal_facts(text: str) -> dict:
    facts = {}

    dates = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text)
    if dates:
        facts["dates"] = dates[:5]

    amounts = re.findall(r"₹\s?\d+(?:,\d+)*(?:\.\d+)?", text)
    if amounts:
        facts["amounts"] = amounts[:5]

    if "landlord" in text.lower():
        facts["party_1"] = "landlord"
    if "tenant" in text.lower():
        facts["party_2"] = "tenant"

    return facts

# -----------------------------
# API: DECIDE
# -----------------------------
@app.post("/decide")
def decide_action(payload: DecideRequest, db: Session = Depends(get_db)):
    domain = classify_domain(payload.user_input)
    state_key = build_state_key(
        payload.user_type,
        payload.region,
        domain
    )

    action = select_best_action(
        db,
        state_key,
        payload.candidate_actions
    )

    return {
        "state_key": state_key,
        "domain": domain,
        "chosen_action": action
    }

# -----------------------------
# API: FEEDBACK
# -----------------------------
@app.post("/feedback")
def submit_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    reward = calculate_reward(
        payload.vote,
        payload.time_spent,
        payload.follow_up
    )
    update_agent_memory(
        db,
        payload.state_key,
        payload.action_key,
        reward
    )
    return {"status": "recorded", "reward": reward}

# -----------------------------
# API: DOCUMENT UPLOAD
# -----------------------------
@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()

    text = extract_text_from_pdf(file_bytes)
    facts = extract_legal_facts(text)
    domain = classify_domain(text)

    return {
        "domain": domain,
        "facts": facts,
        "text_preview": text[:1000]
    }

# -----------------------------
# ANALYTICS: TOP ACTIONS
# -----------------------------
@app.get("/analytics/top-actions")
def top_actions(limit: int = 10, db: Session = Depends(get_db)):
    records = (
        db.query(AgentMemory)
        .order_by(AgentMemory.avg_reward.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "state_key": r.state_key,
            "action_key": r.action_key,
            "avg_reward": r.avg_reward,
            "times_used": r.times_used
        }
        for r in records
    ]


# -----------------------------
# ANALYTICS: WORST ACTIONS
# -----------------------------
@app.get("/analytics/worst-actions")
def worst_actions(limit: int = 10, db: Session = Depends(get_db)):
    records = (
        db.query(AgentMemory)
        .order_by(AgentMemory.avg_reward.asc())
        .limit(limit)
        .all()
    )

    return [
        {
            "state_key": r.state_key,
            "action_key": r.action_key,
            "avg_reward": r.avg_reward,
            "times_used": r.times_used
        }
        for r in records
    ]


# -----------------------------
# ANALYTICS: STATE SUMMARY
# -----------------------------
@app.get("/analytics/state/{state_key}")
def state_summary(state_key: str, db: Session = Depends(get_db)):
    records = (
        db.query(AgentMemory)
        .filter(AgentMemory.state_key == state_key)
        .all()
    )

    return [
        {
            "action_key": r.action_key,
            "avg_reward": r.avg_reward,
            "times_used": r.times_used
        }
        for r in records
    ]

# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def root():
    return {"status": "law-agent core running"}
