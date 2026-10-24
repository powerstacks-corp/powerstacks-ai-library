# BI for Defender

## Security Operations Analyst (Preview)

A security briefing built from your BI for Defender semantic model. Ask your AI assistant what your security team should look at today, and it returns findings ranked by how many devices each one affects.

The Preview covers:

- **Data collection and coverage:** how current the data is, the license record, and onboarded devices that have no vulnerability or software assessment data, so their exposure is unknown rather than clean.
- **Critical and exploitable vulnerabilities:** devices with at least one active vulnerability that Microsoft Defender rates Critical or that has a known exploit, out of the devices that have assessment data. Fixed vulnerabilities are left out.
- **Missing Microsoft security updates:** counted by KB, with the devices that need each one.
- **End-of-support software:** software at or past its end-of-support date, plus upcoming end-of-support dates.
- **Devices not reporting:** onboarded devices not seen for more than 7 days, with 14, 30, 60, and 90 day call-outs.

Each finding gives the affected and applicable device counts, why it matters, and a next step. The skill recommends; it never changes anything. On request, it turns the briefing into an executive PowerPoint presentation and a one-page interactive HTML report.

Not covered yet: Microsoft Defender Antivirus health, security configuration (including attack surface reduction rules), incidents and alerts, and Secure Score.

### Get Started

See the [getting started guide](../../docs/getting-started.md). Install the folder [`skills/security-operations-analyst`](skills/security-operations-analyst/SKILL.md).

### Example Questions

- "Act as my security operations analyst. Give me today's security briefing."
- "Which devices have exploitable vulnerabilities, and which updates would fix the most of them?"
- "Show me the devices that haven't been seen for more than 30 days."
- "Turn this briefing into an executive presentation and an HTML report."

### Requirements

BI for Defender (tested with release 15). Defender fields describe Microsoft Defender only. See [compatibility](../../docs/compatibility.md) and [known limitations](../../docs/known-limitations.md).
