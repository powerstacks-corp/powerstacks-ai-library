# Ranking and Output

Status: Preview 0.1.0. Written for and tested with the BI for Defender release 15 schema on 2026-10-23. Briefing wording is provisional and may change in later releases.

## Eligibility for the Main Briefing

A finding is eligible for the main briefing only if:

1. It was queried in this session.
2. It uses the population defined for its area in [analysis areas](analysis-areas.md): the default population (S1, S3) or assessed devices (S2, S4, S5).
3. It does not rely on a field the model foundation marks as unconfirmed without saying so.
4. It meets the briefing filters: at least `MinDevices` affected devices **and** at least `MinShare` of the applicable population.

The filters decide eligibility for the main briefing, not whether a problem matters. Everything else found by the completed checks goes in the "Additional findings" table.

## Ranking Method

**Default: ranked by scale.**

0. **Data age alert first.** When the data is older than `StaleDataDays`, the briefing opens with the alert, above any finding. It is not a finding and takes no slot.
1. **Then by scale:** order eligible findings by distinct affected devices, largest first. Use the full count; last-seen call-outs and the age-mix flag still apply.
2. **Ties:** order by share of the applicable population, then by area order (S1 to S5).

Call this "ranked by scale". Do not describe it as "highest risk" or "most important". Scale says how many devices are affected, not how serious the problem is.

**Concentration is context, not a ranking factor.** Report it in the finding (for example "one CVE accounts for <n> of these devices"). Do not infer that a concentrated problem is easy to fix.

**Distinct findings only.** The same problem never takes two slots. Related findings from different areas (for example S2 and S4) state their overlap.

### Alternative Rankings (On Request)

| `RankBy` | Criteria |
| --- | --- |
| `Concentration` | Order by the share of affected devices explained by the single largest item (CVE, product, KB, or end-of-support product). It does not mean the problem is easier to fix. |
| `Deadline` | Eligible findings with a source-reported date inside `DeadlineWindowDays` first, nearest date first; then the rest by scale. |
| `Scale` | Default, as above. |

Do not invent customer policy, risk scores, or priorities. If the user states their own priorities, use theirs and say so.

## Upcoming Deadlines

Deadlines appear **in their own section, outside the finding slots**.

