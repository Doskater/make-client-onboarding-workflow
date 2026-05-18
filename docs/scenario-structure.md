# Make.com Scenario Structure

## Scenario Goal

Capture a new client submission, add it to a Google Sheet, create a client folder in Google Drive, send an internal Gmail alert, and update the tracking row with the folder link and notification status.

## Module Order

```text
1. Webhooks - Custom webhook
2. Google Sheets - Add a row
3. Google Drive - Create a folder
4. Gmail - Send an email
5. Google Sheets - Update a row
```

## Module Details

### 1. Webhooks - Custom Webhook

Name: `Client onboarding form received`

Expected fields:

- `client_name`
- `email`
- `company`
- `service_requested`
- `submitted_at`
- `budget`
- `notes`

The webhook can be replaced later with Typeform, Tally, Jotform, Webflow Forms, or Google Forms. For V1, the custom webhook is the most flexible trigger.

### 2. Google Sheets - Add a Row

Sheet: `Client Onboarding Tracker`

Map the incoming submission into a new tracking row:

| Sheet column | Value |
| --- | --- |
| Client Name | `client_name` |
| Email | `email` |
| Company | `company` |
| Service | `service_requested` |
| Submission Date | `submitted_at` |
| Payment Status | `Pending` |
| Delivery Status | `Not Started` |
| Drive Folder URL | blank until folder is created |
| Notification Sent | `No` |
| Last Updated | current timestamp |
| Error Notes | blank |

Keep the row number output from this module. It is needed by the final update step.

### 3. Google Drive - Create a Folder

Parent folder: `Client Onboarding`

Folder name pattern:

```text
Client - {{company}} - {{YYYY-MM-DD}}
```

Example:

```text
Client - Northline Media - 2026-05-18
```

After the folder is created, use the folder web URL in the Gmail alert and in the final Sheet update.

### 4. Gmail - Send an Email

Recipient: internal operations inbox.

Subject pattern:

```text
New client onboarding: {{company}}
```

Email body should include:

- client name
- email
- company
- service requested
- budget
- notes
- Drive folder URL
- link to the tracking Sheet

Keep the message short so it is useful as an operational alert.

### 5. Google Sheets - Update a Row

Update the same row created in module 2:

| Sheet column | Value |
| --- | --- |
| Drive Folder URL | Google Drive folder URL |
| Notification Sent | `Yes` |
| Last Updated | current timestamp |
| Error Notes | blank |

## Simple Error Handling

Add one error handler route for the Drive and Gmail steps:

```text
Error -> Google Sheets - Update a row -> set Error Notes
```

Error row values:

- `Notification Sent`: `No`
- `Error Notes`: short error message from Make
- `Last Updated`: current timestamp

This keeps the failure visible in the same Sheet instead of hiding it in Make execution history only.

## Future Scaling

Only add extra modules after V1 works reliably:

- payment reminder email when `Payment Status` is still `Pending`
- delivery checklist folder templates
- client handoff email
- weekly status summary
- CRM sync

