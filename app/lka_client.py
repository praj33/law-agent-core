import requests

LKA_BASE_URL = "http://nyaya-core/lka"

def get_domain(domain_id: str):
    res = requests.get(f"{LKA_BASE_URL}/domains/{domain_id}")
    res.raise_for_status()
    return res.json()

def get_routes_for_domain(domain_id: str):
    res = requests.get(
        f"{LKA_BASE_URL}/routes",
        params={"domain": domain_id}
    )
    res.raise_for_status()
    return res.json()

def get_procedure(procedure_id: str):
    res = requests.get(f"{LKA_BASE_URL}/procedure/{procedure_id}")
    res.raise_for_status()
    return res.json()

def get_outcome_signal(procedure_id: str):
    res = requests.get(f"{LKA_BASE_URL}/outcomes/{procedure_id}")
    res.raise_for_status()
    return res.json()
