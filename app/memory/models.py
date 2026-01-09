from sqlalchemy import Column, String, Float, Integer
from app.db.session import Base

class AgentMemory(Base):
    __tablename__ = "agent_memory"

    state_key = Column(String, primary_key=True)
    action_key = Column(String, primary_key=True)

    total_reward = Column(Float, default=0.0)
    times_used = Column(Integer, default=0)
    avg_reward = Column(Float, default=0.0)
