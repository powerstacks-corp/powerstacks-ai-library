# BI for Intune Model Foundation

Status: Preview. Written for BI for Intune version 69 and tested with version 70 on 2026-10-23. Use together with the [PowerStacks Analysis Foundation](analysis-foundation.md), which this file extends.

Model compatibility: written against BI for Intune version 69 and tested with version 70 on 2026-10-23. Use version 70 or later; app protection data needs version 70 (see section 3). The model itself does not expose its version (it appears only on the Power BI Apps page), so the AI cannot read it. Confirm that the tables and columns you need exist at runtime before relying on them; skills list theirs as `requiredSchema` in their manifests. A schema check shows that the tables and columns are **structurally available**. It does not prove that their meaning, values, or business rules match the version these instructions were written against.

Rules marked **(provisional)** are interpretations PowerStacks has not yet confirmed. Follow them; when one affects a result, report the result as the data states it and say that the interpretation is unconfirmed.

## 1. What the Model Is

The model contains no vulnerability or threat data. Vulnerability analysis belongs to BI for Defender; do not attempt it with BI for Intune data.

BI for Intune is a semantic model of Microsoft Intune and related directory data: devices, users, groups, policies and their per-device status, apps and their install status, updates, security posture, Endpoint Analytics, Autopilot, and Cloud PCs. Most tables describe current state as of the last refresh. A few tables record events over short recent windows.

## 2. Before You Query

1. Read [core tables, identifiers, and grain](model-core-tables.md) and [measure semantics](model-measure-semantics.md).
2. Discover the tables you need in the connected model and confirm the columns exist.
3. Establish freshness first (see [time and freshness](model-time-and-freshness.md)).
4. Decide the population and identifier before counting anything.

To connect, the AI tool needs the semantic model ID. It is the GUID after `/datasets/` or `/modeling/` in the semantic model's URL in the Power BI service (for example `https://app.powerbi.com/groups/<workspace ID>/datasets/<semantic model ID>` or `.../modeling/<semantic model ID>/modelView`).

The model has no descriptions on tables, columns, or measures. Read measure definitions to learn what they do.

## 3. Devices: Records From Several Sources

The `Device` table combines device records found in several sources. `Device[Managed By]` tells you **where the record was found**, not how the device is managed. The model does not contain every directory device; it contains devices found in these sources.

| `Managed By` | Source |
| --- | --- |
| `Intune` | Intune managed-device record |
| `Co-Managed` | Intune managed-device record that is co-managed with Configuration Manager |
| `Autopilot` | Autopilot registration only |
| `Update Compliance` | Windows Update for Business reports only |
| `Sign-In` | Sign-in data only |
| `Enrollment` | Failed enrollment attempt only |
| `Cloud PC` | Cloud PC record without a matching Intune record. From v70 this is rare (Windows 365 Flex IDs are recovered); a remaining record may be a Cloud PC that no longer exists in the tenant |
| `MAM-WE` | Device managed by app protection policies only, without enrollment (v70 and later). `Is Managed` is FALSE; no Intune check-in; no compliance evaluation. Its own category |
| `Defender` | Windows Server onboarded to Microsoft Defender through Intune endpoint security policies, the only Intune feature supported on Windows Server. `Is Managed` is TRUE. Its own category |

Other `Managed By` values can appear (for example `ConfigMgr`). Their meaning is not confirmed (provisional; report them as stated and say their meaning is unconfirmed): keep them outside the managed population and report their record count as stated in a data note.

