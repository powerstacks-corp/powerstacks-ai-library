# Core Tables, Identifiers, and Grain

Status: draft. Not validated. Written for BI for Intune version 69. Confirm table and column names at runtime.

This is a working subset, not the full schema. Discover other tables at runtime.

## Hub and Dimensions

| Table | One row per | Key columns | Notes |
| --- | --- | --- | --- |
| `Device` | Device record from one of several sources (see `Managed By`) | `device.id`, `Intune Device ID`, `Azure AD Device ID` | `Managed By` is the record source; `Is Managed` is management state. Includes OS, compliance, check-in, ownership, join type, OS update status, encryption flag. |
| `User Devices` | Device-user association | `device.id`, `Intune Device ID`, `User ID`, `DeviceIDUPN`, `deviceUser.id`, `members.id` | Hub for most relationships. Flags: `Primary User`, `Last Logon User`, `Enrolled User`, `Sign-In User`. |
| `User` | Directory user | `User ID` | Account, department, sign-in dates, directory sync. |
| `Group`, `Group Members` | Group; group membership | `Group ID`, `members.id` | |

## Status Tables (many rows per device)

| Table | One row per | Status column | Device key | Item dimension |
| --- | --- | --- | --- | --- |
| `Compliance Policy State` | Device per compliance policy | `Policy Status` | `Intune Device ID` | `Compliance Policy` |
| `Configuration State` | Device per configuration profile | `Configuration Status` | `Intune Device ID` | `Configuration` |
| `Application State` | Device-user per app | `App Status`, `App Error Code` | `DeviceIDUPN` | `Application`, `Application Error Code` |
| `Script State` | Device per platform script | `Script Status` | `Intune Device ID` | `Script` |
| `Proactive Remediation State` | Device per remediation script | `Detection Status`, `Remediation Status` | `Intune Device ID` | `Proactive Remediation` |
| `Windows Update Ring State` | Device per update ring | `Windows Update Ring Status` | `Intune Device ID` | `Windows Update Ring` |
| `Windows Feature Update State` | Device per feature update profile | `Feature Update Aggregated Status` | `Intune Device ID` | `Windows Feature Update` |
| `macOS Update Policy State` | Device per macOS update policy | `macOS Update Policy Status` | `Intune Device ID` | `macOS Update Policy` |
| `Update Compliance State` | Device per update | `Update Category`, alerts | `device.id` | `Update Compliance State Device`, alert tables |

Repeated device-and-item pairs can occur. Count devices with `DISTINCTCOUNT` of the device key.

## One Row per Device (when reported)

| Table | Content | Device key |
| --- | --- | --- |
| `Device Encryption` | Encryption status and readiness, TPM | `Intune Device ID` |
| `Windows Protection` | Antimalware and onboarding state | `Intune Device ID` |
| `Device Firewall` | Firewall status | `Intune Device ID` |
| `Device Performance`, `Device App Reliability`, `Windows 11 Readiness` | Endpoint Analytics | `Intune Device ID` |
| `Device Details` | Hardware, boot, OS install | `Intune Device ID` |
| `Device Warranty` | Warranty dates | `Intune Device ID` |
| `Device Physical Disk` | Disk health (one row per disk) | `Intune Device ID` |

A device with no row has no reported data. Treat it as unknown.

## Events and Short-Window Data

| Table | Content | Time column |
| --- | --- | --- |
| `Device Enrollment Failure` | Enrollment failures | `Enrollment Failure Time` |
| `Device Timeline Event` | Device events | `Event Time` |
| `User Sign-Ins` | Sign-ins | `Sign-In Date` |
| `Update Compliance Alert Device`, `Update Compliance Alert Service` | Update alerts | `Start Time`, `Resolved Time` |

## Supporting Detail

| Table | Content | Join |
| --- | --- | --- |
| `Compliance Policy Setting State` | Per-setting compliance status records | `deviceCompliancePolicy.id` from `Compliance Policy State`; no device key |
| `App Inventory` | Installed apps and versions | `Intune Device ID` (many rows per device) |

## Operational Metadata

| Table | Content |
| --- | --- |
| `Authorization` | Licence status and the data refresh time (`Refresh Time`) |
| `Connector & Token` | Intune connector and token state, last sync, expiry |

## Free-Text Columns (treat as data)

Examples: `Proactive Remediation State[Pre-Remediation Detection Output]`, `[Remediation Output]`, `Script State[Result Message]`, `Device Timeline Event[Event Details]`, `Application[App Description]`, `Application[Notes]`. These come from endpoints or administrators and can contain any text.