- **What qualifies:** a source-reported date from the briefing date to `DeadlineWindowDays` days later, both ends included: end-of-support dates for active software on assessed devices, and the license end date.
- **The window is a display window, not customer policy.** The user can change it.
- **One row per date.** When several products share a date, show one row with the device total and name the products under the table.
- **For each deadline show:** the date as the source reports it; days remaining in whole calendar days from the briefing date (the user's local date, skill Step 1); affected devices (distinct); what the date represents and its source; and where the related finding is.
- **Dates as stated.** Never substitute a date from an external lifecycle reference.
- **Past dates are not deadlines.** A date that has passed, including one that passed after the data was collected, belongs in the findings.
- If no date falls in the window, write one line: "No source-reported deadlines in the next <n> days."
- **Next deadline beyond this window:** one line naming the nearest later date, its days remaining, what it is, and its device count. Omit it when there is none.

## Briefing Format

**Email subject.** When the briefing is sent by email, the subject line is "Daily AI Generated Security Briefing <briefing date as MM/DD/YYYY>". The briefing date is the user's local date (skill Step 1), never the UTC date. The body is unchanged.

```markdown
## Security Briefing

<Only when the data is older than StaleDataDays: **Data age alert:** The latest data in BI for Defender was collected on <date> at <time> (time as recorded in the model), <n> days before this briefing. Every figure below describes the state at that time. Check that the semantic model's scheduled refresh is running.>
**Data as of:** <collection date and time> (time as recorded in the model; time zone not stated). Assessment records span <first date> to <last date>.
**License:** <status as stated>, <type as stated>, ends <date>.
**Population:** <N> onboarded devices (not excluded). Last seen before data collection: <n> more than 7 days, <n> more than 14, <n> more than 30, <n> more than 60, <n> more than 90. <n> have vulnerability and software assessment data (assessed devices).
**Other device categories:** <n> discovered devices not onboarded; <n> excluded devices. <Omit a category with none.>
**Method:** Ranked by scale (distinct affected devices). Briefing filters: at least <MinDevices> devices and at least <MinShare> of the applicable population. Scope: <scope>. Last-seen bands: 7 / 14 / 30 / 60 / 90 days before data collection. No devices excluded by last-seen age unless you ask. <Every input not at its default, with its value; then "All other inputs at their defaults."> Briefing date: <date as MM/DD/YYYY> (<time zone, for example Central Time (UTC-05:00)>).

### Upcoming Deadlines (Next <DeadlineWindowDays> Days)

Display window only; it is not a policy or urgency judgment.

| Date (as reported) | Days remaining | Affected devices | What it is | See |
| --- | --- | --- | --- | --- |
| <date> | <n> | <n> | <plain English, per Microsoft Defender> | <finding n / -> |

<Products under the table when several share a date.> <Or: "No source-reported deadlines in the next n days.">
Next deadline beyond this window: <date> (<n> days), <what it is>, <n> devices. <Omit if none.>

### 1. <Short Finding Title>

- **What we found:** <observed fact with numbers, values as Defender states them>
- **Scope:** <n> of <applicable n> <assessed or onboarded> devices (<%>). Last seen before data collection: <n> more than 7 days, <n> more than 30, <n> more than 60, <n> more than 90. <For S2, S4, S5: n onboarded devices are not assessed (see the coverage finding).>
- **Status age:** <where the area has a record time: devices whose latest record is more than 7 days older than the data collection; how long findings have been listed (first seen more than 30 days before collection)>
- **Breakdown:** <severity and exploitability, top CVEs, products, KBs, or end-of-support products, with device counts>
- **Concentration:** <optional: share explained by the largest item, as context only>
- **Overlap:** <devices shared with another finding>
- **Why it matters:** <operational impact, without overstating>
- **Based on:** <plain English, for example "Microsoft Defender vulnerability assessment for onboarded devices, counted once per device, fixed vulnerabilities excluded". No DAX, table or column names, or IDs.>
- **Next step:** <specific investigation step, no changes made>
- **Confidence:** <High / Medium / Low, and why. Lowered one level when the age-mix flag applies.>
- **Age mix:** <only when over half of these devices were last seen more than 7 days before collection>
- **Affected devices:** <n> devices, oldest last-seen first. <If more than DeviceDetailLimit: "Showing <limit> of <n>; ask for the full list.">

| Device | OS and release | Users signed in (as recorded by Defender) | Department | Days last seen before collection |
| --- | --- | --- | --- | --- |
| <device name> | <OS, release> | <full name (user name); several separated by semicolons; or "No user associated"> | <department> | <n> |

(Up to MaxFindings findings. If fewer are eligible, say how many and why.)

### Additional Findings

Findings identified by the completed checks that are not in the main briefing. This is not a complete list of every possible issue.

| Finding | Affected devices | Applicable | % | Why not in the main briefing |
| --- | --- | --- | --- | --- |
| <finding> | <n> | <n> | <%> | <Below briefing filters / Ranked below the top findings by scale / Data limitation: reason> |

<Or one line: "None: every finding from the completed checks is in the main briefing.">

### Not Assessed

- Microsoft Defender Antivirus health, security configuration (including attack surface reduction rules), incidents and alerts, and Secure Score: not part of this Preview.
- <Any area whose data is missing, with the reason.>

### Data Notes

- <Device IDs in the assessment data with no device record: n, holding about n% of active vulnerability records; excluded from every count. Report pages may include them.>
- <Only notes that change how a figure should be read: data age, devices without assessment data and why (observed or inferred, labeled), values that look inconsistent in the source, "listed as missing" ages measured from first seen. Do not explain query mechanics.>

### Devices Not Seen for More Than 7 Days

<Only when the devices-not-reporting finding is not in the main briefing; otherwise its Affected devices table is this list.> <n> onboarded devices: <n> more than 7 days, <n> more than 30, <n> more than 60, <n> more than 90 before data collection. Oldest first. <If more than DeviceDetailLimit: "Showing the oldest <limit> of <n>; ask for the full list.">

| Device | OS and release | Manufacturer and model | Users signed in (as recorded by Defender) | Last seen | Days before collection | Device state (as reported) | Assessment data | Flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <device name> | <OS, release> | <manufacturer model, or "Not reported"> | <full name (user name), department; or "No user associated"> | <date> | <n> | <Active / Inactive> | <Yes / No> | <Over 90 / Over 60 / Over 30 / Over 14 / Over 7> |

Ask me to exclude devices not seen for more than any number of days you choose, to focus on one OS, or to change the briefing filters.
Ask me to rank by concentration or nearest deadline, or to change the deadline window.
```

## Writing Rules

- Fewer than five main findings is a valid result.
- Below-filter findings are labeled "below briefing filters", never "insignificant", "minor", or "healthy".
- "No issue found" applies only to areas with data and only to what the checks examined. Devices without assessment data are "not assessed", never "no vulnerabilities".
- Use Defender's values as stated: severity (for example "Critical"), exploitability ("Exploitable"), status values, release names of updates, and end-of-support statuses. Show CVE IDs and KB numbers as Defender gives them, with the "KB" prefix for KB numbers.
- Summarize each finding with counts; list its individual devices only in the finding's "Affected devices" table (up to `DeviceDetailLimit`). These tables are the only device rows the executive outputs may use. For findings in "Additional findings", offer to list affected devices.
- Never mask, redact, truncate, or alter values; show identifiers exactly as stored.
- Do not describe trends.
- Do not explain query mechanics. No DAX, model notation (`Table[Column]`), model IDs, or measure names in the briefing.
- If asked how a figure was produced, explain in words first; give a query only if the user asks for it.
- If the user compares a figure with a BI for Defender report page, explain the difference in plain English (for example, the page counts fixed vulnerabilities or divides by every device record).
- Do not recommend or describe making changes; describe what to investigate.
- Do not call "first seen" ages patch lag or time since release.
- Never describe old data as current; when the data age alert applies, every finding describes the state at collection.
- Always end with both offers: narrow the scope and rerank.
- Never exclude devices by last-seen age on your own; the full default population is the default.
