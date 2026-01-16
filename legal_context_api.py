from typing import Optional, Dict, Any, List

from nyaya_loader import (
    get_domain,
    get_routes,
    get_procedure,
    get_timeline,
    get_evidence,
    get_glossary,
)


def get_legal_context(
    country: str,
    domain_id: str,
    route_id: str
) -> Optional[Dict[str, Any]]:
    """
    Assemble a legal context object strictly from Nyaya datasets.

    Rules:
    - No inference
    - No fallback
    - No defaults
    - If any required data is missing → return None
    """

    # 1. Domain
    domain = get_domain(country, domain_id)
    if domain is None:
        return None

    # 2. Routes
    routes = get_routes(country, domain_id)
    if routes is None:
        return None

    route = next((r for r in routes if r.get("route_id") == route_id), None)
    if route is None:
        return None

    # 3. Procedures
    procedures: List[Dict[str, Any]] = []
    statutes = set()

    for pid in route.get("procedure_ids", []):
        procedure = get_procedure(country, pid)
        if procedure is None:
            return None

        procedures.append(procedure)

        for step in procedure.get("steps", []):
            statute = step.get("statute")
            if statute:
                statutes.add(statute)

    # 4. Timeline
    timeline = get_timeline(country, route_id)
    if timeline is None:
        return None

    # 5. Evidence
    evidence = get_evidence(country, route_id)
    if evidence is None:
        return None

    # 6. Assemble canonical legal context
    return {
        "country": country,
        "domain": domain_id,
        "route": route_id,
        "procedure": procedures,
        "timeline": timeline,
        "evidence": evidence,
        "statutes": list(statutes),
    }
