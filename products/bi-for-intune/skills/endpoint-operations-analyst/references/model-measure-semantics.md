# Measure Semantics

Status: draft. Not validated. Based on the measure definitions in BI for Intune version 69. Re-read definitions at runtime if results look unexpected.

Measures carry no population filters by design; PowerStacks applies filters in the reports. Apply the managed-device filter yourself when querying the model.

## What Common Measures Count

| Measure family | Counts | Identifier | Filters applied | Use for |
| --- | --- | --- | --- | --- |
| `[Device Count]` | Distinct records | `Device[device.id]` | None | Every record from every source (Intune, Autopilot, Update Compliance, Sign-In, Enrollment, Cloud PC). Not the managed-device count. |
| `[Device Compliant]`, `[Device Non Compliant]`, `[Device ConfigMgr]` | Distinct devices | `Device[Intune Device ID]` | `Device[Compliance]` value only | Overall device compliance. Includes unmanaged records and devices not seen for 30+ days unless you apply the managed-device filter. |
| `[Device Unknown]`, `[Device Error]`, `[Device Conflict]`, `[Device In Grace Period]` | Distinct devices | `Device[Intune Device ID]` | Compliance values that may not occur in a given tenant | `In Grace Period` is a valid Intune state that only appears when the tenant configures a compliance grace period. For compliance breakdowns, group by `Device[Compliance]` and report the values present by name, including values with no measure (for example `Not Evaluated`). A BLANK result means no devices in that state in this data; do not read anything more into it. |
| `[OS Security Update Missing]`, `[... Not Latest]`, `[... Latest]`, `[OS Quality Update ...]`, `[OS Feature Update ...]` | Distinct devices | `Device[device.id]` | OS update status columns | OS update posture. Apply the managed-device filter. |
| `[App Failed]`, `[App Installed]`, `[App State]` and related | **Rows** | n/a | `App Status`, non-blank `User Devices[DeviceIDUPN]` | Status records. For devices, count distinct `User Devices[Intune Device ID]` filtered by `Application State[App Status]`. |
| `[Configuration Error]`, `[Configuration Non Compliant]`, `[Configuration State]` and related | **Rows** | n/a | `Configuration Status`, non-blank `User Devices[DeviceIDUPN]` | Status records. For devices, distinct count `Configuration State[Intune Device ID]`. |
| `[Policy Non Compliant]`, `[Policy State]` and related | **Rows** | n/a | `Policy Status`, non-blank `User Devices[DeviceIDUPN]` | Status records. For devices, distinct count `Compliance Policy State[Intune Device ID]`. |
| `[Script Fail]`, `[Remediation Failed]`, `[Detection Fail]`, `[Windows Update Ring ...]`, `[Feature Update Aggregated ...]` | **Rows** | n/a | Status value, non-blank `User Devices[Intune Device ID]` | Status records. Convert to distinct devices on the status table. |
| `[Encryption ...]`, `[Firewall ...]`, `[Protection ...]` (counts), `[Windows 11 ...]`, `[Performance ...]`, `[Device App Reliability ...]` | Distinct devices | `Device[Intune Device ID]` | Value in the related table | Posture counts for devices that report the data. |
| `[Protection Success Rate (%)]`, `[Performance Health (%)]`, `[Windows 11 Readiness (%)]`, `[Device App Reliability Health (%)]` | Ratio | Rows | Denominator is `COUNTROWS(Device)` | The denominator includes records from every source. Recalculate for managed devices. |
| `[Enrollment Failure Count]` | Distinct failures | `Enrollment Failure ID` | None | Enrollment failures in the window the table covers. |
| `[Connector Count]` | Distinct connectors | `connector.id` | None | Connector inventory. |

## Rules

1. When a row-counting measure is used, say "status records" and give the distinct device count alongside it.
2. The `User Devices` filter inside status measures drops records that have no matching association. Direct counts on the status table can be higher. State which one you report.
3. A BLANK measure result can mean zero, an unused status value, or missing data. Check `VALUES()` of the filtered column before concluding.
4. Do not compare a row-based measure with a device-based measure as if they were the same unit.