- **Managed devices (default population):** `Is Managed = TRUE` and `Managed By` in `Intune` or `Co-Managed`, regardless of check-in age. `Co-Managed` devices are co-managed by Configuration Manager and Intune and count as managed.
- **Always present the full managed population, and call out check-in age** rather than excluding older devices: how many last checked in more than 14, more than 30, more than 60, and more than 90 days ago. Apply the same call-out to every finding's affected devices.
- Count managed devices with a distinct count of `Device[Intune Device ID]` within that filter.
- Devices with an older check-in stay in the population, but their last known state may be out of date. The check-in call-out makes that visible.
- **Records from other sources** (`Autopilot`, `Update Compliance`, `Sign-In`, `Enrollment`, `Cloud PC`) have no Intune management state. Use them only for questions about those sources, such as Autopilot registrations or failed enrollments. Some `Enrollment` records carry an `Intune Device ID`; they are not managed devices.
- Records with `Managed By` of `Intune` or `Co-Managed` should always have `Is Managed = TRUE`. When `Is Managed` is not TRUE on such a record, keep it out of the managed population, but **always flag it as a finding**: it is an inconsistent management state in the source. Report the values as stated; do not suggest a cause.
- `[Device Count]` counts every record from every source. Do not use it as the managed-device denominator.
- **Cloud PCs** (Windows 365) are Windows virtual machines hosted by Microsoft. Mention them only when the scope includes Windows. Within the managed population they have `Device[Cloud PC Enrolled] = TRUE`. It is not normal to encrypt them, so a `Not Encrypted` status on a Cloud PC is expected and is never an encryption gap. Report Cloud PCs separately from physical devices wherever their results differ.
- **OS labels are not normalized.** The same platform can appear under several `Device[OS]` values (for example `MacOS` and `Osx`, `iOS/iPadOS` and `iPhone`). The alternative labels usually come from non-Intune sources. Apply the managed-device filter before scoping by platform, and check `VALUES(Device[OS])`.
- **Categories outside the Intune-managed population.** Two record sources are reported as their own categories, never mixed into the managed population, compliance numbers, check-in bands, the stale-device list, or the check for Intune records not marked as managed:
  - **Devices managed by app protection policies only (`Managed By = MAM-WE`).** They do not evaluate compliance and have no Intune check-in. Report their count in the header and analyze them in the app protection area (A16), using app protection sync age instead of check-in.
  - **Windows Servers managed through Defender security settings (`Managed By = Defender`).** Report only their count and this description; nothing else.
- **App protection data can be incomplete.** In version 69 a product issue (fixed in version 70) left every app protection status row without a device or user link, so devices managed by app protection policies only did not appear in the model. Before reporting on app protection or MAM-WE, check that `App Protection State` rows have a `deviceUser.id` and an `Is Protected` value. If they do not, say that app protection status is not available in this data and that app-protected devices without enrollment are not included in the device counts. Never report zero app-protected devices from this state.

### Data Sources

BI for Intune collects data from Microsoft Intune, Windows Autopilot, Windows Update for Business reports, sign-in data, and failed enrollment attempts, and reports their values as the sources provide them. Data is typically refreshed a few times a day.

#### Transformations (Provisional)

PowerStacks changes a small number of values on the way in. These are the only exceptions to reporting source values as stated. **The list below is provisional:** it is drawn from the product release notes, it is not known to be complete, and PowerStacks has not yet confirmed the exact mappings and rules.

| Category | Example | Evidence |
| --- | --- | --- |
| Derived value | `Device[OS]` is calculated as Windows 10 or Windows 11 from the OS build for known workstation operating systems; other Windows devices show "Windows", the value Microsoft returns. | Release notes v57, v58 |
| Relabeled value | Windows devices protected by app protection without enrollment show a device type of "Windows" instead of the raw value "1". | Release notes v62 |
| Relabeled value | The Conditional Access control "Require Domain-Joined Device" is shown as "Require Hybrid-Joined Device". | Release notes v57 |
| Relabeled value | The edition value `ServerRdsh` is shown as "Enterprise Multi-Session". | PowerStacks; not found in product docs |
| Configured assessment | Disk health status is assessed against configurable thresholds (defaults: maximum wear 90, maximum read errors 100, maximum write errors 100). | Semantic model parameters page |
| Configured assessment | App install status is chosen from the primary user, enrolled user, and last logon user contexts, because Intune can report more than one status per app and device. | Release notes v44 |
| Configured assessment | Several status objects report device status only, not device plus user status. | Release notes v59 |

When a finding depends on one of these values, say that the value is calculated, relabeled, or assessed by BI for Intune rather than copied from the source.

#### Caveats (Not Exceptions)

