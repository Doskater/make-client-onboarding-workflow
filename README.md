# Make.com Client Onboarding Workflow

Portfolio proof for a simple Make.com workflow that connects form input, Google Sheets, Google Drive, Gmail, and client status tracking.

The goal is intentionally small: a clean V1 workflow for a media or marketing company that needs to onboard new clients without losing track of payment status, delivery status, client folders, or internal notifications.

## Business Problem

Small teams often start with form submissions, manual Google Sheets updates, hand-created Drive folders, and ad hoc Gmail alerts. That works for the first few clients, but it quickly creates missed follow-ups, inconsistent folder names, and unclear delivery status.

## Solution

The Make.com workflow structure is:

```text
Client form or webhook submission
-> Google Sheets row
-> Google Drive client folder
-> Gmail internal alert
-> Google Sheets status update
```

This repository includes:

- a Make.com scenario structure and setup guide
- a Google Sheets schema for status tracking
- clean live screenshots from the Make scenario builder and Google Sheet tracker
- a redacted blueprint-style scenario snapshot with private connection details removed
- safe demo form submissions
- an offline Python demo that simulates the same workflow outputs
- sample output files for review
- a proposal draft tailored to the Upwork job

## V1 Workflow Fields

The tracking sheet keeps the workflow editable and easy to understand:

- Client Name
- Email
- Company
- Service
- Submission Date
- Payment Status
- Delivery Status
- Drive Folder URL
- Notification Sent
- Last Updated
- Error Notes

Default statuses are `Pending` for payment and `Not Started` for delivery.

## Make.com Scenario

The recommended scenario is documented in [docs/scenario-structure.md](docs/scenario-structure.md).

The workflow uses only these tools:

- Webhooks or a connected form trigger
- Google Sheets
- Google Drive
- Gmail

No database, CRM, or extra SaaS tool is required for the V1.

## Live Build Evidence

I also assembled the V1 chain in a live Make.com scenario:

- [Make scenario canvas screenshot](screenshots/make-scenario-clean.png)
- [Make visible execution screenshot](screenshots/make-execution-success.png)
- [Google Sheets tracker screenshot](screenshots/google-sheet-tracker-clean.png)
- [Live build notes](docs/live-build-notes.md)
- [Redacted scenario snapshot](make/live_scenario_redacted.json)

The redacted snapshot is safe for portfolio review. It intentionally removes real webhook URLs, account emails, connection IDs, and OAuth details.

## Local Demo

The local demo does not connect to Google or Make.com. It creates deterministic sample artifacts that show what the workflow would produce after a successful run.

Run from this project folder:

```bash
python3 scripts/run_demo.py
```

Generated files:

- `sample_output/google_sheet_rows.csv`
- `sample_output/drive_folder_manifest.csv`
- `sample_output/gmail_notifications.md`
- `sample_output/error_log.csv`
- `sample_output/run_report.md`

## Tests

```bash
python3 -m unittest discover -s tests
```

## Client Handoff

For a real client, the handoff is simple:

1. Create or copy the Google Sheet from `sample_data/google_sheet_schema.csv`.
2. Create one parent Drive folder for all client folders.
3. Build or import the Make scenario using [docs/setup-guide.md](docs/setup-guide.md).
4. Send one demo submission.
5. Confirm the Sheet row, Drive folder, Gmail alert, and status update.

## Why This Is Kept Simple

This workflow is designed for a first operational version. It avoids complex branching, unnecessary tools, and custom code in Make. The structure can later scale into payment reminders, delivery checklists, CRM sync, or dashboards after the basic client onboarding process is proven.
