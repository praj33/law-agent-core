const API_BASE = "http://127.0.0.1:8000";

export default function FeedbackButtons({ stateKey, action }) {
  async function sendFeedback(vote) {
    await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        state_key: stateKey,
        action_key: action,
        vote,
        time_spent: 120,
        follow_up: false
      })
    });
  }

  return (
    <div style={{ marginTop: 10 }}>
      <button onClick={() => sendFeedback("up")}>👍 Helpful</button>
      <button onClick={() => sendFeedback("down")} style={{ marginLeft: 10 }}>
        👎 Not Helpful
      </button>
    </div>
  );
}
