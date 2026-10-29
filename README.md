# Research & Reporting Toolkit

A practical toolkit for source-based research, competitor comparisons, and concise business summaries.

> **Status:** Usable service MVP with reusable templates, a source-backed research sample, and a Python utility for auditing research inputs.

## Start here

1. Copy the [research brief template](templates/research-brief-template.md).
2. Track claims in the [source log CSV](templates/source-log-template.csv).
3. Compare options with the [competitor comparison CSV](templates/competitor-comparison-template.csv).
4. Prepare a decision-maker version with the [executive summary template](templates/executive-summary-template.md).
5. Review the [quality checklist](checklists/quality-review.md).

## Portfolio examples

- [CRM evaluation framework](examples/research-brief/sample-crm-evaluation-brief.md) — reusable decision criteria, without claiming a vendor ranking.
- [Free CRM options for a small team](examples/research-brief/free-crm-options-small-team.md) — limited comparison based on official vendor pages, with a [matching source log](examples/research-brief/free-crm-source-log.csv).

## Functional utility

The [research input audit tool](tools/README.md) checks source-log columns, duplicate IDs, URL structure, comparison scores, and criterion-weight totals. It uses only Python's standard library. It does not browse sources or verify claims automatically.

Run from the repository root:

```bash
python tools/audit_research_inputs.py --sources examples/research-brief/free-crm-source-log.csv
python -m unittest discover -s tests -v
```

## Services this toolkit supports

- Focused research briefs with traceable claims
- Document and report summaries
- Competitor or service comparisons
- Source logs and evidence tracking
- Executive summaries and action lists
- Quality review before delivery

See [starter service packages](SERVICE_PACKAGES.md) for proposed scope and intake requirements.

## Working principles

- Cite material factual claims and keep a source log.
- Prefer primary and authoritative sources where practical.
- Separate verified facts, assumptions, interpretation, and recommendations.
- Mark unknown information instead of guessing.
- Label portfolio demonstrations honestly and protect confidential information.
- Treat AI-generated summaries as drafts that require checking.

## Current limitations

The CRM comparison uses official vendor pages only, not independent tests or hands-on product trials. Product limits and prices can change, so reconfirm details before decisions. The comparison CSV is a starter template; complete and verify scores before using them for a decision. The audit tool checks input structure, not factual truth or source reliability.

## Quality checks

Automated tests run through GitHub Actions on pushes and pull requests. See the [test workflow](.github/workflows/test.yml).
