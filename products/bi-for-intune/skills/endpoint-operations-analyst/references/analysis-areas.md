# Analysis Areas

Status: Preview 0.11.0. Query patterns written for BI for Intune version 69 and tested with version 70 on 2026-10-23. Confirm names at runtime.

## Shared Pattern: Managed Device Set

Define the set once and apply it to any table with `TREATAS`, so counts do not depend on relationship paths.

```dax
DEFINE
    VAR Active =
        CALCULATETABLE (
            VALUES ( Device[Intune Device ID] ),
            Device[Is Managed] = TRUE (),
            Device[Managed By] IN { "Intune", "Co-Managed" }
        )
    VAR Affected =
        CALCULATETABLE (
            VALUES ( 'User Devices'[Intune Device ID] ),
            'Application State'[App Status] = "Failed",
            TREATAS ( Active, 'User Devices'[Intune Device ID] )
        )
EVALUATE
ROW (
    "Managed devices", COUNTROWS ( Active ),
    "With failed app installs", COUNTROWS ( Affected ),
    "  of which check-in over 14 days",
        CALCULATE ( DISTINCTCOUNT ( Device[Intune Device ID] ),
            TREATAS ( Affected, Device[Intune Device ID] ), Device[Last Check-In (Days)] > 14 ),
    "  over 30 days",
        CALCULATE ( DISTINCTCOUNT ( Device[Intune Device ID] ),
            TREATAS ( Affected, Device[Intune Device ID] ), Device[Last Check-In (Days)] > 30 ),
    "  over 60 days",
        CALCULATE ( DISTINCTCOUNT ( Device[Intune Device ID] ),
            TREATAS ( Affected, Device[Intune Device ID] ), Device[Last Check-In (Days)] > 60 ),
    "  over 90 days",
        CALCULATE ( DISTINCTCOUNT ( Device[Intune Device ID] ),
            TREATAS ( Affected, Device[Intune Device ID] ), Device[Last Check-In (Days)] > 90 )
)
```

Add `Scope` filters (for example `Device[OS] = "Windows 11"`) inside `CALCULATETABLE`. Add an `ActiveDays` filter only if the user asked to limit the analysis.

DAX notes:

- Quote table names in single quotes. `Application` is a reserved word and fails unquoted.
- Exclude BLANK before comparing day counts.
- Test Boolean flags as TRUE or not TRUE (`== TRUE()` or `<> TRUE()`); flags are often blank instead of FALSE. A plain `= FALSE()` also matches BLANK (for example `Disk S.M.A.R.T Predict Failure`, which is often blank).
- Several `Device` records can share one `Intune Device ID` across sources. When you group or filter by `Device` columns (OS, ownership, check-in) for a device set, repeat the managed filter (`Is Managed = TRUE`, `Managed By` in `Intune` or `Co-Managed`) so attributes from non-managed records do not leak in.
- Use `DISTINCTCOUNT` of the device key on the status table for device counts.
- To group a status table by a filtered value inside `SUMMARIZECOLUMNS`, pass the filter as a table (`TREATAS({"Failed"}, 'Application State'[App Status])`), not as a boolean expression.
- Discover columns with `INFO.VIEW.COLUMNS()` or the schema tool. Do not sample rows (`TOPN`) to find column names.

## Shared Pattern: Device List for a Finding

Use this pattern for every device list: a finding's affected devices and the devices not checked in for more than 14 days. It returns one row per device. Do not combine `User Devices` and `User` rows directly (for example with `SUMMARIZECOLUMNS` over columns of both tables): `User Devices` has one row per device-user association, and some associations repeat, so devices appear several times or are paired with every user.

Replace `Affected` with the finding's device set (any one-column table of `Intune Device ID` values from the managed device set). Device attributes come from the device's managed record; users come from `User Devices` rows with `Primary User` = TRUE for that device, looked up in `User`.

