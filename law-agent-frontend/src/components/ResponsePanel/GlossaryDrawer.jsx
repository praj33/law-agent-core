import { useState } from "react";

export default function GlossaryDrawer({ glossary = {} }) {
  const [open, setOpen] = useState(false);
  const entries = Object.entries(glossary);

  if (!entries.length) return null;

  return (
    <div style={{ marginTop: 25 }}>
      <h3
        style={{ cursor: "pointer" }}
        onClick={() => setOpen(!open)}
      >
        📚 Legal Terms {open ? "▲" : "▼"}
      </h3>

      {open && (
        <ul style={{ paddingLeft: 20 }}>
          {entries.map(([term, meaning]) => (
            <li key={term} style={{ marginBottom: 8 }}>
              <b>{term}</b>: {meaning}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