These limit **what data is present**. They do not change any value, so they are not exceptions to reporting source values as stated. Mention them when they affect how a figure should be read.

Collection defaults (per-tenant settings; the customer may have changed them):

- Sign-in data covers **failed sign-ins only, for the last day**. Do not treat a missing sign-in as "the user has not signed in".
- Group membership includes **dynamic groups only**.

Permission and reporting limitations:

- Some data needs extra permissions or add-ons. Without them the related data is empty or defaulted, which is expected. For example, without the recovery-key read permission `Device[OS Recovery Key Stored]` is FALSE on every device even where a key exists; if it is FALSE everywhere, report it as a possible permission gap, not as missing keys (release notes v69).
- When the remediation-assignment setting is turned off (a workaround for a Microsoft service error), remediation assignment details are empty (release notes v69).
- Windows Update for Business reports can take from 72 hours to two weeks to include a newly configured device.

## 4. Identifiers

| Identifier | Meaning | Use |
| --- | --- | --- |
| `Intune Device ID` | Intune managed-device identifier | Default device key for management analysis. Blank for most records from non-Intune sources. |
| `device.id` | Key of the `Device` table (one per record, any source) | Joins `Device` to `User Devices` and some update and Autopilot tables. Usually equals `Azure AD Device ID`. |
| `Azure AD Device ID` | Directory device identifier | Directory-level questions. Not interchangeable with `Intune Device ID`. |
| `User ID` | Directory user identifier | User questions; key of `User`. |
| `DeviceIDUPN` | Combined device-and-user key | Joins `Application State` to `User Devices`. Often blank. |
| `deviceUser.id`, `members.id` | Bridge keys | Used by sign-in, app protection, and group relationships through `User Devices`. |

Do not join on serial number or device name. Both repeat across rows.

## 5. Grain and Double Counting

- `User Devices` is the hub table. It has one row per device-user association, so a device with several users appears several times.
- Most relationships filter in both directions and many are many-to-many. Combining a device-level table with a user-level table through `User Devices` can multiply rows.
- Status tables (`Compliance Policy State`, `Configuration State`, `Application State`, `Script State`, `Proactive Remediation State`, `Windows Update Ring State`, `Windows Feature Update State`) hold one row per device (or device-user) per policy, app, or script. A device with several policies has several rows by design; that is not duplication.
- **Use the device table for a device's overall state** where it exists: `Device[Compliance]` is the device's overall compliance state. Use `Compliance Policy State` only to explain which policy a device is non-compliant on, never to count compliant or non-compliant devices.
- To count affected devices, use `DISTINCTCOUNT` of the device identifier on the status table, not `COUNTROWS`.
- Some status tables contain repeated device-and-item pairs. Do not assume one row per pair.

## 6. Existing Measures

Prefer existing measures, but read [measure semantics](model-measure-semantics.md) first. Key points:

- **Measures carry no population filters by design.** PowerStacks applies filters such as the managed-device definition in the reports, not in DAX. When you query the model directly, no report filters apply, so you must apply the population filter yourself (see section 3).
- Device compliance measures count distinct `Intune Device ID` across every record that has one, including records that are not managed and devices that have not checked in for more than 30 days.
- Status-table measures (for example `[App Failed]`, `[Configuration Error]`, `[Policy Non Compliant]`, `[Remediation Failed]`) count **status rows**, not devices, and only rows that match a `User Devices` record. Report them as "status records" or convert to a device count.
- Several percentage measures divide by all `Device` rows, which include records from every source. Recalculate against managed devices when the question is about managed devices.
- Some measures filter on status values that may not exist in the connected model and return BLANK. A BLANK is not evidence of zero problems.

## 7. Missing Data: Problems Versus Options Not Enabled

BI for Intune lets each customer choose what data to bring in. Semantic model parameters turn sources on or off (for example `AzureAD LogAnalytics Enable`, default off, which is needed for both Windows Update for Business reports and PowerStacks custom inventory; and switches for application state, script state, compliance setting state, driver updates, and remediation assignments). The custom inventory script has its own switches (for example warranty collection, off by default). These settings are **not visible in the model**, so infer the scenario from which data is present and say what you inferred.

