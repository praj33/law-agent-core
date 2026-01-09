export default function TimelineView({ timeline = [] }) {
  if (!timeline.length) return null;

  return (
    <div style={{ marginTop: 25 }}>
      <h3>🗓 Estimated Timeline</h3>

      {timeline.map((item, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "8px 10px",
            marginBottom: 6,
            background: "#262626",
            borderRadius: 6
          }}
        >
          <span>{item.label}</span>
          <b>{item.days} days</b>
        </div>
      ))}
    </div>
  );
}
