export default function StepsView({ steps = [] }) {
  if (!steps.length) return null;

  return (
    <div style={{ marginTop: 25 }}>
      <h3>📋 What You Should Do Next</h3>

      <ol style={{ paddingLeft: 20 }}>
        {steps.map((step, i) => (
          <li
            key={i}
            style={{
              marginBottom: 8,
              background: "#262626",
              padding: 10,
              borderRadius: 6
            }}
          >
            {step}
          </li>
        ))}
      </ol>
    </div>
  );
}
