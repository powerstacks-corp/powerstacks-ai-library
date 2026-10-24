# Analysis Areas

Status: Preview 0.1.0. Query patterns written for and tested with the BI for Defender release 15 schema on 2026-10-23. Confirm names at runtime (skill Step 0).

This Preview covers five areas. Each area produces at most one main finding; its sub-results are drill-downs.

| Area | Name | Applicable population (for share) | Main finding |
| --- | --- | --- | --- |
| S1 | Data collection and assessment coverage | Default population | Onboarded devices with no assessment data |
| S2 | Critical and exploitable vulnerabilities | Assessed devices | Devices with at least one active critical or exploitable vulnerability |
| S3 | Devices not reporting | Default population | Devices last seen more than 7 days before data collection |
| S4 | Missing security updates | Assessed devices | Devices missing at least one Microsoft security update identified by a KB number |
| S5 | End-of-support software | Assessed devices | Devices with active software at or past its end-of-support date |

- **Default population:** onboarded devices that are not excluded, counted by `Defender Device ID` (model foundation, section 3).
- **Assessed devices:** default-population devices with at least one software inventory row. Devices without one are not assessed for S2, S4, and S5; S1 counts them.

## Shared Pattern: Device Set and Constants

Define the device set once and reuse it. Apply it to each fact table's own device column (through `Software Devices` for vulnerabilities), so device IDs without a device record are excluded and counts do not depend on bidirectional relationship paths.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Pop =
        CALCULATETABLE (
            VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded",
            NOT ( Device[Is Excluded] = TRUE () )
        )
    VAR WithSoftware =
        DISTINCT ( SELECTCOLUMNS ( 'Software Devices', "Id", 'Software Devices'[Defender Device ID] ) )
    VAR Assessed = INTERSECT ( Pop, WithSoftware )
    VAR ActiveVuln =
        FILTER (
            ADDCOLUMNS (
                FILTER ( 'Software Vulnerabilities', 'Software Vulnerabilities'[Is Active] = TRUE () ),
                "Dev", RELATED ( 'Software Devices'[Defender Device ID] ),
                "Sev", RELATED ( Vulnerability[Severity Level] ),
                "Exp", RELATED ( Vulnerability[Exploitability Level] )
            ),
            [Dev] IN Pop
        )
EVALUATE
ROW (
    "Collected at", CollectedAt,
    "Default population", COUNTROWS ( Pop ),
    "Assessed devices", COUNTROWS ( Assessed ),
    "Devices with an active vulnerability", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( ActiveVuln, "d", [Dev] ) ) )
)
```

Add `Scope` filters (for example `Device[OS] = "Windows 11"`) inside the `Pop` definition.

DAX notes:

- Quote table names in single quotes.
- Test flags as TRUE or not TRUE; flags can be blank instead of FALSE.
- Count distinct devices in a table variable with `COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( <table>, "d", [Dev] ) ) )`.
- Never count from the `Vulnerability` catalog directly, and never rely on an unfiltered path through `User Devices`.
- Do not read semantic model parameters, and never run `INFO.EXPRESSIONS()` or `INFO.PARTITIONS()`.
- `COUNTROWS` of an empty table returns blank; report it as 0.
- `TOPN` keeps ties, so a top 10 can return more rows; show the top rows and say how many share the last value.

## Last-Seen Call-Out (Every Finding)

For the population and for each finding's affected device set, count devices by days from `Device[Last Seen]` to the data collection time. Report "more than 7, 14, 30, 60, and 90 days" call-outs in the briefing; the executive outputs use the bands 0 to 14, 15 to 30, 31 to 60, 61 to 90, and over 90.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Pop =
        CALCULATETABLE ( VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded", NOT ( Device[Is Excluded] = TRUE () ) )
    VAR Ages =
        ADDCOLUMNS ( Pop, "Age",
            DATEDIFF ( LOOKUPVALUE ( Device[Last Seen], Device[Defender Device ID], [Defender Device ID] ), CollectedAt, DAY ) )
EVALUATE
ROW (
    "Devices", COUNTROWS ( Ages ),
    "Over 7", COUNTROWS ( FILTER ( Ages, [Age] > 7 ) ),
    "Over 14", COUNTROWS ( FILTER ( Ages, [Age] > 14 ) ),
    "Over 30", COUNTROWS ( FILTER ( Ages, [Age] > 30 ) ),
    "Over 60", COUNTROWS ( FILTER ( Ages, [Age] > 60 ) ),
    "Over 90", COUNTROWS ( FILTER ( Ages, [Age] > 90 ) )
)
```

