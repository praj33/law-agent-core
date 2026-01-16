import json
import os
from typing import Optional, Dict, Any, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "nyaya_data")


# -------------------------
# INTERNAL HELPERS
# -------------------------

def _load_json(country: str, filename: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(DATA_DIR, country, filename)

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# -------------------------
# PUBLIC DATA ACCESS API
# -------------------------

def get_domain(country: str, domain_id: str) -> Optional[Dict[str, Any]]:
    data = _load_json(country, "domains.json")
    if not data:
        return None
    return data.get(domain_id)


def get_routes(country: str, domain_id: str) -> Optional[List[Dict[str, Any]]]:
    data = _load_json(country, "routes.json")
    if not data:
        return None
    return data.get(domain_id)


def get_procedure(country: str, procedure_id: str) -> Optional[Dict[str, Any]]:
    data = _load_json(country, "procedures.json")
    if not data:
        return None
    return data.get(procedure_id)


def get_timeline(country: str, route_id: str) -> Optional[List[Dict[str, Any]]]:
    data = _load_json(country, "timelines.json")
    if not data:
        return None
    return data.get(route_id)


def get_evidence(country: str, route_id: str) -> Optional[Dict[str, Any]]:
    data = _load_json(country, "evidence.json")
    if not data:
        return None
    return data.get(route_id)


def get_glossary(country: str, domain_id: str) -> Optional[Dict[str, Any]]:
    data = _load_json(country, "glossary.json")
    if not data:
        return None
    return data.get(domain_id)