| What the data shows | Classification | How to report it |
| --- | --- | --- |
| Part of a source loaded while other data from the same source is empty for every device (for example the custom inventory driver flag is set but device details are empty) | **Problem** (partial load) | Lead with the environment alert: "Some data did not load in the latest refresh. Please run the data refresh again; if the problem persists, contact PowerStacks support. Also make sure BI for Intune is on the latest version." Dependent areas are not assessed. |
| Everything that comes from Log Analytics is empty (both Windows Update for Business reports and custom inventory) | **Problem** | Coverage line: neither source is present; run the data refresh again, and if the problem persists contact PowerStacks support; make sure BI for Intune is on the latest version. Dependent areas are not assessed. |
| One whole source is not present while the other Log Analytics source is (for example custom inventory present, Windows Update for Business reports absent) | **Possible missed opportunity** (may not be enabled) | Coverage line: the source is not present, what it would add, and "contact PowerStacks support if you expected this data". Dependent areas are not assessed. No device-level gap. |
| A source is present but one of its optional parts is empty for every device (for example custom inventory without Microsoft 365 data, or no warranty row for any eligible device) | **Missed opportunity** | Coverage line: what enabling that part would add. For warranty, "empty" means no `Device Warranty` row at all; warranty rows that exist but have no dates are a possible lookup problem, not a missed opportunity (section 11). |
| A single table is empty while related tables loaded (for example per-device, per-policy compliance results empty while the policies and setting results loaded) | **Possibly a data-collection setting** | Data note: the data is not present in this refresh and this can be a data-collection setting; contact PowerStacks support if you expected it. The dependent part is not assessed. No environment alert. |
| Some devices lack data that most devices have | **Device-level coverage gap** | Report as a finding (for example A14b, A14c). |

What each source adds, for opportunity wording: Windows Update for Business reports adds Windows security update status, feature update end-of-service dates, and update scans. PowerStacks custom inventory adds hardware details, disk health, app and driver inventory, monitor details, and (when enabled) Microsoft 365 Apps update status and warranty dates.

Never describe missing data as a device, policy, or collector problem on the devices, and never report every device as a gap because a source or table is absent.

### Check the Data Settings First

**Purpose:** reading the settings is only for telling whether a feature is disabled or failing. Settings that do not switch a feature on or off (for example the disk health thresholds) are not read, even where they are safe.

The model's data settings (semantic model parameters) can be read with a metadata query. Read them before classifying missing data, so a setting the customer turned off is not mistaken for a failed load.

**Read only the settings PowerStacks has approved:** `AzureAD Sign-Ins Failure Only`, `AzureAD Sign-Ins Day(s)`, `AzureAD LogAnalytics Enable`, `AzureAD LogAnalytics Day(s)`, `AzureAD Group Members Enable`, `AzureAD Group Dynamic Members Only`, `AzureAD Group Members Filter Starts With`, `AzureAD Group Members Nested Crawler Enable`, `AzureAD Compliance Policy Setting State Enable`, `AzureAD Application State Enable`, `AzureAD Script State Enable`, `AzureAD Driver Updates Enable`, `AzureAD Proactive Remediation Assignment Enable`, `AzureAD Timeline Event Day(s)`, `AzureAD Compliance Policy State Enable`, `AzureAD Application Assignment Enable`. Never read any other parameter, and never read `ApiKey`, `AzureAD TenantID`, `AzureAD ClientID`, or `AzureAD ClientSecret`. The query selects the approved names before any value is read and also excludes the four by name. Do not change it to read other parameters.