Replace `Pop` with a finding's device set to get that finding's call-out.

## Affected Devices for Any Finding

Every main finding lists its affected devices (up to `DeviceDetailLimit`, oldest last-seen first). Build the finding's device set as a one-column table of `Defender Device ID` values (for example `DISTINCT ( SELECTCOLUMNS ( CritOrExpl, "d", [Dev] ) )` from S2), then:

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Affected = { "<device set from the finding>" } -- illustrative: replace with the finding's device set
    VAR Links =
        DISTINCT ( SELECTCOLUMNS (
            FILTER ( 'User Devices', NOT ISBLANK ( 'User Devices'[User ID] ) && 'User Devices'[Logon User] = TRUE () ),
            "Key", 'User Devices'[device.id], "Uid", 'User Devices'[User ID]
        ) )
EVALUATE
SELECTCOLUMNS (
    ADDCOLUMNS (
        FILTER ( Device, Device[Defender Device ID] IN Affected ),
        "Users",
            VAR k = Device[device.id]
            VAR u =
                CONCATENATEX ( FILTER ( Links, [Key] = k ),
                    LOOKUPVALUE ( 'User'[Full Name], 'User'[User ID], [Uid] ) & " ("
                        & LOOKUPVALUE ( 'User'[User Name], 'User'[User ID], [Uid] ) & ")", "; " )
            RETURN IF ( ISBLANK ( u ), "No user associated", u ),
        "Departments", VAR k = Device[device.id] RETURN
            CONCATENATEX ( FILTER ( Links, [Key] = k ), LOOKUPVALUE ( 'User'[Department], 'User'[User ID], [Uid] ), "; " )
    ),
    "Device", Device[Device Name],
    "OS", Device[OS],
    "Release", Device[OS Release ID],
    "Last seen", Device[Last Seen],
    "Days before collection", DATEDIFF ( Device[Last Seen], CollectedAt, DAY ),
    "Users", [Users],
    "Departments", [Departments]
)
ORDER BY [Days before collection] DESC, [Device]
```

- Tested with the BI for Defender release 15 schema on 2026-10-23: one row per device for the whole default population, with users looked up per device (distinct device and user pairs), so devices are not repeated or paired with every user. Do not combine `User Devices` and `User` rows directly instead.
- The model has no serial number, so device lists have no serial number column.
- Show values as stored. A device with no user recorded shows "No user associated"; a blank department shows as blank.
- These rows are the only device rows the executive outputs use.

## S1: Data Collection and Assessment Coverage

**What it checks:** data age, the license record, which default-population devices have no assessment data, and assessment data that has no device record.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Pop =
        CALCULATETABLE ( VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded", NOT ( Device[Is Excluded] = TRUE () ) )
    VAR Known = CALCULATETABLE ( VALUES ( Device[Defender Device ID] ), NOT ISBLANK ( Device[Defender Device ID] ) )
    VAR WithSoftware =
        DISTINCT ( SELECTCOLUMNS ( 'Software Devices', "Id", 'Software Devices'[Defender Device ID] ) )
    VAR NotAssessed = EXCEPT ( Pop, WithSoftware )
    VAR Unmatched = EXCEPT ( WithSoftware, Known )
EVALUATE
ROW (
    "Collected at", CollectedAt,
    "License status", MAX ( 'Authorization'[Status] ),
    "License type", MAX ( 'Authorization'[License Type] ),
    "License end date", MAX ( 'Authorization'[End Date] ),
    "Latest device last seen", MAX ( Device[Last Seen] ),
    "Assessment records from", MIN ( 'Software Vulnerabilities'[Last Seen] ),
    "Assessment records to", MAX ( 'Software Vulnerabilities'[Last Seen] ),
    "Default population", COUNTROWS ( Pop ),
    "Discovered, not onboarded", CALCULATE ( COUNTROWS ( Device ), Device[Onboarding Status] = "Can Be Onboarded" ),
    "Excluded", CALCULATE ( COUNTROWS ( Device ), Device[Is Excluded] = TRUE () ),
    "Not assessed", COUNTROWS ( NotAssessed ),
    "Device IDs with data but no device record", COUNTROWS ( Unmatched )
)
```

