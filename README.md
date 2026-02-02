# WTL Partnership Knowledge Graph

> **Purpose:** Central repository for all partnership intelligence  
> **Owner:** Reed (Partnerships)  
> **Sync:** Auto-updates from Nomo meeting data  
> **Updated:** 2026-02-02

---

## Repository Structure

```
wtl-partnerships/
├── README.md                    # This file
├── STRUCTURE.md                 # Documentation on organization
├── sync/                        # Meeting data sync scripts
│   ├── nomo-sync.sh            # Pull from Nomo MCP
│   ├── last-sync.json          # Timestamp tracking
│   └── pipeline-update.py      # Update pipeline from meetings
├── entities/                    # Knowledge graph entities
│   ├── people/                 # Partner contacts, decision makers
│   ├── companies/              # Partner organizations
│   ├── deals/                  # Active deals & opportunities
│   └── relationships/          # Connection mapping
├── pipeline/                    # Partnership pipeline
│   ├── active/                 # Active deals (by stage)
│   ├── closed/                 # Closed deals (won/lost)
│   └── pipeline.json           # Master tracker
├── meetings/                    # Meeting notes & transcripts
│   ├── YYYY-MM/               # Organized by month
│   └── index.md               # Meeting index
├── templates/                   # Partnership templates
│   ├── NDA.md
│   ├── PKS.md
│   ├── pricing-sheet.md
│   └── partner-enablement.md
├── pricing/                     # Pricing documentation
│   ├── aivident.md
│   ├── elwyn.md
│   ├── nora.md
│   └── nomo.md
└── analytics/                   # Partnership metrics
    ├── monthly-report.md
    ├── revenue-by-partner.md
    └── conversion-funnel.md
```

---

## Quick Navigation

| Need to find... | Go to... |
|-----------------|----------|
| Partner contact info | `entities/people/` |
| Deal status | `pipeline/active/` |
| Meeting notes | `meetings/YYYY-MM/` |
| Pricing | `pricing/[product].md` |
| Templates | `templates/` |
| Pipeline overview | `pipeline/pipeline.json` |

---

## Active Pipeline Summary

| Partner | Product | Stage | Value | Next Action | Last Update |
|---------|---------|-------|-------|-------------|-------------|
| TrueVA | Elwyn | Proposal | TBD | Pricing doc for DBS | 2026-02-02 |
| CIMB | Elwyn/1RM | Closed-Won | Rp X | VR/AI approved | 2026-02-02 |
| Humani Santika | All | Onboarding | TBD | NDA/PKS | 2026-02-02 |
| Dearezt | Aivident | Active | Ongoing | ASTRA deal | 2026-01-30 |
| DayaLima | Aivident | Active | Rp X | BPJS case study | 2026-01-30 |
| Talenta | Aivident | Negotiation | TBD | PKS discussion Feb 4 | 2026-01-28 |

---

## Auto-Sync Status

- **Nomo MCP:** Connected ✅
- **Last sync:** 2026-02-02 15:30 UTC
- **Meetings indexed:** 20
- **Entities extracted:** 12

---

## How to Use

### For Reed (Partnership Agent)
```bash
# Daily workflow
cd ~/repos/wtl-partnerships
./sync/nomo-sync.sh          # Pull latest meetings
./sync/pipeline-update.py    # Update pipeline

# Update deal status
vim pipeline/active/trueva-dbs.md
git add . && git commit -m "Update TrueVA status" && git push
```

### For Aldo
- Browse deals: `pipeline/active/`
- Check pricing: `pricing/[product].md`
- Meeting history: `meetings/YYYY-MM/`

---

*Maintained by Reed 🌿 | Auto-sync enabled | Last manual update: 2026-02-02*