```dax
EVALUATE
VAR Allowed =
    FILTER (
        SELECTCOLUMNS ( INFO.EXPRESSIONS (), "Name", [Name], "Expression", [Expression] ),
        [Name] IN {
            "AzureAD Sign-Ins Failure Only",
            "AzureAD Sign-Ins Day(s)",
            "AzureAD LogAnalytics Enable",
            "AzureAD LogAnalytics Day(s)",
            "AzureAD Group Members Enable",
            "AzureAD Group Dynamic Members Only",
            "AzureAD Group Members Filter Starts With",
            "AzureAD Group Members Nested Crawler Enable",
            "AzureAD Compliance Policy Setting State Enable",
            "AzureAD Application State Enable",
            "AzureAD Script State Enable",
            "AzureAD Driver Updates Enable",
            "AzureAD Proactive Remediation Assignment Enable",
            "AzureAD Timeline Event Day(s)",
            "AzureAD Compliance Policy State Enable",
            "AzureAD Application Assignment Enable"
        }
            && NOT ( [Name] IN { "ApiKey", "AzureAD TenantID", "AzureAD ClientID", "AzureAD ClientSecret" } )
    )
RETURN
    SELECTCOLUMNS ( Allowed, "Setting", [Name],
        "Value", LEFT ( [Expression], SEARCH ( " meta", [Expression], 1, LEN ( [Expression] ) + 1 ) - 1 ) )
```

How to use the settings:

| Setting | When off (or limited) |
| --- | --- |
| `AzureAD LogAnalytics Enable` | Windows Update for Business reports and custom inventory are not enabled: missed opportunity, not a problem. When on and every Log Analytics source is empty: problem. |
| `AzureAD Compliance Policy State Enable` | Per-device, per-policy compliance results are turned off: the compliance cause breakdown is not available (say so); device compliance counts still come from each device's overall state. |
| `AzureAD Compliance Policy Setting State Enable` | Setting-level compliance results are turned off. |
| `AzureAD Application State Enable` | App install status is turned off: app deployment area not assessed. |
| `AzureAD Application Assignment Enable` | App assignment details are turned off: assignment intent (required, available, uninstall) cannot be checked because of this setting. Turning it on may slow the data sync or cause sync failures. |
| `AzureAD Script State Enable` | Platform script results are turned off: script area not assessed. |
| `AzureAD Proactive Remediation Assignment Enable` | Remediation assignment details are turned off. Turning it on may slow the data sync or cause sync failures. |
| `AzureAD Driver Updates Enable` | Windows driver update data is turned off. |
| `AzureAD Group Members Enable`, `AzureAD Group Dynamic Members Only` | Group membership off, or dynamic groups only. |
| `AzureAD Sign-Ins Failure Only`, `AzureAD Sign-Ins Day(s)` | Sign-in data scope. |
| `AzureAD Group Members Filter Starts With`, `AzureAD Group Members Nested Crawler Enable` | Which groups' members are loaded, and whether nested groups are followed. |
| `AzureAD LogAnalytics Day(s)`, `AzureAD Timeline Event Day(s)` | Look-back windows for Log Analytics and timeline data; state them when they limit a figure. |

- A setting that is off explains its missing data: report it in plain English ("app assignment details are turned off in your BI for Intune data settings"), as an option the customer can turn on, never as a problem or a device gap.
- A setting that is on while its data is empty points to a problem: classify it with the table above (partial load or all Log Analytics data missing: re-run the refresh, then contact PowerStacks support if it persists; latest version).
- If the settings cannot be read (for example the user lacks permission for metadata queries), say so once and fall back to the classification table above.
- Settings inside the custom inventory script (for example warranty collection) are not in the model, and settings not on the approved list are not read; for both, infer from the data.

## 8. Freshness and Activity

