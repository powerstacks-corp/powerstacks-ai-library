# BI for Defender Model Foundation

Status: Preview 0.1.0. Written for and tested with the BI for Defender release 15 schema on 2026-10-23. Use together with the [PowerStacks Analysis Foundation](analysis-foundation.md), which this file extends.

Model compatibility: written against the BI for Defender semantic model schema that matches BI for Defender release 15. The model does not expose its version, so the AI cannot read it. Confirm at runtime that the tables and columns you need exist; skills list theirs as `requiredSchema` in their manifests. A schema check shows that the tables and columns are **structurally available**. It does not prove that their meaning, values, or business rules match the version these instructions were written against.

Rules marked **(provisional)** are interpretations PowerStacks has not yet confirmed. Follow them; when one affects a result, report the result as the data states it and say that the interpretation is unconfirmed.

## 1. What the Model Is

BI for Defender is a semantic model of Microsoft Defender data: devices, Microsoft Defender Antivirus state, software inventory and its vulnerabilities, missing security updates, security configuration assessment, Secure Score, incidents and alerts, process and application control events, and discovered cloud apps. It also holds one PowerStacks license record with the data collection time.

- Most tables describe **current state as of the last data collection**.
- Secure Score is the only history: one snapshot per day.
- Process and application control events cover short windows of a few days at most by default; check their date range before using them.
- Incidents and alerts come from several Microsoft Defender services, not only from devices.

The model has no descriptions on tables, columns, or measures. Read measure definitions before using them.

## 2. Before You Query

