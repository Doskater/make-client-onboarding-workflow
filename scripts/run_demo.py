#!/usr/bin/env python3
"""Generate offline sample outputs for the Make.com client onboarding workflow."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "sample_data" / "demo_submissions.json"
DEFAULT_OUTPUT = ROOT / "sample_output"

SHEET_COLUMNS = [
    "Client Name",
    "Email",
    "Company",
    "Service",
    "Submission Date",
    "Payment Status",
    "Delivery Status",
    "Drive Folder URL",
    "Notification Sent",
    "Last Updated",
    "Error Notes",
]

REQUIRED_FIELDS = ["client_name", "email", "company", "service_requested"]


@dataclass(frozen=True)
class ProcessedSubmission:
    sheet_row: dict[str, str]
    folder_row: dict[str, str]
    notification_markdown: str


def load_submissions(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Input JSON must be an object or a list of objects.")


def missing_required_fields(submission: dict[str, Any]) -> list[str]:
    return [field for field in REQUIRED_FIELDS if not str(submission.get(field, "")).strip()]


def folder_safe(value: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]+", "-", value.strip())
    clean = re.sub(r"-+", "-", clean).strip("-")
    return clean or "unknown-company"


def date_from_submission(submission: dict[str, Any]) -> str:
    submitted_at = str(submission.get("submitted_at", "")).strip()
    if not submitted_at:
        return datetime.now(timezone.utc).date().isoformat()
    return submitted_at[:10]


def fake_drive_url(company: str, submitted_date: str) -> str:
    folder_slug = folder_safe(f"{company}-{submitted_date}")
    return f"https://drive.google.com/drive/folders/demo-{folder_slug}"


def build_notification(submission: dict[str, Any], folder_url: str) -> str:
    company = str(submission["company"]).strip()
    client_name = str(submission["client_name"]).strip()
    return "\n".join(
        [
            f"## New client onboarding: {company}",
            "",
            f"- Client: {client_name}",
            f"- Email: {submission['email']}",
            f"- Company: {company}",
            f"- Service: {submission['service_requested']}",
            f"- Budget: {submission.get('budget', 'Not provided')}",
            f"- Drive folder: {folder_url}",
            "",
            "Notes:",
            str(submission.get("notes", "No notes provided.")).strip() or "No notes provided.",
            "",
        ]
    )


def process_submission(submission: dict[str, Any], now: str) -> ProcessedSubmission:
    submitted_date = date_from_submission(submission)
    company = str(submission["company"]).strip()
    folder_name = f"Client - {company} - {submitted_date}"
    folder_url = fake_drive_url(company, submitted_date)

    sheet_row = {
        "Client Name": str(submission["client_name"]).strip(),
        "Email": str(submission["email"]).strip(),
        "Company": company,
        "Service": str(submission["service_requested"]).strip(),
        "Submission Date": str(submission.get("submitted_at", submitted_date)).strip(),
        "Payment Status": "Pending",
        "Delivery Status": "Not Started",
        "Drive Folder URL": folder_url,
        "Notification Sent": "Yes",
        "Last Updated": now,
        "Error Notes": "",
    }

    folder_row = {
        "Company": company,
        "Folder Name": folder_name,
        "Folder URL": folder_url,
        "Parent Folder": "Client Onboarding",
    }

    return ProcessedSubmission(
        sheet_row=sheet_row,
        folder_row=folder_row,
        notification_markdown=build_notification(submission, folder_url),
    )


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_demo(input_path: Path, output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        display_input_path = input_path.resolve().relative_to(ROOT)
    except ValueError:
        display_input_path = input_path

    submissions = load_submissions(input_path)
    processed: list[ProcessedSubmission] = []
    errors: list[dict[str, str]] = []

    for index, submission in enumerate(submissions, start=1):
        missing = missing_required_fields(submission)
        if missing:
            errors.append(
                {
                    "Submission Index": str(index),
                    "Client Name": str(submission.get("client_name", "")).strip(),
                    "Email": str(submission.get("email", "")).strip(),
                    "Error Notes": f"Missing required field(s): {', '.join(missing)}",
                    "Last Updated": now,
                }
            )
            continue
        processed.append(process_submission(submission, now))

    write_csv(
        output_dir / "google_sheet_rows.csv",
        [item.sheet_row for item in processed],
        SHEET_COLUMNS,
    )
    write_csv(
        output_dir / "drive_folder_manifest.csv",
        [item.folder_row for item in processed],
        ["Company", "Folder Name", "Folder URL", "Parent Folder"],
    )
    write_csv(
        output_dir / "error_log.csv",
        errors,
        ["Submission Index", "Client Name", "Email", "Error Notes", "Last Updated"],
    )

    notifications = ["# Gmail Notification Drafts", ""]
    for item in processed:
        notifications.append(item.notification_markdown)
    (output_dir / "gmail_notifications.md").write_text("\n".join(notifications), encoding="utf-8")

    report = "\n".join(
        [
            "# Client Onboarding Workflow Demo Report",
            "",
            f"Input file: `{display_input_path}`",
            f"Processed submissions: {len(processed)}",
            f"Errored submissions: {len(errors)}",
            "",
            "Generated artifacts:",
            "",
            "- `google_sheet_rows.csv`",
            "- `drive_folder_manifest.csv`",
            "- `gmail_notifications.md`",
            "- `error_log.csv`",
            "",
        ]
    )
    (output_dir / "run_report.md").write_text(report, encoding="utf-8")

    return {"processed": len(processed), "errors": len(errors)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline Make.com workflow demo.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = run_demo(args.input, args.output_dir)
    print(f"Processed {result['processed']} submissions.")
    print(f"Logged {result['errors']} errors.")
    print(f"Output written to {args.output_dir}")


if __name__ == "__main__":
    main()