- Optional refresh history check: see [time and freshness](model-time-and-freshness.md#refresh-history-check-optional). It can flag an unusually long refresh; it never proves data is missing.
- State the model refresh time first. See [time and freshness](model-time-and-freshness.md).
- `Device[Last Check-In]` is the device's last sync time with Intune. It is not the refresh time.
- Columns ending in `(Days)` were calculated at refresh. Add the time elapsed since refresh if the gap matters.
- **TRUE/FALSE fields can be blank instead of FALSE** (a known Power BI behavior that cannot be changed in the model). Always test a flag as TRUE or not TRUE; never test for FALSE.
- A BLANK `(Days)` value compares as 0 in DAX. Always exclude blanks explicitly (`NOT ISBLANK(...)`) before filtering on a day count, or records from non-Intune sources will look recently active.

### Dates and Deadlines

- Report a date exactly as the source gives it (for example the end-of-service date from Windows Update for Business reports, or a connector expiration date from Intune). Name the source.
- Calculate days remaining from the **date of the answer in the user's local time zone** (the time zone the user states or their computer reports; UTC only when neither is known, and then say so), as whole calendar days to the source date. State the time zone. Collection and query times stay in UTC. Do not use a stored `(Days)` column for this: it was calculated at refresh and is out of date by the time of the answer.
- Do not replace or "correct" a source date with a date from a lifecycle website or any other external reference.
- End-of-service dates are passed through unchanged from Windows Update for Business reports. Microsoft gives different editions of the same feature update different servicing periods (Home and Pro editions are serviced for a shorter period than Enterprise and Education), so group end-of-service dates by release **and** edition. A difference between editions is not by itself an inconsistency.
- If the source looks inconsistent (for example devices on the same release and edition reporting different end-of-service dates), report the dates as stated, give the counts, and flag the difference for investigation. Do not decide which date is right, and do not explain it with a cause the data does not show.
- A date that has already passed is not an upcoming deadline. Report it as the current state the source gives (for example `End Of Service`).

## 9. Check-In Age

Report the full managed population and show check-in age with it:

- For the population and for every finding, give the total and how many of those devices last checked in more than 14, more than 30, more than 60, and more than 90 days ago.
- **Device details for devices last checked in more than 14 days ago.** List them so the team can act on them, with the identifying details in section 14 (device name, serial number, platform, ownership, manufacturer and model, the device's user (primary user name and UPN; if there is no primary user, the enrolled user, then the last logon user, labeled as such; "no user associated" if none), the user's department, and the last logon user and date when different from the primary user), plus last check-in date and days since check-in, each clearly flagged as over 14, over 30, over 60, or over 90 days (the highest band that applies). Show values exactly as stored.
- Make clear that a device with an old check-in shows its last known state, which may be out of date.
- The customer chooses any exclusion. Do not exclude devices by check-in age unless the user asks; when they do, apply exactly the window or filter they choose (any number of days, platform, or group) and say so.

**Standing rule: age-mix flag.** Whenever more than half of the devices behind a figure or finding last checked in more than 14 days ago:

1. Say so plainly next to the figure, for example: "<n>% of these devices have not checked in for more than 14 days, so their status may be out of date."
2. Lower the confidence of that finding by one level.
3. Keep the full count. Do not remove the older devices yourself.

The flag does not apply to a finding that is about check-in age itself (every device in it is old by definition).

At the end of any answer that reports device counts, offer to narrow the analysis, for example: "Ask me to exclude devices that have not checked in for more than any number of days you choose (for example 14, 30, 60, or 90)." The user decides what to include.

Intune removes devices that have not checked in for a set number of days (its device cleanup rule). The default is 90 days, but each customer can change it, so the limit varies by tenant. Devices silent for longer than the tenant's limit are no longer in Intune and therefore not in the model. Do not assume a 90-day limit: report the oldest check-in age actually present (`MAX(Device[Last Check-In (Days)])` for Intune records) and say that devices silent for longer may already have been removed.

## 10. Fields That Need Care

- `Windows Protection` describes **Microsoft Defender Antivirus only**. Many organizations run a third-party antivirus, in which case Defender real-time protection, tamper protection, and signature fields are expected to show Defender as off or out of date. The model has no data about third-party antivirus products. Do not report Defender fields as a protection gap unless the user confirms Defender is their antivirus.
- `Windows Protection[Protection Status]` blanks are unknown, not healthy (provisional; report blanks as unknown and say this reading is unconfirmed).
- `Device[OS Security Update Status]`, `[OS Quality Update Status]`, `[OS Feature Update Status]`, `[OS Feature Update EOS Date]`, and related OS update columns come from **Windows Update for Business reports** (its per-device client record). Microsoft documents them as follows:
  - Security update status refers to the monthly security update released on the second Tuesday, for the device's installed feature update. `Latest`: the latest security update is installed. `Not Latest`: the latest security update is not installed. `Multiple Security Updates Missing`: two or more security updates are missing.
  - There is no grace period: a device becomes `Not Latest` when a new security update is released and stays so until it installs it. State which monthly release was the latest at the data refresh time.
  - Quality update status refers to the optional preview update released on the fourth Tuesday.
  - The EOS date is the end-of-service date Windows Update for Business reports gives for the installed feature update. Report it as stated, attributed to that source.
  - A blank value means the device has no Windows Update for Business reports record (for example an unsupported edition, not sending data, or not active in the last 28 days). Treat blank as unknown, not as up to date.
  - The source refreshes about once a day, so these values can lag the device by a day or more on top of the model refresh.
- **Windows Update for Business reports enrollment.** `Device[Update Compliance Enrolled] = TRUE` means the device is enrolled in Windows Update for Business reports, the service that populates the Windows update status data in BI for Intune. As with every flag, test for TRUE or not TRUE. A managed Windows device that is checking in to Intune but is not enrolled has no update status; report it as a coverage problem, not as up to date or out of date. Devices can take from 72 hours to two weeks to appear in Windows Update for Business reports after they are configured, so recently enrolled devices may show as not enrolled for a short time.
- **Windows Update Distribution report.** `Device[WU Distribution Enrolled] = TRUE` means the device appears in the Windows Update Distribution report, which supplies `Device[OS Release ID]`. The release and the end-of-service date therefore come from two different sources, each passed through as provided, so a device's release label and its end-of-service date can disagree; report both as stated. A device can have a release from this report and still have no Windows Update for Business reports status.
- **Devices found only in Windows Update for Business reports.** Records with `Managed By = Update Compliance` are Windows devices reporting to Windows Update for Business reports that have no Intune record. When their `Device[Last WU Scan (Days)]` is recent, the device is active but not managed by Intune, which indicates a problem with its management state.
- Encryption, firewall, Endpoint Analytics, and Windows 11 readiness data exist only for devices that report them. Devices with no row are unknown.
- `'Application Error Code'` does not contain every code found in `Application State[App Error Code]`. Group by the raw column.
- `Compliance Policy Setting State` has no device key. Join it through `deviceCompliancePolicy.id`; its counts are setting-status records.
- A policy or profile in `Error` does not prove a control is missing. Check the control's own state (for example `Device Encryption`) where it exists.
- `Application Assignment` can be empty, in which case assignment intent cannot be determined. Check `AzureAD Application Assignment Enable` first: if it is off, say the setting is turned off.

## 11. PowerStacks Custom Inventory

BI for Intune can include data from the PowerStacks custom inventory collector, an optional script deployed through Intune (on Windows as a daily Intune remediation; on macOS as an Intune shell script). It uploads a full snapshot each run. Customers choose whether to deploy it and which parts to enable, so some tenants have none of this data.

| Data | Platforms | Flag on `Device` | Notes |
| --- | --- | --- | --- |
| Device details (hardware, battery, boot time, disks, monitors, chassis) | Windows, macOS | `Device Details Enrolled` | macOS sends a smaller set (no monitors, chassis, or OS install date). Monitor data includes the manufacture year and week (`Device Monitor`), which helps estimate hardware age for lifecycle and budget planning. |
| App inventory | Windows, macOS | `App Inventory Enrolled` | Machine-wide apps plus the apps of the one user signed in when the script ran. |
| Driver inventory | Windows | `Driver Inventory Enrolled` | Excludes Microsoft drivers. |
| Microsoft 365 apps | Windows | `Device Microsoft 365 Enrolled` | How BI for Intune determines whether Microsoft 365 Apps (Office) is getting updates. Status in `Device Microsoft 365[M365 Status]` (for example `Up-To-Date`, `Outdated`, `Unknown`). |
| Warranty | Windows | `Device Warranty Enrolled` | Optional and off by default; supported only for Dell, HP, Lenovo, and Getac, and only for vendors whose API credentials the customer supplies. Warranty dates (`Device Warranty`) show when a device left the factory and when coverage ends, which is used for lifecycle and budget planning. |

Rules:

- `Device Details Enrolled` or `App Inventory Enrolled` not TRUE on a managed Windows or macOS device means that custom inventory data is **not present** for that device. Its hardware, disk, app inventory, and related data are unknown, not healthy. Report what is observed (the flag is not TRUE and the data is missing) with the check-in call-out. Do not state the cause: a missing flag does not by itself show that the collector is unassigned, failing, or turned off.
- Do not mention custom inventory flags for platforms the collector does not support (iOS/iPadOS, Android), or the Windows-only flags in a macOS scope.
- If no managed device in the tenant has a given flag TRUE, say so as an observation in Data Notes (for example "no managed device reports driver inventory"). Possible explanations include the collector or that part of it not being deployed, being turned off, or not reporting. The data does not show which, so do not report it as a confirmed deployment or reporting failure, and do not rank it as a device-level gap.
- **How the flags are set:** a flag is TRUE when BI for Intune found data for that inventory type and device in the corresponding custom inventory table. Microsoft 365 and warranty fields arrive in the same device inventory record as device details, so those flags can be TRUE whenever device details exist. To know whether warranty dates or Microsoft 365 status actually exist, check `Device Warranty` and `Device Microsoft 365`, not the flag.
- `Device Microsoft 365 Enrolled` not TRUE on a managed Windows device is a coverage gap: BI for Intune cannot tell whether Microsoft 365 Apps on that device is getting updates. Count it as its own gap only for devices that report custom inventory; devices without custom inventory are already counted there.
- **Warranty classification (one rule).** Base: physical managed Windows devices from Dell, HP, Lenovo, or Getac that report custom inventory; devices without custom inventory are counted only in the custom inventory gap, and other manufacturers are not counted. Decide from `Device Warranty` rows, never from `Device Warranty Enrolled`: a base device with **no row** has no warranty record; a base device whose rows **all** have a blank `Warranty End Date` has a record with no dates. No warranty record is a reporting **opportunity** (or, when no base device has any row, warranty reporting is not enabled: a missed opportunity per section 7), never a device problem. A record with no dates means the lookup ran without result: report it as a possible warranty lookup problem, not an opportunity, even when it applies to every base device. The skill's analysis area for warranty coverage gives the reporting wording.

## 12. Historical Coverage

Most tables are current state only. Do not describe trends for compliance, configuration, app, or update status. Event tables (`Device Timeline Event`, `User Sign-Ins`, `Device Enrollment Failure`, update compliance alerts) cover limited windows; check their date range before using them for any time comparison.

## 13. Inventory

`App Inventory` lists installed applications and versions per device (Windows and macOS devices that report it). It answers inventory questions.

## 14. Personal and Device Data

The model contains user names, email addresses, device names, serial numbers, phone numbers, network addresses, and recovery-key or local-credential metadata. **Never mask data.** The people using these answers already have access to the underlying data, so never mask, redact, truncate, or alter a value; show it exactly as stored (for example a device name that contains a person's name). Briefings still summarize with counts for readability and list individual devices or users where a rule requires it or the user asks.

**Help the customer identify devices.** Device names are often serial numbers and mean little on their own. Whenever you list devices, include: device name, serial number, platform, ownership, manufacturer and model, the device's user (primary user name and UPN; if there is no primary user, the enrolled user, then the last logon user, labeled as such; "no user associated" if none), the user's department, and the last logon user and date when different from the primary user. Users come from `User Devices` (`Primary User`, `Enrolled User`, `Last Logon User`, `UPN`, `Last Logon`) and `User` (`Full Name`, `Department`); serial number from `Device[Serial Number]`. If a device has more than one user of the same kind, list them all. Build device lists with the device list pattern in the skill's analysis areas (one row per device, users looked up per device), never by combining `User Devices` and `User` rows directly, which repeats devices. The model holds recovery-key and local-credential metadata, not the secrets themselves. Discover columns with metadata (`INFO.VIEW.COLUMNS()` or a schema tool), not by sampling rows, so identifiers are not pulled in unnecessarily.
