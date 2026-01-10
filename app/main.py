from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List, Optional
import fitz  # PyMuPDF
import re

# =====================================================
# CONFIG
# =====================================================
DATABASE_URL = "sqlite:///./law_agent.db"

# =====================================================
# DATABASE SETUP
# =====================================================
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# =====================================================
# AGENT MEMORY (RL TABLE)
# =====================================================
class AgentMemory(Base):
    __tablename__ = "agent_memory"

    state_key = Column(String, primary_key=True)
    action_key = Column(String, primary_key=True)
    total_reward = Column(Float, default=0.0)
    times_used = Column(Integer, default=0)
    avg_reward = Column(Float, default=0.0)

Base.metadata.create_all(bind=engine)

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(title="Nyaya RL Decision Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

# =====================================================
# DB DEPENDENCY
# =====================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# REQUEST SCHEMAS
# =====================================================
class DecisionRequest(BaseModel):
    user_type: str
    jurisdiction: str
    domain_id: str
    case_summary: str


class FeedbackRequest(BaseModel):
    state_key: str
    action_key: str
    vote: Optional[str] = None
    time_spent: int = 0
    follow_up: bool = False

# =====================================================
# LOCAL NYAYA LKA STUB (STRICT CONTRACT)
# =====================================================
LKA_ROUTES = {
    "IN_RENT_EVICTION": [
        {
            "route_id": "IN_EVICTION_NOTICE",
            "domain_id": "IN_RENT_EVICTION",
            "route_name": "Legal Eviction via Notice",
            "procedure_ids": [
                "IN_EVICT_NOTICE",
                "IN_EVICT_FILE",
                "IN_EVICT_HEARING"
            ]
        }
    ]
}

LKA_PROCEDURES = {
    "IN_EVICT_NOTICE": {
        "procedure_id": "IN_EVICT_NOTICE",
        "steps": [
            {
                "step": 1,
                "action": "Serve legal notice",
                "statute": "TPA Section 106",
                "min_days": 15,
                "max_days": 30
            }
        ],
        "failure_paths": ["NO_RESPONSE", "INVALID_NOTICE"],
        "appeal_available": True
    },
    "IN_EVICT_FILE": {
        "procedure_id": "IN_EVICT_FILE",
        "steps": [
            {
                "step": 1,
                "action": "File eviction suit",
                "statute": "Rent Control Act",
                "min_days": 30,
                "max_days": 90
            }
        ],
        "failure_paths": ["CASE_DISMISSED"],
        "appeal_available": True
    },
    "IN_EVICT_HEARING": {
        "procedure_id": "IN_EVICT_HEARING",
        "steps": [
            {
                "step": 1,
                "action": "Court hearing",
                "statute": "Civil Procedure Code",
                "min_days": 60,
                "max_days": 180
            }
        ],
        "failure_paths": ["ADJOURNMENT"],
        "appeal_available": True
    }
}

LKA_EVIDENCE = {
    pid: {
        "procedure_id": pid,
        "required_documents": [
            "Rent Agreement",
            "Ownership Proof",
            "Previous Notices"
        ],
        "optional_documents": ["Witness affidavit"]
    }
    for pid in LKA_PROCEDURES
}

LKA_OUTCOMES = {
    pid: {
        "procedure_id": pid,
        "success_range": [0.55, 0.75],
        "escalation_risk": 0.2,
        "wrong_route_penalty": 0.4
    }
    for pid in LKA_PROCEDURES
}

# =====================================================
# RL CORE
# =====================================================
def build_state_key(jurisdiction: str, domain_id: str, user_type: str) -> str:
    return f"{jurisdiction}|{domain_id}|{user_type}".lower()


def calculate_reward(vote, time_spent, follow_up):
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


def update_memory(db, state_key, action_key, reward):
    record = db.query(AgentMemory).filter(
        AgentMemory.state_key == state_key,
        AgentMemory.action_key == action_key
    ).first()

    if not record:
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


def select_best_route(db, state_key, routes):
    memories = db.query(AgentMemory).filter(
        AgentMemory.state_key == state_key
    ).all()

    score_map = {m.action_key: m.avg_reward for m in memories}

    best = routes[0]
    best_score = score_map.get(best["route_id"], 0.0)

    for r in routes:
        score = score_map.get(r["route_id"], 0.0)
        if score > best_score:
            best = r
            best_score = score

    return best

# =====================================================
# DOCUMENT PARSER
# =====================================================
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_legal_facts(text):
    facts = {}
    dates = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text)
    if dates:
        facts["dates"] = dates[:5]

    amounts = re.findall(r"₹\s?\d+(?:,\d+)*(?:\.\d+)?", text)
    if amounts:
        facts["amounts"] = amounts[:5]

    return facts

# =====================================================
# API: DECISION
# =====================================================
@app.post("/api/v1/decision")
def make_decision(payload: DecisionRequest, db: Session = Depends(get_db)):
    state_key = build_state_key(
        payload.jurisdiction,
        payload.domain_id,
        payload.user_type
    )

    routes = LKA_ROUTES.get(payload.domain_id)
    if not routes:
        raise HTTPException(400, "No legal routes available")

    chosen_route = select_best_route(db, state_key, routes)

    procedures = [
        LKA_PROCEDURES[pid]
        for pid in chosen_route["procedure_ids"]
    ]

    evidence = [
        LKA_EVIDENCE[p["procedure_id"]]
        for p in procedures
    ]

    outcomes = [
        LKA_OUTCOMES[p["procedure_id"]]
        for p in procedures
    ]

    return {
        "state_key": state_key,
        "jurisdiction": payload.jurisdiction,
        "domain_id": payload.domain_id,
        "chosen_route": chosen_route,
        "procedures": procedures,
        "evidence": evidence,
        "outcomes": outcomes
    }

# =====================================================
# API: FEEDBACK
# =====================================================
@app.post("/api/v1/feedback")
def feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    reward = calculate_reward(
        payload.vote,
        payload.time_spent,
        payload.follow_up
    )
    update_memory(
        db,
        payload.state_key,
        payload.action_key,
        reward
    )
    return {"status": "recorded", "reward": reward}

# =====================================================
# API: DOCUMENT UPLOAD
# =====================================================
@app.post("/api/v1/upload")
async def upload_document(file: UploadFile = File(...)):
    text = extract_text_from_pdf(await file.read())
    facts = extract_legal_facts(text)
    return {
        "facts": facts,
        "preview": text[:1000]
    }

# =====================================================
# HEALTH
# =====================================================
@app.get("/")
def health():
    return {"status": "Nyaya RL Decision Engine running"}
