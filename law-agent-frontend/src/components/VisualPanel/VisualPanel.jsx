import CourtProcessFlow from "./CourtProcessFlow";

export default function VisualPanel({ domain }) {
  if (!domain) {
    return (
      <div className="card" style={{ opacity: 0.6 }}>
        <h3>🧭 Court Process Flow</h3>
        <p className="subtext">
          Ask a legal question to view how the legal process unfolds.
        </p>
      </div>
    );
  }

  const flows = {
    rent_dispute: [
      "Legal Notice",
      "Waiting Period",
      "Case Filing",
      "Court Hearing",
      "Final Order"
    ],
    family_law: [
      "Dispute Identified",
      "Mediation",
      "Petition Filing",
      "Court Hearings",
      "Judgment"
    ],
    employment_law: [
      "Issue Raised",
      "Internal Complaint",
      "Legal Notice",
      "Labour Court",
      "Resolution"
    ]
  };

  const steps = flows[domain] || [
    "Issue Identified",
    "Legal Consultation",
    "Formal Action",
    "Resolution"
  ];

  return (
    <div className="card">
      <h3>🧭 Court Process Flow</h3>

      <p className="subtext">
        Visual explanation for <b>{domain.replace("_", " ")}</b>
      </p>

      <CourtProcessFlow steps={steps} />

      <p className="subtext" style={{ marginTop: 12 }}>
        This visualization explains the *procedural path* of a legal case.
        It does not predict outcomes.
      </p>
    </div>
  );
}
