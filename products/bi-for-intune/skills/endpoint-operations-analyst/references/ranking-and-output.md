# Ranking and Output

Status: Preview 0.11.0. Ranking method decided by PowerStacks.

## Eligibility for the Main Briefing

A finding is eligible for the main five only if:

1. It was queried in this session.
2. It is based on the managed device population, or on one of these areas defined on another basis: data collection health (A1, counted by dependent devices; see below), check-in age (A2), recent Autopilot events (A10, counted within the event window), devices in Windows Update for Business reports but not in Intune (A14a), or Intune or co-managed records not marked as managed (A14e). These are the only exceptions. Enrollment failures (A10) and warranty coverage (A14d) never take a main slot.
3. It does not rely on a field marked "Not assessed" or unconfirmed without saying so.
4. It meets the briefing filters: at least `MinDevices` affected devices **and** at least `MinShare` of the applicable population. Where the applicable population is not established, follow the rule in [analysis areas](analysis-areas.md#applicable-population); never claim the share filter was met against an invented denominator.

The filters decide eligibility for the main five, not whether a problem matters. Everything else found by the completed checks goes in the "Additional findings" table.

**A1 (data collection health) under the filters.** A connector or token problem is tenant-level, so the share filter does not apply to it. Count the managed devices that depend on it where the model can identify them (for example managed Apple devices for the Apple push certificate) and apply `MinDevices` to that count; rank it by that count. When the model cannot count the dependent devices, write "tenant-wide; device count not determined". A connector that is expired or not in a success state is **always reported**: in the main briefing when it meets `MinDevices`, otherwise in "Additional findings" with the reason "always flagged (below briefing filters)" or "always flagged (device count not determined)". An expiry date that has already passed is reported there as current state, not as a deadline.

**A14a and A14e** use the applicable populations in [analysis areas](analysis-areas.md#applicable-population). A14e is always reported when at least one record exists (main briefing when it meets the filters, otherwise "always flagged (below briefing filters)").

## Ranking Method

**Default: ranked by scale.**

0. **Environment alert first.** A partial data load always leads the briefing, above any finding.
1. **Data collection first, only when material.** If a data collection issue materially undermines the analysis (see skill Step 1), place it first and say which findings it limits. Otherwise rank it like any other finding.
2. **Then by scale:** order eligible findings by distinct affected-device count, largest first. Use the full count (no check-in filter); the age-mix flag and check-in call-outs still apply.
3. **Ties:** order by share of the applicable population, then by area order (A1 to A16, skipping retired A13).

Call this "ranked by scale". Do not describe it as "highest risk", "most important", or "neutral". Scale says how many devices are affected, not how serious the problem is.

**Concentration is context, not a ranking factor.** Report it in the finding (for example "one script accounts for <n>% of these failures"). Do not infer that a concentrated problem is quick or easy to fix.

**No area is ranked up or down for its type.** Every area, including Endpoint Analytics (A11), is ranked by distinct affected devices under the same eligibility rules.

**Distinct findings only.** A finding that is part of a larger finding appears as a drill-down inside it (see skill Step 4). The same problem never takes two slots.

### Alternative Rankings (on request)

When the user asks, rerank and state the criteria used:

| `RankBy` | Criteria |
| --- | --- |
| `SecurityRelevance` | Findings about security controls (encryption, OS security updates and end of service, compliance, Defender when it is the antivirus) first, then the rest; by scale within each group. This groups findings by the type of control they concern. It is not a risk score and does not reflect the customer's own policy unless the user provides it. |
| `Concentration` | Order by the share of affected devices explained by the single largest item (app, profile, policy, script, error code). It shows where one item drives most of a problem; it does not mean the problem is easier to fix. |
| `Deadline` | Eligible findings with a source-reported date inside `DeadlineWindowDays` first, nearest date first; then the rest by scale. The eligibility rules and briefing filters are unchanged. |
| `Scale` | Default, as above. |

Do not invent customer policy, risk scores, or priorities. If the user states their own priorities, use theirs and say so.

## Upcoming Deadlines

Deadlines are shown **in their own compact section, outside the finding slots**. A date never moves a finding into the main five; ranking stays by scale unless the user asks for `RankBy = Deadline`.

- **What qualifies:** a source-reported date from the briefing date to `DeadlineWindowDays` days later, both ends included (default 14). In BI for Intune today: Windows feature update end-of-service dates (A7) and connector and token expiration dates (A1).
- **The window is a display window, not customer policy.** It decides which dates are listed here. It does not say how much notice the customer needs or whether a date is urgent. The user can change it.
- **Include every qualifying deadline in scope, whatever happens to the related finding**: in the main five, ranked below them, below the briefing filters, or with no separate finding (for example a connector expiry).
- **One row per date.** When several releases or editions share a date, show one row with the total and list the release and edition breakdown under the table. Say "next 1 day" (singular) when the window is 1.
- **For each deadline show:** the date as the source reports it; days remaining, in whole calendar days from the briefing date (the user's local date, skill Step 4a); the affected-device count; and in plain English what the date represents and which source reported it.
- **Affected devices:** count the managed devices the date applies to. For tenant-level items such as a connector expiry, count the devices that depend on it where the model can identify them (for example managed Apple devices for the Apple push certificate); otherwise say it applies tenant-wide and that the model cannot count the devices.
- **Cross-reference, do not repeat.** If the same issue is a main finding or an "Additional findings" row, give the reference (for example "see finding 2" or "see Additional findings") instead of repeating the explanation.
- **Dates as stated.** Never substitute a date from an external lifecycle reference. If the source looks inconsistent (for example devices on the same release and edition reporting different end-of-service dates), list the dates as reported with their counts and say "flagged for investigation". Different dates for different editions of a release are expected and are not flagged.
- **Past dates are not deadlines.** A date that has passed is current state and belongs in the findings (for example devices already at `End Of Service`).
- If no date falls in the window, write one line: "No source-reported deadlines in the next <n> days."
- **Next deadline beyond this window.** After the table (or the "no deadlines" line), add one line naming the nearest source-reported date after the window ends: "Next deadline beyond this window: <date> (<n> days), <what it is>, <n> devices." Use the same sources, day calculation, and wording rules as the table. If there is no later date in the data, omit the line. The line does not change ranking and is not a finding.


## Briefing Format

**Email subject.** When the briefing is sent by email, the subject line is "Daily AI Generated Endpoint Briefing <briefing date as MM/DD/YYYY>", for example "Daily AI Generated Endpoint Briefing 03/01/2027". The briefing date is the user's local date (skill Step 4a), never the UTC date: a briefing run in the evening in the Americas must not carry the next day's date. The briefing body is unchanged.

```markdown
## Endpoint Briefing

<Only for a partial load: **Environment alert:** Some data did not load in the latest refresh (<affected data in plain English>). Please run the data refresh again; if the problem persists, contact PowerStacks support. Also make sure BI for Intune is on the latest version. Areas that depend on this data are not assessed below.>
**Data as of:** <collection time> UTC (queried <query time> UTC). <Data collection note only if material.> <If the refresh history check flags it: "The latest data refresh took <n> minutes, unusually long compared with recent refreshes (median <m> minutes over the previous <k> completed refreshes).">
**Population:** <N> managed devices. Last check-in: <n> over 14 days, <n> over 30 days, <n> over 60 days, <n> over 90 days. <Windows scopes only: n are Cloud PCs.>
**Other device categories:** <n> devices managed by app protection policies only (no enrollment; see the app protection finding). <When app protection status is not linked to devices: "Devices managed by app protection policies only: not determined (see Not Assessed)."> <n> Windows Servers managed through Defender security settings. <Omit a category with no devices or outside the scope.>
**Coverage:** <Data turned off in settings: "<data> is turned off in your BI for Intune data settings; turning it on would add <what it adds>." For app assignment and remediation assignment details, add: "Turning these on may slow the data sync or cause sync failures."> <Missing sources, classified as in the model foundation: "Problem: <source> data is not present; please contact PowerStacks support." or "Not enabled or not present: <source>. Enabling it would add <what it adds>. Contact PowerStacks support if you expected this data."> <Whenever present: n devices recorded by Intune (or co-managed) are not marked as managed (n synced within 14 days); they are outside the managed population.> <Windows scopes: n managed Windows devices are not enrolled in Windows Update for Business reports, so they have no update status. Of these, n are Microsoft Entra registered, which Windows Update for Business reports does not support (n marked corporate-owned in Intune), and n have an unknown join type; n devices report to Windows Update for Business reports but are not in Intune (n scanned within 14 days).> <Windows or macOS scopes, when custom inventory is deployed: n managed devices are not reporting custom inventory (n Windows, n macOS; n checked in within 14 days). Only when at least one of them is a Windows device: "For the Windows devices, this includes their Microsoft 365 Apps data." Only when some exist: n managed Windows devices report custom inventory but have no Microsoft 365 Apps update data.> <Windows scopes with physical Dell, HP, Lenovo, or Getac devices that report custom inventory, classified with the warranty rule in analysis area A14d, each part only when it has devices: "Warranty reporting is not enabled: none of these n devices has a warranty record; turning on warranty collection would show factory and warranty dates for lifecycle planning." or "n of these devices have no warranty record (n checked in within 14 days); onboarding them to warranty reporting would show factory and warranty dates for lifecycle planning." and "n <vendors> devices have warranty records with no warranty dates (n checked in within 14 days); the warranty lookup may be failing for these vendors.">
**Method:** Ranked by scale (distinct affected devices). Briefing filters: at least <MinDevices> devices and at least <MinShare> of the applicable population. Scope: <scope>. Check-in bands: 14 / 30 / 60 / 90 days. No devices excluded by check-in age unless you ask. <Every input not at its default, with its value, for example "Up to 3 findings; primary antivirus: Defender."; then "All other inputs at their defaults."> Briefing date: <date as MM/DD/YYYY> (<time zone, for example Central Time (UTC-05:00)>; collection and query times are UTC).

### Upcoming Deadlines (next <DeadlineWindowDays> days)

Display window only; it is not a policy or urgency judgment.

| Date (as reported) | Days remaining | Affected devices | What it is | See |
| --- | --- | --- | --- | --- |
| <source date> | <n> | <n> | <plain English: what the date means, per <source>> | <finding n / Additional findings / Data Notes / -> |

<Inconsistency note only when one of the conflicting dates is in the window or is the next deadline: dates as reported with counts, "flagged for investigation". When the conflicting date has passed, the note belongs in the finding only.> <Or: "No source-reported deadlines in the next n days.">
Next deadline beyond this window: <date> (<n> days), <what it is>, <n> devices. <Omit if there is no later date.>

### 1. <Short finding title>

- **What we found:** <observed fact with numbers, values as the source states them>
- **Scope:** <n> of <applicable n> managed devices (<%>). Last check-in: <n> over 14 days, <n> over 30, <n> over 60, <n> over 90.
- **Status age:** <Where the source has a status time, report status age separately from device check-in age (Step 4). A recent check-in does not make an old status current.>
- **Concentration:** <optional: share explained by the largest item, as context only>
- **Drill-down:** <optional: sub-findings combined into this one, with their counts>
- **Overlap:** <optional: devices shared with another finding, when kept separate>
- **Why it matters:** <operational impact, without overstating>
- **Based on:** <plain-English description of the data used, for example "Intune's per-device remediation results for managed devices". No DAX, table or column names, or IDs.>
- **Next step:** <specific investigation step, no changes made>
- **Confidence:** <High / Medium / Low, and why. Lowered one level when the age-mix flag applies.>
- **Age mix:** <only when over half of these devices last checked in more than 14 days ago>
- **Affected devices:** <n> devices, oldest check-in first. <If more than DeviceDetailLimit: "Showing <limit> of <n>; ask for the full list."> <For a tenant-level finding with no countable devices: "No device list (tenant-level).">

| Device | Serial number | User | Department | OS | Last check-in (days) |
| --- | --- | --- | --- | --- | --- |
| <device name> | <serial> | <primary user name (UPN); or "Enrolled user: ..." / "Last logon user: ..."; or "No user associated"> | <department> | <OS> | <n; or "No Intune check-in" for records outside Intune> |

(Up to MaxFindings findings. If fewer are eligible, say how many and why.)

### Additional Findings

Findings identified by the completed checks that are not in the main briefing. This is not a complete list of every possible issue.

| Finding | Affected devices | Applicable | % | Why not in the main briefing |
| --- | --- | --- | --- | --- |
| <finding> | <n, or "not determined" (tenant-level)> | <n, "not established", "tenant-level", or "none (count only)"> | <% or "not determined"> | <Below briefing filters (devices or share) / Ranked below the top five by scale / Reporting opportunity / Possible warranty lookup problem / Always flagged (below briefing filters) / Always flagged (device count not determined) / Part of finding <x> (drill-down) / Applicable population not established / No denominator: reported as a count / Data limitation: <reason>> |

### Not Assessed

<Only areas that apply to this scope and have no data, or are excluded by an input such as PrimaryAntivirus. Omit this section if there are none.>

- <Area>: <why>.

### Data Notes

- <Refresh history, one line when not flagged: "Refresh history could not be checked (no access)." or "Refresh history could not be checked (service error)." or "Refresh history was not checked in this run." or "The latest data refresh took <n> minutes; refresh duration not assessed: only <k> previous completed refreshes (at least <minimum> needed)." or nothing when the duration is within the usual range.>
- <Refresh history, when a newer refresh is in progress or failed: "A newer data refresh started <time> UTC and had not finished when checked." or "A newer data refresh started <time> UTC and failed.">
- <A single table not present while related data loaded: "<data> is not present in this refresh; this can be a data-collection setting. Contact PowerStacks support if you expected it.">
- <An event table with no rows: "No <events> are recorded in this refresh, so no time window can be stated." Do not describe it as zero failures over a period.>
- <Only notes that change how a figure should be read: missing or unknown data, excluded records, Cloud PC notes for Windows scopes, values that look inconsistent in the source. Do not explain table mechanics such as rows versus devices; report device counts and leave it there.>

### Devices Not Checked In for More Than 14 Days

<n> managed devices: <n> over 14 days, <n> over 30, <n> over 60, <n> over 90. Oldest first. <If more than DeviceDetailLimit: "Showing the oldest <limit> of <n>; ask for the full list.">

| Device | Serial number | Platform | Ownership | Manufacturer and model | User | Department | Last logon user (if different) | Last check-in | Days | Flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <device name> | <serial> | <OS> | <ownership> | <manufacturer model> | <primary user name (UPN); or "Enrolled user: ..." / "Last logon user: ..."; or "No user associated"> | <department> | <name (UPN), last logon date> | <date> | <n> | <Over 90 / Over 60 / Over 30 / Over 14> |

Ask me to exclude devices that have not checked in for more than any number of days you choose (for example 14, 30, 60, or 90), to focus on a platform or group, or to change the briefing filters.
Ask me to rank by security relevance, scale, concentration, or nearest deadline, or to change the deadline window.
```

## Writing Rules

- Fewer than five main findings is a valid result.
- Below-filter findings are labeled "below briefing filters", never "insignificant", "minor", or "healthy".
- "No issue found" applies only to areas with data and only to what the checks examined. Areas without data are "not assessed".
- Summarize each finding with counts; list its individual devices only in the finding's "Affected devices" table (up to `DeviceDetailLimit`), and list stale devices in the list of devices not checked in for more than 14 days. The affected-device tables are the only device rows the executive outputs may use. For findings in "Additional findings", offer to list affected devices.
- Deduplicate device-user pairs before listing (analysis area A2) and apply `DeviceDetailLimit` to distinct devices.
- A failed result with error code 0 (0x00000000) is reported as stated, without interpretation.
- Any device list, including one given on request, uses the identifying details in the model foundation, section 14: serial number, user, and department as well as the device name.
- Never mask, redact, truncate, or alter values; show identifiers exactly as stored.
- Do not describe trends.
- Do not explain query mechanics (row counts, table grain, join keys) in the briefing.
- No DAX, model notation (`Table[Column]`), model IDs, or measure names in the briefing. Use plain English. Status values may be quoted as Intune shows them (for example "Not Latest").
- If asked how a figure was produced, explain in words first; give a query only if the user asks for it.
- Do not state the obvious, including that the data was only read (the connection cannot change the model). Mention only attributes and areas that can apply to the scope (Cloud PCs are Windows devices; never mention them in a scope without Windows). Do not list topics the model does not cover unless the user asks.
- Do not recommend or describe making changes; describe what to investigate. Exception: for an app error code, Microsoft's published guidance from [app error codes](app-error-codes.md) may be quoted, attributed to Microsoft and cited.
- Show error codes in hex first with the decimal in parentheses, for example 0xC7D14FB5 (-942583883).
- When a finding states which monthly security update was the latest at refresh (A7), derive it from Microsoft's published schedule (the second Tuesday of the month): the latest release is the second Tuesday of the refresh month if the refresh date is on or after it, otherwise the second Tuesday of the previous month. Say that this date comes from Microsoft's release schedule, not from the model.
- Always end with both offers: narrow by any check-in age or other exclusion the user chooses, and rerank (including by nearest deadline or with a different deadline window).
- Never exclude devices by check-in age on your own; the full managed population is the default.
- Never describe a finding's share as meeting the filter when its applicable population is not established; write "not determined" or the upper-bound wording from analysis areas.
