# Setup Guide

## 1. Create the Google Sheet

Create a Sheet named:

```text
Client Onboarding Tracker
```

Use the columns from:

```text
sample_data/google_sheet_schema.csv
```

The first tab can be named `Clients`.

## 2. Create the Parent Drive Folder

Create a Google Drive folder named:

```text
Client Onboarding
```

Every client folder should be created inside this parent folder.

## 3. Create the Make.com Scenario

Create a new scenario in Make.com and add modules in this order:

```text
Webhooks -> Google Sheets -> Google Drive -> Gmail -> Google Sheets
```

Configure the modules using:

```text
docs/scenario-structure.md
```

## 4. Connect Accounts

Connect only the accounts needed for V1:

- Google Sheets
- Google Drive
- Gmail

Use the client's own Google account or a workspace-owned automation account. Do not use a freelancer-owned Google account for production.

## 5. Test With Demo Payload

Send the payload from:

```text
sample_data/demo_submission.json
```

Expected result:

- one new row appears in Google Sheets
- one client folder appears in Google Drive
- one Gmail alert is sent
- the Sheet row is updated with `Notification Sent = Yes`
- the Sheet row has a Drive folder link

## 6. Production Checklist

Before activating the scenario:

- Confirm the internal notification recipient.
- Confirm the parent Drive folder location.
- Confirm the exact Sheet tab and column names.
- Confirm that `Payment Status` and `Delivery Status` values match the team's language.
- Run one successful test.
- Run one missing-field test and confirm `Error Notes` is visible.

## 7. Handoff Notes

The workflow owner should know how to:

- edit Sheet status fields manually
- find the generated Drive folder
- change the Gmail recipient
- inspect Make execution history
- turn the scenario on or off

Keep the V1 scenario readable. If a future requirement needs more than one or two extra branches, document it before adding it.

