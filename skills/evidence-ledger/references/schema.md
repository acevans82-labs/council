# ledger.json schema

One ledger per effort, at `benches/<bench>/efforts/<effort>/ledger.json`. Prior rounds are archived under `rounds/<round_id>/ledger.json`.

```json
{
  "effort": {
    "slug": "acme",
    "name": "Acme Co",
    "bench": "board-director",
    "bench_name": "Board director",
    "noun": "company | idea | deal | decision | initiative | question | other",
    "description": "one line in the principal's words",
    "principal_role": "free text: chair of the board | founder | head of regulatory | parent | ...",
    "round_type": "initial|update",
    "round_id": "r1-20261020",
    "round_number": 1,
    "date": "2026-10-20",
    "trigger": "string: what prompted this round, or 'initial'",
    "depth": "standard|deep (quick convenings are consults and have no ledger)",
    "materials_gate": {"result": "cleared|downgraded|blind", "missing": ["string"]},
    "prior_round": {"round_id": "string|null", "mode": "none|carry_forward|full_rerun"},
    "supplied_documents": [{"name": "string", "type": "deck|report|financials|contract|plan|notes|other", "received": "YYYY-MM-DD"}]
  },
  "chair": {"persona_id": "chair", "competence": "High|Moderate|Low", "rationale": "string"},
  "roster": [
    {"persona_id": "financial", "name": "Financial & Unit Economics", "layer": "analyst|stakeholder|redteam",
     "relevance": "High|Moderate|Low", "competence": "High|Moderate|Low", "rationale": "string",
     "view": "one-paragraph stakeholder view, stakeholders only"}
  ],
  "phases": [
    {"n": 1, "purpose": "Analysts establish the facts", "personas": ["financial"], "abstained": [],
     "summary": "string, reads like minutes", "notable": ["string"]}
  ],
  "evidence": [
    {"id": "E-001", "claim": "string", "source_tier": "T1|T2|T3", "reliability": "A|B|C|D",
     "locator": "document p.12 | URL | register entry and date", "retrieved": "2026-10-20T14:02Z",
     "recorded_by": "financial", "carried_from": null, "reverified": null, "supersedes": null,
     "calc": "optional, required on derived numbers: inputs by E- ID, the formula, the assumptions"}
  ],
  "findings": [
    {"id": "F-001", "persona": "financial", "phase": 1, "statement": "string",
     "confidence": "High|Moderate|Low", "evidence_strength": "Strong|Corroborated|Single-source|Inferred",
     "evidence_ids": ["E-001"], "status": "headline|supporting|open",
     "contested_by": [{"persona": "channel-partner", "note": "string"}], "so_what": "string",
     "driver": "a driver key from the bench's scoring frame",
     "question": "lands|choose_or_leave|hurts (stakeholders only)",
     "extra": {"any persona-specific fields: mirror, return_view, stance, program, direction, mechanism, status, timing, jurisdiction, lens, access_assessment, story, signals"}}
  ],
  "conflicts": [
    {"id": "C-001", "description": "string", "evidence_ids": ["E-003","E-011"],
     "values": [{"source_tier": "T1", "value": "string"}, {"source_tier": "T3", "value": "string"}],
     "confidence_real": "High|Moderate|Low", "likely_cause": "timing|definition|scope|error|misstatement|unknown",
     "public_disclosure_relevant": false, "raised_by": "financial",
     "resolution": "string|null", "resolved_by": "chair|principal|unresolved", "ruling_id": "R-001|null",
     "tier": "0|1|2|3, required while resolved_by is null or 'unresolved'; see skills/council-ledger",
     "tier_rationale": "string|null, one sentence, expected on Tier 0"}
  ],
  "rulings": [
    {"id": "R-001", "phase": 3, "on": "F-004|C-001", "decision": "string", "rationale": "string",
     "dissent": [{"persona": "string", "note": "string"}]}
  ],
  "judgment_calls": [
    {"id": "J-001", "phase": 9, "question": "string", "options": ["string"], "why_principal": "string",
     "type": "judgment|gap_only_principal_can_fill|material_conflict|document_request|headline_waiver",
     "asked_at": "iso", "answer": "string|null", "answered_at": "iso|null", "answered_in_round": "r2-20261104|null", "impact": "string|null",
     "tier": "0|1|2|3, required on every judgment call; see skills/council-ledger",
     "tier_rationale": "string|null, one sentence, expected on Tier 0"}
  ],
  "handoffs": [
    {"id": "H-001", "phase": 1, "from": "financial", "to": "channel-partner", "item": "string", "why": "string", "status": "open|answered"}
  ],
  "gaps": [
    {"id": "G-001", "expected": "string", "why_expected": "string", "searched": ["string"],
     "status": "not_found|found_late|principal_provided|confirmed_nonexistent", "raised_to_principal": true,
     "principal_could_supply": "string|null",
     "tier": "0|1|2|3, required while raised_to_principal is true; see skills/council-ledger",
     "tier_rationale": "string|null, one sentence, expected on Tier 0"}
  ],
  "open_questions": [
    {"id": "Q-001", "type": "gap|disagreement|other_party|judgment|signal", "question": "string",
     "owner": "principal|other_party|council", "linked": ["F-002","C-001"]}
  ],
  "assessment": {
    "label": "the bench's score label, e.g. 'Probability of value creation over 3–5 years'",
    "score": 62, "band": 12, "horizon": "from the bench",
    "drivers": [
      {"name": "Competitive standing", "key": "standing", "weight": 20, "score": 6, "rationale": "string", "finding_ids": ["F-001"]}
    ],
    "verdict": "narrative, 2–4 paragraphs, neutral voice",
    "top_movers": ["string x3"],
    "biggest_stakeholder_risk": "string",
    "what_would_raise": ["string x3"],
    "confidence_rationale": "string from the Evidence Auditor's report and T3/Inferred share",
    "section_summaries": {"<section key from the bench's assessment outline>": "one paragraph"}
  },
  "exec_summary": {"see skills/council-ledger": "schema and caps live there"},
  "score_history": [
    {"round_id": "r1-20261020", "date": "2026-10-20", "score": 62, "band": 12, "note": "initial"}
  ]
}
```

Notes
- All arrays are append-only during a round.
- `phase` on a record is the phase number within the round (1 analysts … 9 synthesis). `round_id` identifies the round of the effort. Never confuse the two: phases are inside a round.
- `so_what` is required on headlines; `driver` is required on every finding so the chair can roll findings into driver scores. Driver keys come from the bench's scoring frame in `bench.md`.
- Stakeholder findings carry `question` so the assessment can group them by the three questions.
- `why_principal` is required on every judgment call. When the principal answers between rounds, `answer`, `answered_at` and `answered_in_round` are filled and the answer is recorded as T1 evidence ("principal, round N answers").
- `effort.noun` is what the bench calls the thing it assesses; outputs use it in prose ("how the idea lands with each stakeholder").