- **Data age** is the briefing date minus the collection time, in whole days. When it is more than `StaleDataDays`, the briefing leads with a data age alert (see ranking and output).
- **Not assessed devices:** break them down by last-seen age (a device not seen for a month or more usually has no current assessment) and by first-seen date (a device first seen within a day or two of collection may not have been assessed yet; this is an inference, so label it).
- **Device IDs without a device record:** count them and the share of active vulnerability records they hold. They are excluded from every count. Report them in Data Notes, never as a device finding.
- **Discovered devices** (not onboarded) and excluded devices go on the header line, not in this finding.

## S2: Critical and Exploitable Vulnerabilities

**What it checks:** assessed devices with at least one active vulnerability that Defender rates `1 - Critical` or `Exploitable`.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Pop =
        CALCULATETABLE ( VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded", NOT ( Device[Is Excluded] = TRUE () ) )
    VAR ActiveVuln =
        FILTER (
            ADDCOLUMNS (
                FILTER ( 'Software Vulnerabilities', 'Software Vulnerabilities'[Is Active] = TRUE () ),
                "Dev", RELATED ( 'Software Devices'[Defender Device ID] ),
                "Sev", RELATED ( Vulnerability[Severity Level] ),
                "Exp", RELATED ( Vulnerability[Exploitability Level] )
            ),
            [Dev] IN Pop
        )
    VAR CritOrExpl = FILTER ( ActiveVuln, [Sev] = "1 - Critical" || [Exp] = "Exploitable" )
    VAR Expl = FILTER ( ActiveVuln, [Exp] = "Exploitable" )
    VAR Crit = FILTER ( ActiveVuln, [Sev] = "1 - Critical" )
    VAR Both = FILTER ( ActiveVuln, [Sev] = "1 - Critical" && [Exp] = "Exploitable" )
    VAR Older = FILTER ( CritOrExpl, DATEDIFF ( 'Software Vulnerabilities'[First Seen], CollectedAt, DAY ) > 30 )
    VAR PerDevice = GROUPBY ( CritOrExpl, [Dev], "Latest", MAXX ( CURRENTGROUP (), 'Software Vulnerabilities'[Last Seen] ) )
EVALUATE
ROW (
    "Devices, critical or exploitable", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( CritOrExpl, "d", [Dev] ) ) ),
    "Devices, exploitable", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Expl, "d", [Dev] ) ) ),
    "Devices, critical", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Crit, "d", [Dev] ) ) ),
    "Devices, critical and exploitable", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Both, "d", [Dev] ) ) ),
    "CVEs, exploitable", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Expl, "c", 'Software Vulnerabilities'[vulnerability.id] ) ) ),
    "CVEs, critical", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Crit, "c", 'Software Vulnerabilities'[vulnerability.id] ) ) ),
    "Devices with one first seen over 30 days", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( Older, "d", [Dev] ) ) ),
    "Devices whose latest record is over 7 days old", COUNTROWS ( FILTER ( PerDevice, DATEDIFF ( [Latest], CollectedAt, DAY ) > 7 ) )
)
```

Drill-downs (use the same `ActiveVuln` variable):

- **Severity and exploitability grid:** `GROUPBY ( ActiveVuln, [Sev], [Exp] )` with distinct devices, CVEs (`vulnerability.id`), and pairs (`deviceVulnerability.id`) per group.
- **Most widespread exploitable CVEs:** add `"CVE", RELATED ( Vulnerability[Vulnerability Name] )` and `"CVSS", RELATED ( Vulnerability[CVSS V3] )`, group the exploitable rows by CVE, and rank by distinct devices.
- **Software involved:** add `"SW", RELATED ( 'Software Devices'[softwareVersion.id] )`, look up `Software[Software Name]` and `Software[Publisher]`, and rank products by distinct devices with a critical or exploitable vulnerability.

Rules:

- Active rows only. Never use `[Device Exploitable]` or `[Device Exploitable (%)]`.
- Share = affected devices over **assessed devices**. Say how many default-population devices are not assessed (S1).
- **Status age:** the vulnerability record's own last update (`Software Vulnerabilities[Last Seen]`) can be older than the device's last-seen date. Report devices whose latest critical or exploitable record is more than 7 days old separately from device last-seen age.
- "First seen more than 30 days before collection" describes how long Defender has listed the vulnerability on the device. It is not the time since a fix was released.
- Concentration (one CVE or one product on most devices) is context only. It does not mean the problem is easy to fix.

## S3: Devices Not Reporting

**What it checks:** default-population devices last seen more than 7 days before the data collection time, with last-seen bands and the device list.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR WithSoftware =
        DISTINCT ( SELECTCOLUMNS ( 'Software Devices', "Id", 'Software Devices'[Defender Device ID] ) )
    VAR Links =
        DISTINCT ( SELECTCOLUMNS (
            FILTER ( 'User Devices', NOT ISBLANK ( 'User Devices'[User ID] ) && 'User Devices'[Logon User] = TRUE () ),
            "Key", 'User Devices'[device.id], "Uid", 'User Devices'[User ID]
        ) )
    VAR Stale =
        FILTER ( Device,
            Device[Onboarding Status] = "Onboarded"
                && NOT ( Device[Is Excluded] = TRUE () )
                && DATEDIFF ( Device[Last Seen], CollectedAt, DAY ) > 7 )
EVALUATE
SELECTCOLUMNS (
    ADDCOLUMNS ( Stale,
        "Users", VAR k = Device[device.id] RETURN
            CONCATENATEX ( FILTER ( Links, [Key] = k ),
                LOOKUPVALUE ( 'User'[Full Name], 'User'[User ID], [Uid] ) & " ("
                    & LOOKUPVALUE ( 'User'[User Name], 'User'[User ID], [Uid] ) & "), "
                    & LOOKUPVALUE ( 'User'[Department], 'User'[User ID], [Uid] ), "; " ) ),
    "Device", Device[Device Name],
    "OS", Device[OS],
    "Release", Device[OS Release ID],
    "Manufacturer", Device[Device Manufacturer],
    "Model", Device[Device Model],
    "Device state", Device[Device State],
    "Last seen", Device[Last Seen],
    "Days before collection", DATEDIFF ( Device[Last Seen], CollectedAt, DAY ),
    "Has assessment data", Device[Defender Device ID] IN WithSoftware,
    "Users", [Users]
)
ORDER BY [Days before collection] DESC
```

