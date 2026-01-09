import StepsView from "./StepsView";
import TimelineView from "./TimelineView";
import GlossaryDrawer from "./GlossaryDrawer";

export default function ResponsePanel({ result }) {
  if (!result) return null;

  return (
    <div
      style={{
        marginTop: 30,
        padding: 20,
        borderRadius: 10,
        background: "#1f1f1f",
        border: "1px solid #333"
      }}
    >
      <h2 style={{ marginBottom: 10 }}>🧠 Legal Assessment</h2>

      <p style={{ opacity: 0.9 }}>
        Based on your situation, this appears to be a
        <b> {result.domain.replace("_", " ")} </b>
        case.
      </p>

      <div
        style={{
          marginTop: 10,
          padding: 12,
          background: "#262626",
          borderRadius: 6
        }}
      >
        <b>Recommended Action:</b>
        <div style={{ fontSize: 18, marginTop: 4 }}>
          {result.chosen_action.replaceAll("_", " ")}
        </div>
      </div>

      <StepsView steps={result.steps} />
      <TimelineView timeline={result.timeline} />
      <GlossaryDrawer glossary={result.glossary} />
    </div>
  );
}
