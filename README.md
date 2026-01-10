# Nyaya RL Decision Engine

A jurisdiction-aware, reinforcement-learning powered legal decision engine built as part of Nyaya’s sovereign legal intelligence system.

This system does **not** generate legal advice.
It deterministically selects **legal routes, procedures, evidence, and timelines** from Nyaya’s Legal Knowledge API (LKA).

---

## 🎯 Why This Is Different

| Chatbots | Nyaya RL Decision Engine |
|--------|-------------------------|
| Free-form answers | Structured legal decisions |
| Hallucinated law | Dataset-backed legal routes |
| No memory | Reinforcement-learning memory |
| No explainability | Steps, timelines, evidence |
| Unsafe fallbacks | Deterministic failure handling |
| Single jurisdiction | Jurisdiction-aware routing |

---

## 🧠 System Architecture

User Request
↓
State Builder (jurisdiction + domain + user type)
↓
Nyaya Legal Knowledge API (LKA)
↓
Route Selection (RL memory)
↓
Procedures + Evidence + Outcomes
↓
Structured JSON Response


The engine **never invents law** and **never bypasses LKA**.

---

## 🧩 Core Concepts

### State
<jurisdiction>|<domain_id>|<user_type>


Example:
IN|IN_RENT_EVICTION|LAWYER


---

### Action
A **legal route** provided by Nyaya LKA.

Example:
IN_EVICTION_NOTICE

---

### Reward
Derived from:
- User feedback (up / down)
- Time spent
- Follow-up actions

Stored in a persistent RL memory table.

---

## 🌍 Jurisdiction Safety

- Each jurisdiction is isolated
- If LKA does not expose routes for a jurisdiction, the engine **fails safely**
- No fallback, no hallucination, no cross-country leakage

This behavior is **intentional and required**.

---

## 📡 API Endpoints

### Decision API

POST /api/v1/decision

Request:
```json
{
  "user_type": "citizen",
  "jurisdiction": "IN",
  "domain_id": "IN_RENT_EVICTION",
  "case_summary": "Tenant has not paid rent for 4 months"
}
```
Response:

Chosen legal route

Procedures with steps & timelines

Evidence requirements

Outcome probabilities

### Feedback API
```json
POST /api/v1/feedback
```

Used to reinforce future decisions.

### Document Upload API
```json
POST /api/v1/upload
```

Extracts structured legal facts from uploaded PDFs.

### 🧪 Demo Scenarios

✅ India (Working)

Domain: IN_RENT_EVICTION

Routes returned from LKA

RL selects optimal route

Procedures, evidence, outcomes returned

### ⛔ UK (Safely Blocked)

Domain: UK_RENT_EVICTION

No routes in LKA

Engine returns:

```json
{
  "detail": "No legal routes available"
}
```


This proves jurisdiction safety and non-hallucination.

### 🏛️ Compliance Guarantees

No keyword-based domain detection

No hardcoded statutes

No invented legal routes

Full traceability of decisions