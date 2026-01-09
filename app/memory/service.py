from sqlalchemy.orm import Session
from app.memory.models import AgentMemory

def update_agent_memory(
    db: Session,
    state_key: str,
    action_key: str,
    reward: float
):
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
