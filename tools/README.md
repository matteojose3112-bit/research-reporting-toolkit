# Research input audit utility

`audit_research_inputs.py` checks source-log CSVs for required columns, duplicate IDs, and absolute HTTP(S) URLs. It checks comparison CSVs for missing fields, invalid 1–5 scores, duplicate option/criterion pairs, evidence gaps on scored rows, and whether criterion weights total 100% per option.

It uses only the Python standard library. The tool does not visit URLs or verify that sources support the claims; a human still needs to review evidence and recency.

From the repository root:

```bash
python tools/audit_research_inputs.py --sources examples/research-brief/free-crm-source-log.csv
python tools/audit_research_inputs.py --comparison templates/competitor-comparison-template.csv
python -m unittest discover -s tests -v
```

The starter comparison template intentionally has blank scores and weights; warnings are expected until the sheet is completed for a real assignment.
