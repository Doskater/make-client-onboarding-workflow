# Status Tracking Notes

## Payment Status

Recommended values:

- `Pending`
- `Invoice Sent`
- `Paid`
- `Overdue`
- `Refunded`

Default for a new submission:

```text
Pending
```

## Delivery Status

Recommended values:

- `Not Started`
- `In Progress`
- `Waiting on Client`
- `Delivered`
- `Closed`

Default for a new submission:

```text
Not Started
```

## Why These Fields Stay Manual

For V1, payment and delivery statuses should remain editable in Google Sheets. This keeps the workflow easy for a small team to understand and avoids building a complex CRM before the intake process is proven.

Later, these fields can trigger:

- payment reminder emails
- delivery update notifications
- client folder checklist generation
- weekly internal reports

