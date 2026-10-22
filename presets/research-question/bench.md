---
slug: research-question
name: Open question, evidence weighed
principal_role: <fill in: researcher, student, professional, or curious person>
organization: <fill in, or personal>
field: <fill in: the discipline or subject area the questions tend to come from, in one line; "any" is acceptable>
noun: question
other_party: none
horizon: not applicable
preset: research-question
rebuttal: on
lookback_months: 120
created: 2026-10-20
---
# Bench — Open question, evidence weighed

## The principal's seat
The principal is anyone with an open question in any field who wants the evidence weighed rather than a single confident answer: a researcher checking a claim outside their specialty, a student framing a thesis, a professional deciding what the literature actually supports, a curious person who has read two contradictory articles. In this hat the principal decides what to believe and what to do with the answer; the principal cannot decide what the evidence says, and the council does not pretend to settle what the field has not. The council addresses the principal in the third person as "the principal", never "you". The horizon is not applicable: the question is answered as of the round date, and the assessment names what would change the answer.

## What this bench assesses
A question: empirical ("does X cause Y"), practical ("does X work for people like Z"), interpretive ("what is the best explanation for X"), or forecasting ("is X likely by date Y"). Examples: whether a widely reported dietary intervention has evidence behind it for adults over fifty; whether a historical claim repeated in popular books holds up against the primary sources.

## The question the bench answers
score_label: Confidence that the evidence supports the council's answer

The council first states the question as posed, then as refined (narrower, with the population, the outcome and the comparison named), then answers it in one sentence, and scores its confidence in that answer. A low score with a clear answer is a legitimate result; so is "the evidence does not decide this", scored accordingly.

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |
| evidence_quality | Quality of the evidence on the answer | 25 | Multiple well-designed, replicated, independent studies or primary datasets, pre-registered where the field does that, with methods that fit the question | A few decent studies or one strong one, not yet replicated; or good observational data without a controlled comparison; or primary sources with known gaps | Anecdote, a single unreplicated source, a press release, a secondary account of a secondary account, or marketing |
| consensus | Agreement in the field | 20 | Expert bodies, reviews and the leading researchers on both sides of past disputes agree, and the disagreement that remains is at the margins | A working majority leans one way with a credible minority dissenting on substance; or the field has not formally reviewed the question | The field is split down the middle, or the apparent consensus is one group citing itself, or the question has never been studied by the people best placed to study it |
| mechanism | A plausible mechanism | 20 | The answer has a mechanism that fits established knowledge, has been observed directly, and predicts things that were then found | A mechanism is proposed and plausible but not directly observed; or several mechanisms compete and the evidence does not pick one | No mechanism, or one that contradicts well-established knowledge, or the effect is the kind that disappears when measured more carefully |
| applicability | Applicability to the principal's situation | 20 | The evidence comes from people, settings, periods or conditions like the principal's, or the effect is shown to transfer | The evidence is from a related population or setting and transfer is plausible but untested | The evidence is from a population, setting or period unlike the principal's, and the answer could reverse with that difference |
| counter_evidence | How the counter-evidence has been handled | 15 | The strongest evidence against the answer has been found, weighed and explained; negative results and failed replications are in the record | Some counter-evidence is acknowledged; the record of negative results has not been searched; the strongest opposing study is cited but not engaged | Counter-evidence is absent from the record, or dismissed on the source's reputation rather than its method; publication bias is likely and unexamined |

### Standards
Defaults per skills/scoring. In addition: a score above 75 requires evidence_quality at 7 or higher and counter_evidence at 6 or higher; the council does not express high confidence in an answer whose opposition it has not read.

## Assessment outline
Subject sections, in order: the question as posed and as refined; what the evidence says; where the field disagrees; what applies to the principal's situation; what would change the answer.

Stakeholder order: domain-expert-a, domain-expert-b, end-user, values-ethics, community-public.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
| research-evidence | analyst | high | Finds and grades the primary evidence: studies, datasets, primary sources, reviews, and the negative results |
| options-tradeoffs | analyst | high | Framing and alternatives: refines the question, names the rival hypotheses, says what would discriminate between them |
| technical-feasibility | analyst | moderate | Mechanism and plausibility: whether the proposed explanation could work, given what is established |
| valuation-precedent | analyst | moderate | Precedent and analogues: how similar questions were settled, and which confident answers later reversed |
| financial | analyst | low | Who funds the research and who profits from each answer; the money behind the evidence |
| regulatory-policy | analyst | low | What official bodies, guidelines and standards currently say, and whether that is evidence or inertia |
| domain-expert-a | stakeholder | high | Expert, position A: the strongest school of thought on one side, assigned by the chair per effort |
| domain-expert-b | stakeholder | high | Expert, position B: the strongest opposing school of thought, assigned by the chair per effort |
| end-user | stakeholder | high | The person who has to act on the answer: what they can do with it and what precision they need |
| values-ethics | stakeholder | moderate | The values embedded in the question and the answer, and who is harmed by getting it wrong either way |
| community-public | stakeholder | low | How the question plays in public discourse: the popular version, the misinformation, the motivated readings |
| adversary | redteam | high | The strongest counter-case to the council's emerging answer |
| pre-mortem | redteam | high | The answer turned out wrong: two years on, how, and what should have been noticed |
| evidence-auditor | redteam | high | Grades every citation at source; on this bench the audit is most of the work |
(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Materials ladder
quick: nothing beyond the context folder
standard: the question written precisely and the sources the principal already trusts or distrusts
deep: the question, the principal's own data or prior work, and the specific studies or sources the answer must engage

## Depth profiles
(defaults per skills/convening)

## Primary sources in this field
T1 is what the principal supplies: their own data, notes, drafts, the articles that prompted the question. T2 on this bench: peer-reviewed journals and their published corrections and retractions; pre-registrations and trial registries; primary datasets and official statistics; archives and primary documents for historical questions; systematic reviews from recognised bodies; standards and guidelines from professional and official bodies, graded as evidence only where they cite theirs. T3: textbooks and popular books, press, encyclopedias, preprints not yet reviewed (graded by their method, not their venue), blogs, talks, and the principal's own field's folklore. The lookback is set to 120 months rather than the default 24 because the evidence on a question accumulates over decades and the decisive study is often old; personas still read the most recent reviews first and say where the record has moved inside the last two years.

## The other party
None. If the principal wants a note for a colleague, a supervisor or a reader, the chair writes a note for a named reader per skills/assessment-output.

## Confidentiality
The principal's own data, unpublished drafts and notes stay in the effort folder and are never quoted into another effort. Where the question is about the principal's own health, finances or legal position, the council treats it as it would on the personal-decision bench: it is not a clinician, lawyer or financial adviser, says so in outputs, and names the professional to consult. Keep documents uncommitted by uncommenting the `documents/` line in `.gitignore` if the repository is shared.