- Report `Device State` as Defender states it, but compute the bands from `Last Seen`; `Device State` is fixed at collection.
- `User Devices` repeats a device and user pair (one row per network address and similar), so always take `DISTINCT` pairs before listing users.
- An empty user value means "No user associated".
- A device that has not been seen is not proof of a security problem. It may be offline, retired, or rebuilt. Its last known state may be out of date.
- State the overlap with S1 (devices not seen for a long time usually have no assessment data).

## S4: Missing Security Updates

**What it checks:** assessed devices with at least one active vulnerability whose fix Defender names as a Microsoft security update with a KB number.

```dax
DEFINE
    VAR CollectedAt = MAX ( 'Authorization'[Refresh Time] )
    VAR Pop =
        CALCULATETABLE ( VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded", NOT ( Device[Is Excluded] = TRUE () ) )
    VAR Upd =
        FILTER (
            ADDCOLUMNS (
                FILTER ( 'Software Vulnerabilities', 'Software Vulnerabilities'[Is Active] = TRUE () ),
                "Dev", RELATED ( 'Software Devices'[Defender Device ID] ),
                "Exp", RELATED ( Vulnerability[Exploitability Level] ),
                "KB", 'Software Vulnerabilities'[Missing Security Update ID],
                "Txt", 'Software Vulnerabilities'[Missing Security Update]
            ),
            [Dev] IN Pop
        )
    VAR WithKB = FILTER ( Upd, NOT ISBLANK ( [KB] ) )
    VAR TextOnly = FILTER ( Upd, ISBLANK ( [KB] ) && NOT ISBLANK ( [Txt] ) )
EVALUATE
ROW (
    "Devices missing a KB update", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( WithKB, "d", [Dev] ) ) ),
    "Distinct KB numbers", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( WithKB, "k", [KB] ) ) ),
    "Devices with a KB update listed over 30 days",
        COUNTROWS ( DISTINCT ( SELECTCOLUMNS (
            FILTER ( WithKB, DATEDIFF ( 'Software Vulnerabilities'[First Seen], CollectedAt, DAY ) > 30 ), "d", [Dev] ) ) ),
    "Devices with entries without a KB", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( TextOnly, "d", [Dev] ) ) ),
    "Distinct entries without a KB", COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( TextOnly, "t", [Txt] ) ) )
)
```