```dax
DEFINE
    VAR Active =
        CALCULATETABLE (
            VALUES ( Device[Intune Device ID] ),
            Device[Is Managed] = TRUE (),
            Device[Managed By] IN { "Intune", "Co-Managed" }
        )
    VAR Affected =
        CALCULATETABLE (
            VALUES ( 'User Devices'[Intune Device ID] ),
            'Application State'[App Status] = "Failed",
            TREATAS ( Active, 'User Devices'[Intune Device ID] )
        )
    VAR AffectedIds =
        CALCULATETABLE ( VALUES ( Device[Intune Device ID] ), TREATAS ( Affected, Device[Intune Device ID] ) )
    VAR DeviceList =
        GENERATE (
            AffectedIds,
            VAR DevId = Device[Intune Device ID]
            VAR ManagedRecord =
                CALCULATETABLE (
                    Device,
                    REMOVEFILTERS ( Device ),
                    Device[Intune Device ID] = DevId,
                    Device[Is Managed] = TRUE (),
                    Device[Managed By] IN { "Intune", "Co-Managed" }
                )
            VAR PrimaryUsers =
                CALCULATETABLE (
                    VALUES ( 'User Devices'[User ID] ),
                    REMOVEFILTERS ( Device ),
                    'User Devices'[Intune Device ID] = DevId,
                    'User Devices'[Primary User] = TRUE ()
                )
            VAR Users =
                CALCULATETABLE ( 'User', REMOVEFILTERS ( Device ), TREATAS ( PrimaryUsers, 'User'[User ID] ) )
            VAR UserNames = CONCATENATEX ( Users, 'User'[Full Name], "; ", 'User'[Full Name] )
            RETURN
                ROW (
                    "Device name", MAXX ( ManagedRecord, Device[Device Name] ),
                    "Serial number", MAXX ( ManagedRecord, Device[Serial Number] ),
                    "OS", MAXX ( ManagedRecord, Device[OS] ),
                    "Last check-in (days)", MINX ( ManagedRecord, Device[Last Check-In (Days)] ),
                    "Primary user", IF ( ISBLANK ( UserNames ), "No user associated", UserNames ),
                    "Department", CONCATENATEX ( Users, 'User'[Department], "; ", 'User'[Full Name] )
                )
        )
EVALUATE
DeviceList
ORDER BY [Last check-in (days)] DESC
```

- Tested with BI for Intune version 70 on 2026-10-23: one row per device for every managed device and for a finding's affected devices, with a device that has repeated primary-user rows shown once.
- A device with several primary users shows them in one row, separated by semicolons, with departments in the same order. A device with no primary user shows "No user associated"; for it, look up the enrolled user, then the last logon user (`Enrolled User` or `Last Logon User` = TRUE in the same way) and label which one is shown (model foundation, section 14).
- Add other identifying columns from the managed record in the same way (for example `Ownership`, `Device Manufacturer`, `Device Model`).
- Apply `DeviceDetailLimit` to the rows of this result, which are distinct devices. When there are more devices than the limit, report the total.

## Applicable Population

Unless an area says otherwise, the applicable population for `MinShare` is managed devices that have a status row for the area, excluding `Not Applicable`. Report `Unknown` and blank statuses as unknown, not as part of the healthy group.

**Where the applicable population is not established, do not invent one.**

1. Show the affected count and say that the applicable population is not established, and why.
2. Do not report a percentage of an invented denominator, and do not say the share filter was met.
3. You may still check the filter against a known upper bound: the managed devices in scope. Affected devices cannot exceed it, so if the affected count is at least `MinShare` of the managed devices in scope, the filter is met; say "at least n% of managed devices in scope". This works only when the affected items are managed devices.
4. If that bound does not apply or does not settle it, the finding is not eligible for the main briefing. List it in "Additional findings" with the reason "applicable population not established".