1. Check the schema (the skill's Step 0).
2. Establish freshness first (section 8).
3. Decide the population and the device key before counting anything (sections 3 and 4).
4. Discover columns with `INFO.VIEW.COLUMNS()` or a schema tool, never by sampling rows, so device and user values are not pulled into the working context.

To connect, the AI tool needs the semantic model ID. It is the GUID after `/datasets/` or `/modeling/` in the semantic model's URL in the Power BI service (for example `https://app.powerbi.com/groups/<workspace ID>/datasets/<semantic model ID>` or `.../modeling/<semantic model ID>/modelView`).

## 3. Devices and Populations

`Device` has one row per Defender device record. It includes devices onboarded to Microsoft Defender for Endpoint and devices Defender discovered on the network but that are not onboarded.

| Column | Values and meaning |
| --- | --- |
| `Onboarding Status` | `Onboarded`, or `Can Be Onboarded` (discovered, not onboarded). Discovered records have few attributes and no assessment data. |
| `Device State` | `Active` or `Inactive`, as Defender reports it. It is fixed at the data collection time. |
| `Is Excluded` | TRUE when the device is excluded in Defender. Test as TRUE or not TRUE. |
| `Last Seen` | When Defender last saw the device. This is device activity, not the data collection time. |
| `Exposure Level`, `Risk Level` | Defender-calculated categories, reported as stated. `None` usually means the device has no current assessment. |

- **Default population:** onboarded devices that are not excluded (`Onboarding Status` = `Onboarded` and `Is Excluded` not TRUE), counted by distinct `Defender Device ID`, whatever their last-seen age. Show last-seen age with the population instead of excluding older devices; the customer chooses any exclusion.
- **Discovered devices** (`Can Be Onboarded`) are their own category. Report their count on its own line; never add them to the default population or any denominator.
- **Excluded devices** are reported as a count only.
- `[Device Count]` counts every record, including discovered devices. Do not use it as a denominator.

### Devices With Assessment Data

Antivirus state, software inventory, vulnerabilities, missing updates, and security configuration exist only for devices with a recent assessment. Devices that Defender has not seen for roughly the last 30 days, and devices onboarded very recently, can have no assessment data at all.

- **Applicable population for vulnerability, update, and software findings:** default-population devices that have at least one software inventory row (`Software Devices`). A device with software inventory and no vulnerabilities was assessed and has none.
- A device with no software inventory row is **not assessed**, never "no vulnerabilities". Count these devices and report them as a coverage gap.
- The exact assessment window is not documented (provisional; do not state a window as a rule, describe what the data shows, and say the window is unconfirmed).

### Device IDs Without a Device Record

Assessment tables can contain `Defender Device ID` values that have no row in `Device` (for example a device that was re-onboarded and received a new ID). These rows cannot be tied to a device, its name, or its last-seen date.

- Build the device set from `Device` and apply it to each fact table's own `Defender Device ID`. This excludes unmatched IDs consistently.
- Count the unmatched IDs and report them in Data Notes with how much data they carry, because table-level measures include them and report pages may show different totals.

## 4. Identifiers

| Identifier | Meaning | Use |
| --- | --- | --- |
| `Defender Device ID` | Microsoft Defender for Endpoint device identifier | **Device key.** Unique in `Device`; the key on `Device AntiVirus`, `Software Devices`, `Secure Configuration`, `Process`, `Application Control`, and `Device Tag`. |
| `device.id` | Key between `Device` and `User Devices` (hidden) | Joins devices to users. Usually equals `Azure AD Device ID`; falls back to the Defender ID when the device has no directory ID. Not the device key. |
| `Azure AD Device ID` | Directory device identifier | Can be blank. Do not use it to join to other PowerStacks models without a confirmed mapping. |
| `User ID` | Directory user identifier | Key of `User`. |
| `deviceSoftwareVersion.id` | One software version on one device | Joins `Software Vulnerabilities` to `Software Devices`. |
| `deviceVulnerability.id` | One vulnerability on one device | Count device and vulnerability pairs with a distinct count of this column. |
| `vulnerability.id` | One CVE | Joins to the `Vulnerability` catalog. |

Device names can repeat. Never join or count on device name.

## 5. Grain and Relationships

- Every relationship is bidirectional, and several are many-to-many. `User Devices` is the hub; device tables, alert evidence, and cloud app entities reach `Device` through it. Unfiltered paths through the hub can return every device; never infer a device link from an unfiltered bidirectional path.
- `Software Vulnerabilities` has no device column. It reaches devices only through `Software Devices` (`deviceSoftwareVersion.id`), so use `RELATED('Software Devices'[Defender Device ID])` in row context or `TREATAS` onto `Software Devices[Defender Device ID]`.
- One device and CVE pair can appear on several rows (one per affected software version). Count pairs with `DISTINCTCOUNT` of `deviceVulnerability.id`, CVEs with `vulnerability.id`, and devices with the device key.
- `Vulnerability` is the **full CVE catalog**, not the tenant's findings. Never count from it directly; always start from `Software Vulnerabilities`.
- `Secure Configuration` has one row per device and configuration. `Device AntiVirus` has one row per device.

## 6. Existing Measures

**Measures carry no population filters by design.** Apply the population yourself when you query the model directly. Several measures count something different from what a security question usually needs:

| Measure | What it counts | Use instead |
| --- | --- | --- |
| `[Device Exploitable]` | Devices with any exploitable vulnerability row, **including fixed** rows | Distinct devices from active rows only |
| `[Device Exploitable (%)]` | The above divided by **every device record**, including devices with no vulnerability data and discovered devices | Devices with active exploitable rows over default-population devices with software inventory |
| `[Vulnerabilities Detected Count]`, `[Vulnerabilities Exploitable Count]`, `[Vulnerability Detected]`, `[Vulnerability Exploitable]` | Pairs or CVEs **including fixed** rows and unmatched device IDs | Distinct counts on active rows for devices in the device set |
| `[Missing Security Updates Count]` | Distinct missing update **text** values, including fixed rows | Distinct `Missing Security Update ID` on active rows |
| `[AntiVirus Active Rate (%)]` | Active antivirus rows over every device record | Not used by the security briefing |
| `[Secure Score (%)]` | Sum over every snapshot unless filtered | Filter `Secure Score[Is Latest]` = TRUE or one date |
| `[Device Count]` | Every device record | Default population |

Report pages that use these measures can show different figures from a skill that applies these rules. When a user compares, explain the difference in plain English.

`[Viewer Name]` returns the signed-in user. Never use it in AI output.

## 7. Data Settings (Semantic Model Parameters)

BI for Defender has data settings (semantic model parameters), but no settings have been approved for AI reading. **Read no parameters.** Never read `ApiKey`, `AzureAD TenantID`, `AzureAD ClientID`, or `AzureAD ClientSecret`, and never run `INFO.EXPRESSIONS()` or `INFO.PARTITIONS()`. Infer from the data which optional parts are present, say that it was inferred, and report an empty optional table as "not present in this data", not as a problem on devices.

## 8. Freshness and Time

| Time | Column | Meaning |
| --- | --- | --- |
| Data collection time | `Authorization[Refresh Time]` | When the data was collected. Everything is as of this time or earlier. The time zone is not stated in the model. |
| Device activity | `Device[Last Seen]` | When Defender last saw the device |
| Assessment activity | `Software Vulnerabilities[Last Seen]`, `Secure Configuration[Last Update]` | When the assessment record was last updated |
| First detection | `Software Vulnerabilities[First Seen]` | When the vulnerability was first seen on the device |
| Collection-only times | `Device[Device Info Time]`, `Device AntiVirus[Last Update]` | Export times. Not device activity. |

- **Data age:** compute it from the collection time and the briefing date. When the data is older than expected, say so first: every figure describes the state at collection.
- Columns ending in `(Days)` are calculated with `NOW()` or `TODAY()` at refresh and are out of date by the time of the answer. Compute ages yourself.
- **Last-seen age:** compute from `Device[Last Seen]` to the data collection time, so the bands describe the devices as of the data. State the data age separately. Do not use `Device State` or `Last Seen (Days)` for bands.
- **Briefing date:** the user's local date (state the time zone). **Days remaining for a date** (for example end of support) is calculated from the briefing date, never from a stored `(Days)` column.
- **License record:** `Authorization[Status]`, `[License Type]`, `[Start Date]`, and `[End Date]` describe the PowerStacks license. Report them as stated; an end date inside the deadline window is a deadline.

## 9. Last-Seen Age

Report the full default population with last-seen call-outs: how many devices were last seen more than 7, 14, 30, 60, and 90 days before the data collection time. Apply the same call-out to every finding's affected devices.

- A device last seen long ago keeps its last known state, which may be out of date.
- **Age-mix flag:** when more than half of the devices behind a finding were last seen more than 7 days before collection, say so next to the figure and lower the finding's confidence by one level. Keep the full count.
- List the devices last seen more than 7 days before collection, with the identifying details in section 11.
- The customer chooses any exclusion; never exclude devices by last-seen age unless the user asks.

## 10. Fields That Need Care

- **Vulnerability status.** `Software Vulnerabilities[Is Active]` is TRUE for the statuses `New`, `Active`, and `Updated`, and FALSE for `Fixed`. Count active rows only. Not every status value occurs in every tenant.
- **Severity and exploitability** come from the catalog through the relationship: `Vulnerability[Severity Level]` (`1 - Critical`, `2 - High`, `3 - Medium`, `4 - Low`, `Unknown`) and `Vulnerability[Exploitability Level]` (`Exploitable`, `No Exploit`). Exploitability is the only exploit signal in the model; there is no exploit-kit or exploit-verified field. Report both values as Defender states them.
- **Missing security updates.** `Missing Security Update ID` holds a KB number for Microsoft updates; `Missing Security Update` holds text that names a release (for example "<month> <year> Security Updates") and, for other entries, can be other text such as a CVE ID. Several KB numbers can share one text. Count Microsoft updates by KB number, and treat entries without a KB number as their own group, listed as stated.
- **Missing Security Update Age (Days)** is the number of days since the vulnerability was first seen on the device, not since the update was released. Call it "listed as missing for", never patch lag.
- **First Seen** can carry very old dates that may reflect where the source's history begins. Use simple "more than 30 days" call-outs; do not present long-term age trends.
- **End of support.** `Software[End Of Support Status]` values include `None`, `EOS Version`, `EOS Software`, and `Upcoming EOS Version`. Blank means not assessed, not supported. Report the status and `End Of Support Date` as stated. A status of `Upcoming EOS Version` whose date has passed by the briefing date is reported as past its date, with the status quoted as stated at collection.
- **Microsoft Defender Antivirus fields describe Defender only.** Many organizations run a third-party antivirus. Never report Defender antivirus fields as a protection gap unless the user confirms Defender is their antivirus.
- **Secure Score.** Filter to one snapshot. `Secure Score Control[Implementation Status]` is free text that can contain policy and account names; never quote it.
- Status text can vary in case between sources (for example lower-case values). Report it as stated.

## 11. Personal and Device Data

The model contains user names, email addresses, device names, and network addresses. **Never mask data.** The people using these answers already have access to the underlying data, so show values exactly as stored. Summarize with counts and list devices where a rule requires it or the user asks.

**Help the customer identify devices.** Whenever you list devices, include: device name, OS and release, manufacturer and model (when present), the users Defender records as signed in to the device (`User Devices[Logon User]` = TRUE; `User[User Name]`, `[Full Name]`, `[Department]`), last-seen date, and days before collection. If no user is recorded, write "No user associated". The model has no serial number. Look users up from `User Devices` filtered to the device's `device.id`, taking distinct device and user pairs (the table repeats a pair once per network address and similar); do not rely on unfiltered relationship paths.

## 12. Transformations and Caveats

- **Transformations:** PowerStacks has not documented value transformations for the fields used by the security briefing. Report values as stated.
- **Caveats:** optional data (for example browser extensions or application control events) depends on the customer's Defender licensing and settings. An empty optional table is not a device problem.
