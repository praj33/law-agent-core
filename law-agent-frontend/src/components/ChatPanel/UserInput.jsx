export default function UserInput({ query, setQuery, onAsk, loading }) {
  return (
    <div>
      <textarea
        rows={4}
        placeholder="Describe your legal issue..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />

      <button onClick={onAsk} disabled={loading || !query}>
        {loading ? "Analyzing…" : "Ask Law Agent"}
      </button>
    </div>
  );
}
