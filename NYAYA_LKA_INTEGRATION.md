# Nyaya LKA Integration Notes — Day 1

## Domain Source
- Endpoint: GET /lka/domains
- Used for: domain_id, jurisdiction, statutes

## Legal Routes Source
- Endpoint: GET /lka/routes?domain={domain_id}
- Used for: action space for RL

## Procedures Source
- Endpoint: GET /lka/procedure/{procedure_id}
- Used for: steps, timelines, escalation paths

## Glossary Source
- Endpoint: GET /lka/glossary/{term}
- Used for: legal definitions in responses

## Evidence Source
- Endpoint: GET /lka/evidence/{procedure_id}
- Used for: audit + document requirements

## Outcome Signals (RL)
- Endpoint: GET /lka/outcomes/{procedure_id}
- Used for: reward shaping, penalties, confidence