Drill-down by KB (same variables):

```dax
EVALUATE
TOPN ( 10,
    ADDCOLUMNS ( GROUPBY ( WithKB, [KB] ),
        "Devices", VAR k = [KB] RETURN COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( FILTER ( WithKB, [KB] = k ), "d", [Dev] ) ) ),
        "Devices with exploitable", VAR k = [KB] RETURN
            COUNTROWS ( DISTINCT ( SELECTCOLUMNS ( FILTER ( WithKB, [KB] = k && [Exp] = "Exploitable" ), "d", [Dev] ) ) ),
        "Release name", VAR k = [KB] RETURN MINX ( FILTER ( WithKB, [KB] = k ), [Txt] ) ),
    [Devices], DESC, [Devices with exploitable], DESC )
ORDER BY [Devices] DESC, [Devices with exploitable] DESC
```

- Show KB numbers with the "KB" prefix and the release name exactly as Defender states it.
- Entries without a KB number are their own group: give their device count and number of distinct entries, and list them only on request. Do not call them Microsoft updates.
- "Listed as missing for more than 30 days" is measured from first seen on the device, not from the update's release.
- State the overlap with S2 (the same devices usually appear in both).

## S5: End-of-Support Software

**What it checks:** active software installs on assessed devices whose status is `EOS Version` or `EOS Software`, or whose `Upcoming EOS Version` date is before the briefing date; and upcoming end-of-support dates for the Upcoming Deadlines section.

```dax
DEFINE
    VAR BriefingDate = DATE ( 2026, 1, 31 ) -- illustrative: use the briefing date (the user's local date)
    VAR Pop =
        CALCULATETABLE ( VALUES ( Device[Defender Device ID] ),
            Device[Onboarding Status] = "Onboarded", NOT ( Device[Is Excluded] = TRUE () ) )
    VAR Installs =
        FILTER (
            ADDCOLUMNS (
                FILTER ( 'Software Devices', 'Software Devices'[Is Active] = TRUE () ),
                "Status", RELATED ( Software[End Of Support Status] ),
                "EOS date", RELATED ( Software[End Of Support Date] ),
                "Product", RELATED ( Software[Software Name] ),
                "Publisher", RELATED ( Software[Publisher] )
            ),
            'Software Devices'[Defender Device ID] IN Pop && NOT ISBLANK ( [Status] ) && [Status] <> "None"
        )
EVALUATE
ADDCOLUMNS (
    GROUPBY ( Installs, [Status], [EOS date], [Product], [Publisher] ),
    "Devices", VAR s = [Status] VAR d = [EOS date] VAR p = [Product] VAR q = [Publisher] RETURN
        COUNTROWS ( DISTINCT ( SELECTCOLUMNS (
            FILTER ( Installs, [Status] = s && [EOS date] = d && [Product] = p && [Publisher] = q ),
            "d", 'Software Devices'[Defender Device ID] ) ) ),
    "Past by briefing date", [EOS date] < BriefingDate
)
ORDER BY [EOS date]
```

- **Finding:** distinct devices with an install whose status is `EOS Version` or `EOS Software`, or whose `Upcoming EOS Version` date is before the briefing date. Quote the status as stated at collection and say when a date has passed since collection.
- **Upcoming deadlines:** dates from the briefing date to `DeadlineWindowDays` later, one row per date, with distinct devices and the products and publishers involved. Find the next date after the window for the "next deadline" line.
- Blank status means not assessed; never count it as supported.
- Never substitute a date from an external lifecycle reference.

## Not in This Preview

The model also holds Microsoft Defender Antivirus state, security configuration assessment (including attack surface reduction rules), incidents and alerts, Secure Score, and cloud app data. This Preview does not analyze them. List them under "Not assessed" with the reason "not part of this Preview".
