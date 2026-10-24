# BI for Intune

## Endpoint Operations Analyst (Preview)

A daily endpoint briefing built from your BI for Intune semantic model. Ask your AI assistant what your team should look at today, and it returns up to five findings ranked by how many devices each one affects.

Each finding includes:

- How many devices are affected, out of how many it applies to.
- How long ago those devices last checked in, so stale status is called out.
- Which policy, app, script, or error code accounts for most of the impact.
- Microsoft's guidance for app installation error codes, where Microsoft documents the code.
- A specific next step to investigate. The skill recommends; it never changes anything.

The briefing also lists upcoming source-reported deadlines (for example certificate and token expirations, and Windows end of service), additional findings below the briefing filters, areas it couldn't assess, and devices that haven't checked in for more than 14 days with serial numbers, users, and departments.

On request, it turns the briefing into an executive PowerPoint presentation and a one-page interactive HTML report.

### Get Started

See the [getting started guide](../../docs/getting-started.md). Install the folder [`skills/endpoint-operations-analyst`](skills/endpoint-operations-analyst/SKILL.md).

### Example Questions

- "Act as my endpoint operations analyst. Give me the five things my team should investigate this morning."
- "Same briefing, but only devices that checked in within the last 30 days."
- "Rank by security relevance."
- "Show me the devices behind the app installation finding."
- "Turn this briefing into an executive presentation and an HTML report."

### Requirements

BI for Intune version 70 or later. See [compatibility](../../docs/compatibility.md) and [known limitations](../../docs/known-limitations.md).
