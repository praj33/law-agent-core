from fastapi import FastAPI, Query

app = FastAPI(title="Nyaya Legal Knowledge API (Stub)")

# -----------------------------
# DOMAIN ONTOLOGY
# -----------------------------
@app.get("/lka/domains")
def list_domains():
    return [
        {
            "domain_id": "IN_RENT_EVICTION",
            "country": "IN",
            "name": "Tenant Eviction",
            "statutes": [
                "Transfer of Property Act",
                "Rent Control Act"
            ],
            "parent_domain": "IN_PROPERTY"
        }
    ]


@app.get("/lka/domains/{domain_id}")
def get_domain(domain_id: str):
    return {
        "domain_id": domain_id,
        "country": "IN",
        "name": "Tenant Eviction",
        "statutes": [
            "Transfer of Property Act",
            "Rent Control Act"
        ],
        "parent_domain": "IN_PROPERTY"
    }


# -----------------------------
# LEGAL ROUTES
# -----------------------------
@app.get("/lka/routes")
def get_routes(domain: str = Query(...)):
    return [
        {
            "route_id": "IN_EVICTION_NOTICE",
            "domain_id": domain,
            "route_name": "Legal Eviction via Notice",
            "procedure_ids": [
                "IN_EVICT_NOTICE",
                "IN_EVICT_FILE",
                "IN_EVICT_HEARING"
            ]
        }
    ]


@app.get("/lka/routes/{route_id}")
def get_route(route_id: str):
    return {
        "route_id": route_id,
        "domain_id": "IN_RENT_EVICTION",
        "route_name": "Legal Eviction via Notice",
        "procedure_ids": [
            "IN_EVICT_NOTICE",
            "IN_EVICT_FILE",
            "IN_EVICT_HEARING"
        ]
    }


# -----------------------------
# PROCEDURES
# -----------------------------
@app.get("/lka/procedure/{procedure_id}")
def get_procedure(procedure_id: str):
    return {
        "procedure_id": procedure_id,
        "steps": [
            {
                "step": 1,
                "action": "Serve legal notice",
                "statute": "TPA Section 106",
                "min_days": 15,
                "max_days": 30
            }
        ],
        "failure_paths": [
            "NO_RESPONSE",
            "INVALID_NOTICE"
        ],
        "appeal_available": True
    }


# -----------------------------
# GLOSSARY
# -----------------------------
@app.get("/lka/glossary/{term}")
def glossary(term: str):
    return {
        "term": term,
        "definition": "Removal of a tenant through lawful court process",
        "statutes": [
            "Transfer of Property Act"
        ],
        "jurisdiction": ["IN"]
    }


# -----------------------------
# EVIDENCE REQUIREMENTS
# -----------------------------
@app.get("/lka/evidence/{procedure_id}")
def evidence(procedure_id: str):
    return {
        "procedure_id": procedure_id,
        "required_documents": [
            "Rent Agreement",
            "Ownership Proof",
            "Previous Notices"
        ],
        "optional_documents": [
            "Witness affidavit"
        ]
    }


# -----------------------------
# OUTCOME PROBABILITIES
# -----------------------------
@app.get("/lka/outcomes/{procedure_id}")
def outcomes(procedure_id: str):
    return {
        "procedure_id": procedure_id,
        "success_range": [0.55, 0.75],
        "escalation_risk": 0.2,
        "wrong_route_penalty": 0.4
    }
