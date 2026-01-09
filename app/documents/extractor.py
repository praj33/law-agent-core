import re

def extract_legal_facts(text: str) -> dict:
    facts = {}

    # Dates
    dates = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text)
    if dates:
        facts["dates"] = dates[:5]

    # Money amounts
    amounts = re.findall(r"₹\s?\d+(?:,\d+)*(?:\.\d+)?", text)
    if amounts:
        facts["amounts"] = amounts[:5]

    # Parties (very simple heuristic)
    if "landlord" in text.lower():
        facts["party_1"] = "landlord"
    if "tenant" in text.lower():
        facts["party_2"] = "tenant"

    return facts
