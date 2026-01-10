def adapt_decision_for_assistant(decision: dict) -> dict:
    route = decision["chosen_route"]
    procedures = decision["procedures"]
    evidence = decision["evidence"]

    steps = []
    timeline = []

    for proc in procedures:
        for step in proc["steps"]:
            steps.append({
                "label": step["action"],
                "statute": step["statute"]
            })
            timeline.append({
                "label": step["action"],
                "min_days": step["min_days"],
                "max_days": step["max_days"]
            })

    glossary_terms = set()
    for proc in procedures:
        for step in proc["steps"]:
            glossary_terms.add(step["action"])

    return {
        "meta": {
            "jurisdiction": decision["jurisdiction"],
            "domain_id": decision["domain_id"],
            "route_id": route["route_id"],
        },
        "recommendation": {
            "title": route["route_name"],
            "confidence_band": decision["outcomes"][0]["success_range"]
        },
        "steps": steps,
        "timeline": timeline,
        "evidence_required": evidence,
        "disclaimer": "This is not legal advice. Generated for informational purposes."
    }
