# Upwork Proposal Draft

AMRL MAKE

Hi, I can build this as a clean V1 Make.com workflow without overcomplicating it.

I would structure it like this:

```text
Form submission or webhook
-> add client row in Google Sheets
-> create Google Drive client folder
-> send Gmail internal alert
-> update the same Sheet row with folder link, notification status, payment status, and delivery status
```

For the first version I would keep the workflow simple: one main scenario, clear module names, a readable Google Sheet, basic error notes written back into the Sheet, and a short handoff document so your team can edit statuses later.

Relevant examples:

- Make/Google workflow proof: https://github.com/Doskater/make-client-onboarding-workflow
- Tracking-sheet automation example: https://github.com/Doskater/local-service-business-automation-hub
- Webhook/integration reliability example: https://github.com/Doskater/front-asana-task-router

For the Make/Google proof, I prepared the workflow structure, setup docs, a redacted scenario snapshot, demo outputs, and clean screenshots of the live Make scenario canvas and Google Sheet tracker.

My suggested V1 structure:

- Google Sheet columns for client details, payment status, delivery status, Drive folder URL, notification status, and error notes
- Drive folder naming like `Client - Company - YYYY-MM-DD`
- Gmail alert to the internal operations inbox with the client details and folder link
- simple error handling that writes the issue into the tracking row instead of hiding it only in Make history
- short setup guide and walkthrough documentation

I can deliver the Make scenario, test it with demo submissions, document how to use it, and leave the structure editable for future scaling.
