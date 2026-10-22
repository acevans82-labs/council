---
slug: personal-decision
name: Personal or family decision
principal_role: <fill in: parent, partner, individual, carer, or the role the decision is made in>
organization: personal
field: <fill in: the kind of decision and the setting in one line, e.g. "a family of four weighing a move between two cities for a job", "a parent choosing between two schools"; the country or state whose rules apply>
noun: decision
other_party: none
horizon: default 2 years, set per effort
preset: personal-decision
rebuttal: on
lookback_months: 24
created: 2026-10-20
---
# Bench — Personal or family decision

## The principal's seat
The principal is a person, often a parent or a partner, weighing a significant personal or family decision: a school, a move, a care arrangement for a parent or a child, a career change, a major purchase, a health choice, a parenting choice. In this hat the principal can decide what the household does, within its money, time and the agreement of whoever shares the decision. The principal cannot decide how a child will take it, what an employer or a school will offer, what a professional will advise, or what the rules will allow. The council addresses the principal in the third person as "the principal", never "you", so that the assessment can be shown to a partner or a family member unedited.

## What this bench assesses
A decision with two or more options on the table and a goal the options are meant to serve. Typical efforts are one decision each, with whatever the principal has: a budget, a job offer, school information, a care assessment, notes from conversations, a list of worries. Examples: whether to move the family for a job offer in another city; which of two care arrangements to choose for an ageing parent.

## The question the bench answers
score_label: Likelihood this choice serves the stated goal over the horizon

The goal is named at intake in the principal's own words ("the children settled and the household not stretched", "my mother safe and still herself"). If more than one option is on the table, the chair scores the leading option and says in the verdict how the others compare. If the principal has not stated a goal, the council asks for one before scoring, because a decision cannot be scored against nothing.

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |
| fit_with_goals | Fit with what the household actually wants | 20 | The option serves the goal the principal stated, and the things the household said matter most are met rather than traded away; the people affected agree that this is the goal | The option serves the goal in part, or serves a goal the principal has not quite said out loud; one thing that matters is traded away with eyes open | The option serves someone else's goal (an employer's, a relative's, a school's) or a goal the household has not agreed; what matters most is traded away without saying so |
| evidence_it_works | Whether this kind of choice works for families like this | 20 | Good studies, official data or a professional's assessment of this household say the option tends to produce the outcome the goal names, for people in a similar situation | The evidence is mixed, thin, or from families unlike this one; the professionals consulted are reasonably confident but not certain | The case rests on one story, one website, one relative's experience or a sales pitch; the evidence that exists points the other way |
| cost_affordability | Cost and whether the household can afford it | 15 | The full cost over the horizon (money, and the time that money cannot buy) is known, fits the budget with room to spare, and the household has a cushion if something goes wrong | The cost is roughly known and fits if nothing else changes; the cushion is thin; one line in the budget is a guess | The cost is unknown or clearly more than the household has; it depends on an income, a sale or a benefit that has not arrived; there is no cushion |
| reversibility_risk | How hard it is to undo, and what goes wrong if it does | 15 | The choice can be undone within a year without lasting harm to anyone, or the worst realistic outcome is one the household can live with | Undoing it costs real money or a year of someone's life; the worst case is hard but recoverable | The choice cannot be undone (a sale, a signed contract, a school year lost, a health effect) and the worst case is one the household could not recover from |
| effect_on_people | Effect on the people affected | 15 | Everyone affected has been heard, the person most affected is better off or no worse off, and the people the household depends on (relatives, friends, carers) are still in reach | One person carries most of the cost of the choice and knows it; someone affected has not yet been asked | The person most affected is worse off and has not been heard; the choice cuts the household off from the people it leans on |
| timing | Timing | 15 | Now is a good time: the deadline is real, the household is steady enough to absorb change, and waiting would cost something specific | The deadline is soft or self-imposed; the household is under other strain; waiting costs little | The decision is being forced by a crisis, a sales deadline or someone else's schedule; the household is already stretched; a better moment is in sight and has not been considered |

### Standards
Defaults per skills/scoring. In addition: a score above 70 requires effect_on_people at 6 or higher, and the council never scores above 50 while the person most affected has not been heard where they are old enough to be asked.

## Assessment outline
Subject sections, in order: the options on the table; what the evidence says; cost and reversibility; the people affected.

Stakeholder order: end-user (the person most affected), co-decider, domain-expert, values-ethics, community-public, employee.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
| research-evidence | analyst | high | What studies, official data and professional guidance say about choices like this for households like this |
| options-tradeoffs | analyst | high | The options actually on the table, including waiting and the hybrid nobody has named, and the cheapest way to tell them apart |
| financial | analyst | high | Household finances: the full cost of each option over the horizon, what it does to the budget, and the cushion |
| operating-model | analyst | high | Day-to-day logistics: the school run, the commute, the care rota, who does what on a Tuesday in the new arrangement |
| regulatory-policy | analyst | low | Eligibility rules, entitlements, deadlines and legal constraints: catchment, residency, benefits, visas, consent, custody |
| end-user | stakeholder | high | The person most affected: the child, the parent being cared for, the partner who moves; the voice the decision is about |
| co-decider | stakeholder | high | Partner / co-decider: the person who has to agree, with their own goal and their own fears |
| domain-expert | stakeholder | high | Professional in the field: the pediatrician, teacher, care assessor, financial planner or clinician whose assessment of this household matters |
| values-ethics | stakeholder | high | Family values and what the principal would be proud of having chosen, looking back |
| community-public | stakeholder | moderate | Family and community: extended family, friends, neighbours, the school community, the people who show up when something goes wrong |
| employee | stakeholder | low | The principal as an employee, only when the decision changes the principal's work |
| adversary | redteam | high | The skeptic: the strongest case for the other choice, or for waiting |
| pre-mortem | redteam | high | Two years on and the choice did not serve the goal; the stories and the early signs |
| evidence-auditor | redteam | high | Grades the evidence, including the stories, the websites and the "everyone says" claims |
(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Materials ladder
quick: nothing beyond the context folder
standard: the options written down and the household budget
deep: the options with their real costs, the offers or documents behind each, any professional assessment, and what the people affected have said

## Depth profiles
(defaults per skills/convening)

## Primary sources in this field
T1 is what the principal supplies: the household budget, the offer letter, the school or care information pack, the professional's written assessment, notes from conversations with the people affected. T2 in this field: official statistics and inspection reports (schools, care providers, neighbourhoods, employers); government and public-health guidance; peer-reviewed research on the kind of choice in question; statutes, eligibility rules and official calculators for entitlements; court or tribunal records where relevant. T3: review sites, parent and carer forums, press, estate-agent and provider marketing, a relative's experience. The seat briefs name where each seat starts; the principal should replace the fill-in prompts with the actual school, provider, employer, city or condition.

## The other party
None. The decision is the household's. If the principal wants a note for a partner, a parent or a professional, the chair writes a note for a named reader per skills/assessment-output, containing only what that reader should see.

## Confidentiality
Personal and children's information never leaves the effort folder. Names, ages, health details, finances and anything about a child are not quoted into any other effort, on this bench or any other, and are not used to search the web in a way that would identify the household. The principal may keep documents uncommitted: the `.gitignore` in this repository has a commented line for `benches/*/efforts/*/documents/`; uncomment it and supplied documents stay on this machine. The council is not a clinician, a lawyer or a financial adviser. Its outputs say so, and where a decision turns on a medical, legal or financial judgment the council names the professional the principal should consult and what to ask them, rather than supplying the judgment itself.