| Area | Applicable population | Status |
| --- | --- | --- |
| A2 | All managed devices in scope | Defined |
| A3 | Managed devices in scope (from the device's overall compliance) | Defined |
| A4, A5, A6 platform scripts, A8, A11, A12 | Managed devices with a status row for the area, excluding `Not Applicable` | Defined (default rule) |
| A6 remediations | Managed devices with at least one known remediation result: `Success`, `Skipped`, `Remediation Failed`, or `Script Error`. Exclude `Not Applicable` and `Unknown`. | Defined |
| A7 | Managed Windows devices with a non-blank security update status (end of service: with a non-blank end-of-service date) | Defined |
| A10 Autopilot | Autopilot deployments in the table's window | Defined |
| A10 enrollment failures | None exists: failed enrollment attempts are events, not managed devices, and the model has no count of attempts. | **No denominator by design.** Report all failures in the window as a count; no percentage. |
| A14a | Windows devices known to Windows Update for Business reports (managed Windows devices enrolled in it, plus the records found only there) | Defined (eligible for the main briefing; see eligibility rule 2 in ranking and output) |
| A14b | Managed Windows devices that are Microsoft Entra joined or hybrid joined; Microsoft Entra registered devices are reported as not supported | Defined |
| A14c | Managed Windows and macOS devices (Microsoft 365 drill-down: managed Windows devices) | Defined |
| A14d | Physical managed Windows devices from Dell, HP, Lenovo, or Getac that report custom inventory (the warranty base) | Defined (not eligible for the main briefing) |
| A14e | Records with `Managed By` of `Intune` or `Co-Managed` | Defined (eligible for the main briefing; always reported when present) |
| A15 | Managed Windows devices with a Microsoft 365 status other than `Unknown` | Defined |
| A16 | Devices with app protection status linked to a device (MAM-WE and enrolled devices), by platform | Defined |
| A1 | Tenant-level. No share filter; `MinDevices` applies to the managed devices that depend on the connector where the model can identify them (see ranking and output, "A1 under the filters") | Dependent devices, or not determined |

## Area Summary

| ID | Area | Status | Platforms | Primary source |
| --- | --- | --- | --- | --- |
| A1 | Data collection health | Supported | All | `Authorization`, `Connector & Token`, `Device[Last Check-In]` |
| A2 | Check-in age | Supported | All | `Device[Last Check-In (Days)]` |
| A3 | Device compliance | Supported | All | `Device[Compliance]`, `Compliance Policy State`, `Compliance Policy` |
| A4 | Configuration profile errors and conflicts | Supported | All | `Configuration State`, `Configuration` |
| A5 | App deployment failures | Supported | All | `Application State`, `Application`, `Application Error Code`, `User Devices` |
| A6 | Script and remediation failures | Supported | Windows (platform scripts also macOS) | `Script State`, `Script`, `Proactive Remediation State`, `Proactive Remediation` |
| A7 | Windows update posture | Supported with caveats | Windows | `Device` OS update columns, `Windows Update Ring State`, `Windows Feature Update State` |
| A8 | Disk encryption | Supported | Windows, macOS | `Device Encryption` |
| A9 | Defender Antivirus health (real-time, tamper, signatures) | Only when `PrimaryAntivirus = Defender` | Windows | `Windows Protection` |
| A10 | Enrollment and Autopilot failures | Supported (recent window only) | Enrollment: all; Autopilot: Windows | `Device Enrollment Failure`, `Autopilot Deployment State` |
| A11 | Endpoint Analytics health | Supported with caveats | Windows | `Device Performance`, `Device App Reliability` |
| A12 | Disk health | Supported with caveats | Windows, macOS | `Device Physical Disk` |
| A13 | macOS update policy status | Retired; do not query or report as not assessed | n/a | n/a |
| A14 | Management and reporting coverage | Supported | Windows (A14c also macOS) | `Device[Managed By]`, `Device[Update Compliance Enrolled]`, `Device[Last WU Scan (Days)]`, custom inventory flags, `Device Warranty` |
| A15 | Microsoft 365 Apps update status | Supported | Windows | `Device Microsoft 365[M365 Status]` |
| A16 | App protection | Supported (v70 and later) | iOS/iPadOS, Android, Windows | `App Protection State`, `App Protection`, `App Protection Type`, `App Protection Policy`, `User Devices`, `Device[Managed By]` |
| U1 | Third-party antivirus health | **Unsupported**: no third-party antivirus data in the model | n/a | n/a |
| U3 | Trends over time | **Unsupported**: current-state model | n/a | n/a |

Platform applicability is based on the data each area uses. Remediations, Endpoint Analytics, Defender, and Windows Update data are Windows-only; check `Device Physical Disk` coverage at runtime.

## Area Details

### A1 Data Collection Health

- Optional refresh history check: an unusually long latest refresh is reported with its duration, baseline median, and sample size, as a data collection note; it is never evidence of missing data on its own.
- Read the data settings first, approved settings only (never read `ApiKey`, `AzureAD TenantID`, `AzureAD ClientID`, `AzureAD ClientSecret`). A setting that is off explains its missing data.
- Missing data is classified with the model foundation, section 7: problems (partial load; all Log Analytics data missing) lead the briefing or the Coverage line with the instruction to contact PowerStacks support; options not enabled are reported as possible missed opportunities; a single empty table is reported as possibly a data-collection setting.

- Freshness query from the model foundation.
- `Connector & Token`: `Connector State`, `Last Sync (Days)`, `Expiration Date (Days)`, `Is Expired`.
- Finding when: a connector is expired or not in a success state, a connector the customer relies on has not synced recently, or the latest device check-in is far older than the refresh time.
- `Connector & Token[Expiration Date]` is a source-reported date. Expiration dates within `DeadlineWindowDays` go in "Upcoming deadlines" (see ranking and output). Calculate days remaining from the briefing date, not from `Expiration Date (Days)`, which was calculated at refresh.
- A connector that is expired or not in a success state is always reported (ranking and output, "A1 under the filters"). Count dependent managed devices where the model identifies them (for example managed Apple devices, every Apple OS label, for Apple connectors); otherwise say it applies tenant-wide and the device count is not determined.
- Which connectors are expected to sync regularly is not confirmed (provisional; report the last sync as stated and say it is unconfirmed whether that connector is expected to sync). An old `Last Sync` can be normal for an unused connector.

### A2 Check-In Age

- Report how many managed devices last checked in more than 14, 30, 60, and 90 days ago, by OS and ownership. Long-silent devices can be a lifecycle finding of their own (lost, retired, or unused).
- This is a lifecycle and data-currency finding: devices may be lost, retired, or unused. It is not proof of any other problem.
- Their last known compliance or update state belongs here, labeled as last known.
- For the briefing filters, A2 uses all managed devices in scope as the applicable population.
- The age-mix flag does not apply to A2.
- **Device details:** list the managed devices last checked in more than 14 days ago, oldest first, with the identifying details in the model foundation, section 14 (device name, serial number, platform, ownership, manufacturer and model, user, department, last logon user when different), last check-in date, days since check-in, and a flag for the highest band that applies (over 14, over 30, over 60, over 90). Repeat the managed filter when reading `Device` columns. Show device names exactly as stored, including any personal names they contain. Show up to `DeviceDetailLimit` rows in the briefing; if there are more, say how many there are in total and offer the full list.
- Build the list with the [device list pattern](#shared-pattern-device-list-for-a-finding), with the devices over 14 days as the device set.
- For every device list, deduplicate identical device-user pairs before formatting or applying `DeviceDetailLimit`. Use distinct pairs of `Intune Device ID` and `UPN` from `User Devices`; retain all different users and their role and last-logon details under the device, following model foundation section 14. Apply the limit to distinct devices, not association rows. Do not merge users with different UPNs or alter their displayed values.
- State the oldest check-in age present. Intune's device cleanup rule (default 90 days, configurable per tenant) removes devices beyond that limit, so devices silent for longer are not in the data and cannot be counted.

### A3 Device Compliance

- Count from `Device[Compliance]` only (the device's overall compliance state). Example: managed devices with `Device[Compliance] = "Non Compliant"`.
- To explain the cause only, break the non-compliant devices down by policy: `Compliance Policy State` with `Policy Status = "Non Compliant"`, grouped by `'Compliance Policy'[Policy Name]`. The policy table has one row per device per policy, so do not use it to count compliant or non-compliant devices.
- Group by `Device[Compliance]` and report every value present by name (for example `Not Evaluated`, `See ConfigMgr`, `In Grace Period`), as Intune reports it. Do not rely on the per-state measures, which only cover some values.
- For the cause, use `Compliance Policy Setting State` joined through `deviceCompliancePolicy.id` from `Compliance Policy State`. It has no device key, so its counts are status records, not devices. If the most common failing setting is the built-in "has a compliance policy assigned" check, that points to policy targeting rather than device drift.
- Break down by `Device[OS]` and `Device[Ownership]`; platform concentration is often the clearest signal.

### A4 Configuration Profile Errors and Conflicts

- Distinct `Configuration State[Intune Device ID]` with `Configuration Status` in `Error` or `Conflict`, grouped by `'Configuration'[Configuration Name]`.
- Profiles with a high error share among their applicable devices are stronger findings than broad low-level noise.

### A5 App Deployment Failures

- Distinct `'User Devices'[Intune Device ID]` with `'Application State'[App Status] = "Failed"`, grouped by `'Application'[App ID]` and name, with the applicable count (`App Status <> "Not Applicable"`).
- **App Status values.** Group by `App Status` first and account for every value present. Values seen in BI for Intune version 70: `Installed`, `Not Installed`, `Failed`, `Uninstall Failed`, `Not Applicable`, and blank. Two are failures:
  - `Failed` (install failed) is the main count of this finding.
  - `Uninstall Failed` (an uninstall assignment did not remove the app) is reported **inside the same finding as its own drill-down**, with its own distinct device count, the apps involved, and its error codes, and with the device overlap with `Failed`. Do not add it to the install failure count. If no device has `Failed` but some have `Uninstall Failed`, the uninstall failures are the A5 finding.
  - `Not Installed` is not a failure; report it only when asked. Blank status is unknown; report its row count in Data Notes, not as healthy or failed.
  - Any other value is reported as stated with its device count, under Data Notes, without interpretation.
- Break down by app type (`'Application Type'[App Type]`, for example "Microsoft Store app (new)", "Windows app (Win32)"): for each type with failures, give distinct devices with a failure, the applicable devices for that type, and how many apps of that type fail, largest first. Report type names as the data states them.
- Break down by the raw `'Application State'[App Error Code]` column, then look up `'Application Error Code'[App Error Message]` where it exists. Show each code in hex first with the decimal in parentheses, for example 0xC7D14FB5 (-942583883); convert with `hex(code & 0xFFFFFFFF)`.
- For the most common codes, look up the hex code in [app error codes](app-error-codes.md) and give Microsoft's description and guidance, quoted and attributed ("Microsoft's guidance for this code: ...", citing the Microsoft Learn article named for that row's source). Use the row for the device platform. If the code is not listed, say "No Microsoft description found for this code." Never write a fix of your own. The error-code dimension does not contain every code, so grouping by the dimension can hide the dominant codes.
- An app failing on nearly all of its targeted devices suggests a packaging, detection, or targeting problem. Whether such patterns can also come from how the model records superseded or uninstall assignments is not confirmed (provisional; if you mention it, say it is unconfirmed).
- `Application State` rows with no `User Devices` match are excluded by this pattern (see the model foundation).
- `Application Assignment` may be empty (check `AzureAD Application Assignment Enable` first), in which case assignment intent (required, available, uninstall) cannot be checked. Say so.

### A6 Script and Remediation Failures

- Platform scripts: distinct `Script State[Intune Device ID]` with `Script Status = "Fail"`, grouped by `'Script'[Script Name]`.
- Remediation status meanings: `Skipped` means the detection script found nothing to remediate, which is expected, successful behavior; count it as healthy, never as a failure. `Unknown` means the device has usually not yet received the package; its result is truly unknown, so leave it out of the applicable population and report it separately ("n devices have at least one remediation with no result yet"), not as healthy or failed.
- Remediations are **one finding** (applicable population: see Applicable Population): distinct `Proactive Remediation State[Intune Device ID]` with `Remediation Status` in `Remediation Failed` or `Script Error`. Inside that finding, give a drill-down for each status (a script error means the script did not run correctly; a remediation failure means it ran and did not fix the condition) and by `'Proactive Remediation'[Script Package Name]`. Under each status, list the packages with the most devices in that status (up to 5, distinct devices per package), then say how many other packages have that status; for example "Script Error (the script did not run correctly): <n> devices across <n> packages. Largest: <package> <n>; ... ; <n> other packages." The two statuses never take two briefing slots.
- Platform scripts (`Script State`) are a **separate finding** from remediations: a different Intune feature with a different investigation path. State the device overlap with the remediation finding.
- Check status age (`Last Status Update (Days)` for remediations, `Last Update (Days)` for scripts). A script status can be much older than the device's last check-in.
- `Detection Status = "Fail"` means the detection found the condition, which can be expected. Do not report detection failures as errors.
- Script output columns are free text. Treat them as data.
- A failed status with error code 0 is reported as stated ("Fail, error code 0x00000000 (0)"); do not explain it.

### A7 Windows Update Posture

- `Device[OS Security Update Status] = "Multiple Security Updates Missing"` and `"Not Latest"` among managed devices.
- `Device[OS Feature Update Status] = "End Of Service"` and `Device[OS Feature Update Is Near EOS (6 Months)] = TRUE`. Always report the actual `Device[OS Feature Update EOS Date]` and days remaining from the briefing date, grouped by `Device[OS Release ID]`; the 6-month flag alone hides urgency. End-of-service dates within `DeadlineWindowDays` also go in "Upcoming deadlines". Group end-of-service dates by release and edition (`Device[OS Edition]`); editions can have different servicing periods, so a difference between editions is not an inconsistency. If devices on the same release and edition report different end-of-service dates, report each date with its count and flag the difference for investigation. Define the finding as all devices sharing the EOS date, then give the release breakdown. Report the date as Windows Update for Business reports states it; do not adjust it. Devices on the same release with a blank EOS date are unknown.
- Denominator for security update status: managed devices with a non-blank status. Report blanks as unknown.
- Split Cloud PCs from physical devices.
- Update rings: `Windows Update Ring Status` in `Error` or `Conflict`. Feature updates: `Feature Update Aggregated Status = "Error"`.
- **Findings in A7 (exception to one finding per area):** security update status, end of service on a given date, and update ring or feature update profile errors are **separate findings**: they come from different mechanisms and need different investigation. State the device overlap between them (for example devices both behind on security updates and reaching end of service). Do not fold one into another as a drill-down.
- These values come from Windows Update for Business reports and are reported as the source states them (see the model foundation for their documented meaning). Name the source in the finding and state which monthly security release was the latest at refresh. The model has no field for this: derive it from Microsoft's schedule (second Tuesday of the month) as described in the writing rules of ranking and output, and say the date comes from that schedule.
- A device's release (from the Windows Update Distribution report) and its end-of-service date (from Windows Update for Business reports) come from different sources. Flag only different end-of-service dates on the same release and edition; report a release label that disagrees with its end-of-service date as stated, without flagging it.

### A8 Disk Encryption

- Distinct `Device Encryption[Intune Device ID]` with `Encryption Status = "Not Encrypted"` among managed devices, by OS.
- Use `Encryption Readiness` and `Encryption Status Details` to suggest why. "Encryption method ... different than that set by policy" may mean the disk is encrypted with a different method; treat it as a policy mismatch, not proof of an unencrypted disk. If a device shows a "Success" detail with a Not Encrypted status, report that as an inconsistency.
- Exclude Cloud PCs from the encryption finding. Cloud PCs (Windows 365) are Microsoft-hosted virtual machines and are not normally encrypted, so their `Not Encrypted` status is expected. Mention the Cloud PC count in Data Notes as expected, not as a gap.
- Whether every OS reports encryption here is not confirmed (provisional; report devices with no row as unknown and say so).

### A9 Defender Antivirus Health

- Assess only when `PrimaryAntivirus = Defender`. With `ThirdParty` or `Unknown`, report A9 as not assessed and say why: Defender fields show Defender's own state, which is expected to be off or out of date when another antivirus is in use.
- When assessed: `Windows Protection[RealTime Protection Enabled]` not TRUE, `[Tamper Protection Enabled]` not TRUE, and `[Signature Update Overdue] = TRUE` (test flags as TRUE or not TRUE; never test for FALSE) among managed devices. Split Cloud PCs from physical devices.
- If `Unknown`, the briefing may note what the Defender fields show (for example "real-time protection is off on most devices, which usually means another antivirus is in use") and ask the user to confirm.

### A10 Enrollment and Autopilot Failures

- `Device Enrollment Failure`: failures within the covered window, counted as distinct `Enrollment Failure ID` (the table can hold more than one row per failure), by `Failure Category` and `Failure Reason` (a failure can appear under more than one category, so category counts can add up to more than the total). State the window (`MIN` and `MAX` of `Enrollment Failure Time`).
- `Autopilot Deployment State[Ap Deployment State] = "Failure"`, with `Enrollment Date` to judge recency. The table covers recent deployments only; state its window.
- When either table has no rows, write in Data Notes that no such events are recorded in this refresh, so no window can be stated. Do not report it as zero failures over a period, and do not classify it as a missing source.
- For the briefing filters, Autopilot failures use the deployments in the window as the applicable population. Enrollment failures have no denominator. Always report **all** enrollment failures in the covered window: the total count of distinct failures, the window dates, and the breakdown by category and reason. Give no percentage and do not apply the share filter. In a scoped briefing, report the tenant-wide total and say it is not limited to the scope, because failed attempts cannot be reliably matched to a platform, release, or group. Place the row in "Additional findings" with the reason "no denominator: reported as a count"; it does not take a main slot.

### A11 Endpoint Analytics Health

- `Device Performance[Performance Health Status] = "Needs Attention"` and `Device App Reliability[Device App Reliability Health Status] = "Needs Attention"`.
- **One finding:** devices with startup performance or app reliability "Needs Attention" (the union of devices), with a drill-down for each score. Applicable population: managed devices with a row in either table. Report blank scores as unknown.
- Caveat: Endpoint Analytics data covers only enrolled devices, and "Needs Attention" is Microsoft's scoring; say so in the finding.
- Rank it by distinct affected devices under the same eligibility rules as every other finding. Concentration (for example a high share of Cloud PCs) can be explained in the finding but does not change its default rank.

### A12 Disk Health

- Distinct `Device Physical Disk[Intune Device ID]` with `[Disk S.M.A.R.T Predict Failure] = TRUE`, and `[Disk Health Status]` values other than healthy, among managed devices.
- Report "none flagged" only if the table has rows for the population; otherwise "not assessed".

### A13 macOS Update Policy Status (Retired)

Retired from the active survey. Do not query it, require its schema, or report it as not assessed. Keep A13 reserved so other area IDs do not change.

### A14 Management and Reporting Coverage

Five checks. Each is its own finding (different cause and investigation path).

**A14a: Active in Windows Update for Business reports but not in Intune.**

- Records with `Device[Managed By] = "Update Compliance"` (these are not in the managed population; count records).
- Call out how many last scanned with Windows Update within 14, 30, and 60 days (`Device[Last WU Scan (Days)]`, excluding blanks). A recent scan means the device is active but not managed by Intune: a management-state problem.
- Applicable population for the briefing filters: Windows devices known to Windows Update for Business reports (managed Windows devices enrolled in it, plus these records).
- Eligible for the main briefing under the usual filters (ranking and output, eligibility rule 2). These records have no Intune check-in, so give the Windows Update scan age in place of the check-in call-out; in the executive outputs, chart the scan age in the same bands and title the chart "Last Windows Update scan".
- Next step: find these devices in Microsoft Entra ID and Intune by device ID and check why they are not enrolled or why their Intune record is missing.

**A14b: Managed in Intune but not enrolled in Windows Update for Business reports.**

- Run only when at least one managed Windows device has `Device[Update Compliance Enrolled] = TRUE`. If none does, do not report a device-level gap; classify it with the model foundation, section 7.
- Managed Windows devices (`Device[OS]` Windows 10 or Windows 11) with `Device[Update Compliance Enrolled]` not TRUE.
- Split by `Device[Join Type]` first. Microsoft Entra registered devices (`Azure AD registered`) are not supported by Windows Update for Business reports (Microsoft: "Devices that are Microsoft Entra registered only (workplace joined) aren't supported with Windows Update for Business reports", Prerequisites for Windows Update for Business reports). Report them separately as **not supported**, not as a gap, with their ownership as stated (for example "<n> are Microsoft Entra registered and marked corporate-owned in Intune"). Do not say why a registered device is marked corporate-owned. Devices whose join type is `Unknown` or blank: report the count as join type unknown. Only Microsoft Entra joined and hybrid joined devices are the enrollment gap.
- Give the check-in call-out as usual for each group, and split Cloud PCs from physical devices.
- These devices have no Windows update status in BI for Intune. State that update findings (A7) do not cover them.
- Applicable population: managed Windows devices that are Microsoft Entra joined or hybrid joined.
- Next step: check the Windows Update for Business reports enrollment prerequisites for these devices (for example the data-sharing policy and the diagnostic data configuration).

**A14c: Managed but not reporting PowerStacks custom inventory.**

- Run only when at least one managed device has `Device[Device Details Enrolled] = TRUE`. If none does, classify it with the model foundation, section 7: usually a possible missed opportunity reported in the Coverage line, not a device-level gap.
- Managed Windows and macOS devices with `Device[Device Details Enrolled]` not TRUE: custom inventory data is not present for them. Describe what is missing, not a cause; a missing flag does not confirm that the collector is unassigned or failing. Give the check-in call-out (some may be devices that also stopped checking in) and split by platform and Cloud PC.
- Drill-downs: devices with device details but no app inventory; Windows devices with device details but no driver inventory (only if some managed device reports driver inventory).
- State which data these devices lack (hardware, disk health, monitor manufacture dates used for lifecycle planning, app inventory, drivers), so related findings (for example disk health) are read as not covering them.
- Devices without custom inventory also have no Microsoft 365 Apps or warranty data, because both arrive with custom inventory. Microsoft 365 Apps and warranty data are Windows-only, so mention them only when at least one of these devices is a Windows device (for example "<n> managed devices are not reporting custom inventory (<n> Windows, <n> macOS; <n> checked in within 14 days). For the Windows devices, this includes their Microsoft 365 Apps data."). Do not count them again under Microsoft 365 or warranty.
- Drill-down: managed Windows devices that report custom inventory (`Device[Device Details Enrolled]` = TRUE) but have no row in `Device Microsoft 365`. Only these are a separate Microsoft 365 gap: BI for Intune cannot tell whether Microsoft 365 Apps is getting updates on them. Omit the line when there are none.
- Do not use `Device Warranty Enrolled` as a gap; warranty is handled by A14d.
- Applicable population: managed Windows and macOS devices.
- Next step: check that the inventory script is assigned to these devices and review its recent results in Intune.

**A14d: Warranty coverage.**

This is the only warranty classification rule. The model foundation, the Coverage line, and the Additional findings table all follow it.

- **Base:** physical managed Windows devices (`Device[Cloud PC Enrolled]` not TRUE) whose `Device[Device Manufacturer]` is Dell, HP, Lenovo, or Getac (check every label for these vendors, for example `Dell Inc.`, `HP`, `Hewlett-Packard`, `LENOVO`) **and** that report custom inventory (`Device[Device Details Enrolled]` = TRUE). Devices without custom inventory are counted only in A14c. Other manufacturers are not counted.
- **Classify each base device from its `Device Warranty` rows only** (never from `Device Warranty Enrolled`, which can be TRUE on a device with no warranty row):
  - **No warranty record:** the device has no row in `Device Warranty`.
  - **Warranty record with no dates:** the device has one or more `Device Warranty` rows and `Warranty End Date` is blank on every one of them.
  - **Warranty dates present:** at least one row has a `Warranty End Date`. Not reported.
- **How to report the two groups**, each with a breakdown by manufacturer and the check-in call-out (lead with devices checked in within 14 days, but count every base device):
  - **No warranty record**, when **no** base device has a warranty row: warranty reporting is not enabled, a **missed opportunity** (model foundation, section 7). One Coverage line ("Warranty reporting is not enabled: none of these <n> devices has a warranty record; turning on warranty collection would show factory and warranty dates for lifecycle planning."). No device-level gap.
  - **No warranty record**, when some base devices do have warranty rows: a reporting **opportunity** for these devices. Onboarding them would show when they left the factory and when coverage ends, for lifecycle and budget planning. Not a defect, not a risk.
  - **Warranty record with no dates** (also when this applies to every base device): a **possible warranty lookup problem**. Warranty collection ran for these devices but returned no dates, so the lookup may be failing for that vendor. Do not call it an onboarding opportunity and do not state a cause.
- Build both groups with set operations on device IDs (for example `VALUES('Device Warranty'[Intune Device ID])`, `EXCEPT`, `INTERSECT`). A per-device CALCULATE with TREATAS inside ADDCOLUMNS can misclassify devices.
- Both groups are shown in the Coverage line and in "Additional findings" (reasons "reporting opportunity" and "possible warranty lookup problem"); neither takes a main slot.
- Next step (no warranty record): check that warranty collection is turned on in the custom inventory script and that API credentials are supplied for each of these vendors. Next step (record with no dates): check the inventory script's warranty results and that vendor's API credentials (the product documentation notes that HP credentials expire frequently and must be refreshed). HP's warranty service can also be very slow or fail intermittently, so HP devices may take several collection runs to fill in; when the gap is mostly HP, say so and suggest checking the inventory script's warranty results over several days before concluding the credentials are wrong. Because HP credentials expire so often, PowerStacks suggests recording the HP credential's expiration date as a comment next to the HP credentials in the inventory script, so the team can see when it needs renewing.

**A14e: Intune or co-managed records not marked as managed.**

- Records with `Device[Managed By]` of `Intune` or `Co-Managed` and `Device[Is Managed]` not TRUE. These two sources should always be managed, so this state is always flagged.
- Count the records, with the check-in call-out (lead with how many synced within 14 days) and their compliance values as stated.
- These records stay outside the managed population; say so.
- **Always report it when the count is at least 1**, whatever the briefing filters: in the Coverage line and as a finding. It is eligible for the main briefing (ranking and output, eligibility rule 2) when it meets the filters; otherwise it appears in "Additional findings" with the reason "always flagged (below briefing filters)". These records are outside the managed population but have an Intune check-in, so give the usual check-in call-out.
- Report the values as the source states them. Do not suggest a cause.
- Next step: look up these devices in the Intune admin center and compare their management state with what the data shows.

### A15 Microsoft 365 Apps Update Status

- Managed Windows devices with `Device Microsoft 365[M365 Status] = "Outdated"`, counted as distinct devices, with the check-in call-out.
- Applicable population: managed Windows devices with a status other than `Unknown`. Report `Unknown` separately.
- Devices without Microsoft 365 data are not covered; say so, pointing to the custom inventory line for devices without custom inventory and to the A14c drill-down for the rest.
- Report the status as the data states it. Next step: check the Microsoft 365 Apps update channel and update policy for these devices.

### A16 App Protection

Covers devices managed by app protection policies only (`Managed By = MAM-WE`) and enrolled devices that also report app protection status. Join `App Protection State` to devices through `deviceUser.id` (to `User Devices`, then `Device`).

- **Check first.** Use only state rows with a `deviceUser.id`. Rows without one (they have a blank `Is Protected` and appear once per policy and app) look like each policy's list of targeted apps, not device status; leave them out of device counts (provisional; apply this rule and say in Data Notes that it is unconfirmed). If no row links to a device, follow the app protection rule in the model foundation (never report zero).
- **Apps not protected.** Rows with `Is Protected` = FALSE, by app and platform, with distinct device counts and the split between MAM-WE and enrolled devices. Meaning: the app is in use on the device and could be protected, but no app protection policy covers it (provisional; report as stated and say this meaning is unconfirmed). These rows can carry an all-zeros policy ID (provisional; report it as stated and do not interpret it).
- **Devices using apps that can be protected.** Distinct devices with linked app protection status, by platform, split into MAM-WE and enrolled devices, with how many have at least one unprotected app.
- **Policies not assigned** (`App Protection Policy[Is Assigned]` not TRUE): report as the likely reason when a platform's unprotected rows all lack a policy (for example, a policy assigned to no group explains every unprotected row on its platform). Say it once rather than counting each row as a separate problem (provisional reporting choice; apply it, and do not present it as a product rule).
- **Activity.** Use `App Protection State[Last Sync (Days)]` (app protection sync age) in bands over 14, 30, 60, and 90 days instead of Intune check-in (provisional reporting choice; apply it and name the measure used: app protection sync age).
- Applicable population for the briefing filters: devices with linked app protection status. MAM-WE devices are never added to the Intune-managed population.
- Next step: assign an app protection policy that covers the unprotected apps on that platform, or confirm the apps should be excluded.

## Related Inventory (Not a Finding Area)

`App Inventory` lists installed applications and versions per device. Use it to answer inventory questions (for example which versions of an app are installed).
