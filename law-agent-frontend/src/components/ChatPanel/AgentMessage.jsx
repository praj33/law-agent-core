export default function AgentMessage({ domain, action }) {
  return (
    <div style={{ marginTop: 20 }}>
      <p><b>Legal Domain:</b> {domain}</p>
      <p><b>Recommended Action:</b> {action}</p>
    </div>
  );
}
