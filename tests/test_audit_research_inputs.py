import tempfile
import unittest
from pathlib import Path
from tools.audit_research_inputs import audit_comparison, audit_sources

class ResearchAuditTests(unittest.TestCase):
    def write(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False)
        tmp.write(content)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_valid_source_log(self):
        path = self.write("source_id,title,url,accessed_date,claim_or_section_supported,status\nS01,Official page,https://example.com,2026-10-29,Plan limits,Checked\n")
        errors, _ = audit_sources(path)
        self.assertEqual(errors, [])

    def test_rejects_invalid_source_url(self):
        path = self.write("source_id,title,url,accessed_date,claim_or_section_supported,status\nS01,Page,not-a-url,2026-10-29,Claim,Checked\n")
        errors, _ = audit_sources(path)
        self.assertTrue(any("absolute http(s)" in e for e in errors))

    def test_weight_warning_for_incomplete_weights(self):
        path = self.write("option_name,criterion,weight_percent,score_1_to_5,evidence_summary,source_ids\nTool A,Cost,20,,,,\n")
        _, warnings = audit_comparison(path)
        self.assertTrue(any("not 100%" in w for w in warnings))

    def test_rejects_score_outside_range(self):
        path = self.write("option_name,criterion,weight_percent,score_1_to_5,evidence_summary,source_ids\nTool A,Cost,100,8,Evidence,S01\n")
        errors, _ = audit_comparison(path)
        self.assertTrue(any("between 1 and 5" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
