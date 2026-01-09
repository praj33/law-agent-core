import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function ChatPanel({ onResult }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  async function onAsk() {
    if (!query.trim()) return;

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/decide`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_type: "citizen",
          region: "india",
          user_input: query,
          candidate_actions: [
            "send_legal_notice",
            "negotiate_settlement",
            "file_eviction_case"
          ]
        })
      });

      const data = await res.json();

      // Build structured result for ResponsePanel
      const structuredResult = {
        domain: data.domain,
        chosen_action: data.chosen_action,
        state_key: data.state_key,
        steps: [
          "Understand your legal position",
          "Prepare a legal notice",
          "Send notice via an advocate",
          "Wait for response or escalation"
        ],
        timeline: [
          { label: "Notice drafting", days: 3 },
          { label: "Notice period", days: 15 },
          { label: "Next legal step", days: 30 }
        ],
        glossary: {
          "Legal Notice": "A formal written communication asserting legal rights.",
          "Eviction": "The legal process of removing a tenant from property."
        }
      };

      onResult(structuredResult);
    } catch (error) {
      console.error("Law Agent error:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>⚖️ Ask the Law Agent</h2>

      <p className="subtext">
        Describe your legal issue in simple words. The agent will analyze the
        situation and guide you with next steps.
      </p>

      <textarea
        rows={4}
        placeholder="e.g. My landlord is forcing eviction without notice"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* THIS IS THE BUTTON YOU ASKED ABOUT */}
      <button
        className="button-primary"
        onClick={onAsk}
        disabled={loading || !query}
      >
        {loading ? "Analyzing…" : "Ask Law Agent"}
      </button>
    </div>
  );
}
