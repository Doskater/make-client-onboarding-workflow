# Live Make.com Build Notes

## Scenario Built

Scenario name:

```text
Client Onboarding Tracker - Sheets Drive Gmail
```

Live module chain:

```text
Custom webhook
-> Google Sheets: Add a Row
-> Google Drive: Create a folder
-> Gmail: Send an email
-> Google Sheets: Update a Row
```

The live scenario was configured with the same V1 structure described in this repository. Google Drive was configured to create folders in My Drive root for the demo account. For a client handoff, the folder step should be switched to a dedicated parent folder named `Client Onboarding`.

## Live Evidence Captured

- `screenshots/make-scenario-clean.png` shows the configured Make scenario canvas.
- `screenshots/make-execution-success.png` shows the editor after a queued webhook record was processed, with a success count on each module position.
- `screenshots/google-sheet-tracker-clean.png` shows the Google Sheets tracking structure with demo rows.
- `make/live_scenario_redacted.json` provides a safe blueprint-style snapshot for review.

## Privacy Handling

The public artifacts do not include:

- real webhook URL
- real Gmail address
- Make connection IDs
- OAuth callback codes
- Google account profile details

## Visible Execution Notes

The scenario was put into `Run once` listening mode and external JSON webhook requests were accepted by Make. Make then showed two queued webhook records. I selected `Use existing data` in the editor, and the visible run state showed a success count of `1` on each module position in the five-step chain.

The execution screenshot should be read together with the scenario canvas screenshot: the canvas screenshot shows the module names and order, and the execution screenshot shows the successful run counters on those same five positions.

For a production client test, run the scenario in Make, send one sample form submission, then confirm:

- one new Sheet row
- one new Drive folder
- one Gmail notification
- the same Sheet row updated with folder URL and notification status
