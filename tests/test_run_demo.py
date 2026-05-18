import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_demo import run_demo


class RunDemoTests(unittest.TestCase):
    def test_generates_success_and_error_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "submissions.json"
            output_dir = root / "output"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "client_name": "Demo Client",
                            "email": "demo@example.com",
                            "company": "Demo Company",
                            "service_requested": "Campaign setup",
                            "submitted_at": "2026-05-18T09:00:00+01:00",
                            "budget": "1000 GBP",
                            "notes": "Ready for onboarding.",
                        },
                        {
                            "client_name": "Broken Client",
                            "email": "broken@example.com",
                            "company": "",
                            "service_requested": "Campaign setup",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            result = run_demo(input_path, output_dir)

            self.assertEqual(result, {"processed": 1, "errors": 1})
            self.assertTrue((output_dir / "google_sheet_rows.csv").exists())
            self.assertTrue((output_dir / "drive_folder_manifest.csv").exists())
            self.assertTrue((output_dir / "gmail_notifications.md").exists())
            self.assertTrue((output_dir / "error_log.csv").exists())

            with (output_dir / "google_sheet_rows.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["Payment Status"], "Pending")
            self.assertEqual(rows[0]["Delivery Status"], "Not Started")
            self.assertEqual(rows[0]["Notification Sent"], "Yes")
            self.assertIn("drive.google.com", rows[0]["Drive Folder URL"])

            with (output_dir / "error_log.csv").open(encoding="utf-8") as handle:
                errors = list(csv.DictReader(handle))
            self.assertIn("company", errors[0]["Error Notes"])


if __name__ == "__main__":
    unittest.main()

