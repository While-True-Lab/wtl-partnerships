# Partnership Knowledge Graph Structure

## Philosophy

This repo treats partnerships as a **knowledge graph** — entities (people, companies, deals) connected by relationships, enriched with temporal data (meetings), and tracked through state changes (pipeline stages).

---

## Entity Types

### 1. People (`entities/people/`)

Each person gets a markdown file:

```markdown
---
id: uuid
name: Full Name
company: company-key
role: Job Title
email: email@example.com
phone: +62xxx
decision_maker: true/false
influencer: true/false
first_met: YYYY-MM-DD
last_contact: YYYY-MM-DD
tags: [tag1, tag2]
---

# Person Name

## Background
Brief bio, how they fit into organization

## Relationship History
- YYYY-MM-DD: First meeting, context
- YYYY-MM-DD: Follow-up, outcome

## Notes
- Personal details (family, interests)
- Communication preferences
- Decision-making style

## Linked Deals
- [[deal-key]]
```

### 2. Companies (`entities/companies/`)

```markdown
---
id: uuid
name: Company Name
type: [client|partner|prospect|competitor]
industry: Industry
size: employees
revenue: annual revenue
location: City, Country
website: https://...
status: [active|inactive|closed]
---

# Company Name

## Overview
Brief company description

## Key Contacts
- [[person-key-1]] - Role
- [[person-key-2]] - Role

## Relationship
- Partner since: YYYY-MM-DD
- Partnership type: [VAD|Channel|Strategic|Technology]
- Revenue share: X%

## Active Deals
- [[deal-key-1]]

## Meeting History
- [[meeting-2026-02-02-cimb]]

## Notes
- Strategic importance
- Competitive landscape
- Opportunities/Risks
```

### 3. Deals (`entities/deals/`)

```markdown
---
id: uuid
name: Deal Name
company: company-key
product: [Aivident|Elwyn|Nora|Nomo]
stage: [prospecting|qualification|proposal|negotiation|closed-won|closed-lost]
value: IDR/USD amount
probability: 0-100%
expected_close: YYYY-MM-DD
actual_close: YYYY-MM-DD
source: [partner-sourced|wtl-sourced|inbound]
assigned_to: Reed
---

# Deal Name

## Overview
What, why, how much

## Stakeholders
- Decision maker: [[person-key]]
- Champion: [[person-key]]
- Influencers: [[person-key]]

## Timeline
- YYYY-MM-DD: Initial contact
- YYYY-MM-DD: Discovery meeting
- YYYY-MM-DD: Proposal sent
- YYYY-MM-DD: (expected) Close

## Meeting Notes
- [[meeting-2026-01-15]]
- [[meeting-2026-01-22]]

## Action Items
- [ ] Item 1
- [ ] Item 2

## Next Steps
What's needed to move forward

## Blockers
What's preventing progress
```

---

## Sync Architecture

### From Nomo MCP
```
Nomo Meetings
     ↓
meeting-extractor.py
     ↓
├── meetings/YYYY-MM-DD-slug.md
├── entities/people/ (auto-create if new)
├── entities/companies/ (auto-create if new)
└── pipeline/ (update deal stage if mentioned)
```

### Pipeline State Machine
```
prospecting → qualification → proposal → negotiation → closed-won
                                   ↓
                              closed-lost (with reason)
```

---

## Data Flow

1. **Meeting happens** → Recorded in Nomo
2. **Sync runs** → Pull transcript, action items, decisions
3. **Extract entities** → Identify people, companies mentioned
4. **Update deals** → Check for pipeline stage changes
5. **Commit & push** → History preserved in git

---

## Naming Conventions

- **Files:** lowercase-with-hyphens.md
- **IDs:** UUID v4 (auto-generated)
- **Dates:** YYYY-MM-DD
- **Currencies:** IDR, USD, SGD (always specify)

---

## Git Workflow

```bash
# Daily sync creates commits automatically
git add meetings/ entities/ pipeline/
git commit -m "Sync: 2026-02-02 - 3 meetings, 2 new contacts"

# Manual updates
git add pipeline/active/deal-name.md
git commit -m "Update TrueVA: pricing approved"
```

---

## Query Patterns

### Find all deals in proposal stage
```bash
grep -l "stage: proposal" pipeline/active/*.md
```

### Find meetings with specific person
```bash
grep -r "person-key" meetings/2026-*
```

### Find deals closing this month
```bash
grep "expected_close: 2026-02" pipeline/active/*.md
```

---

*Documentation v1.0 | Reed 🌿*