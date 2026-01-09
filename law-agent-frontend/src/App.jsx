import { useState } from "react";
import ChatPanel from "./components/ChatPanel/ChatPanel";
import ResponsePanel from "./components/ResponsePanel/ResponsePanel";
import VisualPanel from "./components/VisualPanel/VisualPanel";
import "./App.css";

export default function App() {
  const [agentResult, setAgentResult] = useState(null);

  return (
    <div className="app">
      <div className="app-content">
        {/* HEADER */}
        <header>
          <h1>⚖️ Law Agent</h1>
          <p className="subtext">
            Evidence-driven legal guidance with explainable steps and timelines.
          </p>
        </header>

        {/* MAIN GRID */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.2fr 1fr",
            gap: 30,
            marginTop: 30
          }}
        >
          {/* LEFT: CHAT + RESPONSE */}
          <div>
            <ChatPanel onResult={setAgentResult} />

            {agentResult && (
              <ResponsePanel result={agentResult} />
            )}
          </div>

          {/* RIGHT: VISUAL PANEL */}
          <div>
            <VisualPanel domain={agentResult?.domain} />
          </div>
        </div>

        {/* FOOTER */}
        <footer className="disclaimer">
          This is not legal advice. Generated for informational purposes only.
        </footer>
      </div>
    </div>
  );
}
