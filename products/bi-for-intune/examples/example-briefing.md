# Example Briefing (BI for Intune)

This is real output from the Endpoint Operations Analyst skill, run against a small PowerStacks demo environment on 2026-10-23 with the briefing filters lowered to 1 device and 0% because the environment is small. Device tables are omitted. Your briefing will reflect your own environment.

---

## Endpoint Briefing

**Data as of:** 10/23/2026 5:08 PM UTC (queried 10/23/2026 11:17 PM UTC).
**Population:** 15 managed devices (14 Windows 11, 1 macOS). Last check-in: 0 over 14 days, 0 over 30 days, 0 over 60 days, 0 over 90 days. None are Cloud PCs.
**Other device categories:** 1 device managed by app protection policies only (no enrollment; app protection results below). 1 Windows Server managed through Defender security settings.
**Coverage:** 9 managed Windows devices are not enrolled in Windows Update for Business reports, so they have no update status. All 9 are Microsoft Entra joined (none Microsoft Entra registered, none with an unknown join type); 2 devices report to Windows Update for Business reports but are not in Intune (2 scanned within 14 days). 4 managed devices are not reporting custom inventory (3 Windows, 1 macOS; 4 checked in within 14 days). For the Windows devices, this includes their Microsoft 365 Apps data. 3 Dell Inc. and HP devices (2 Dell Inc., 1 HP) have warranty records with no warranty dates (3 checked in within 14 days); the warranty lookup may be failing for these vendors.
**Method:** Ranked by scale (distinct affected devices). Briefing filters: at least 1 device and at least 0% of the applicable population (lowered from the defaults of 10 devices and 1% for this small demo tenant, as you asked). Scope: all managed devices. Check-in bands: 14 / 30 / 60 / 90 days. No devices excluded by check-in age unless you ask. All other inputs at their defaults. Briefing date: 10/23/2026 (Central Time, UTC-05:00; collection and query times are UTC).

### Upcoming Deadlines (next 14 days)

Display window only; it is not a policy or urgency judgment.

No source-reported deadlines in the next 14 days.
Next deadline beyond this window: 10/10/2028 (718 days), end of service for Windows 11, version 25H2 (Enterprise and Pro editions) per Windows Update for Business reports, 4 devices.

### 1. Platform scripts failing on every device with a script result

- **What we found:** Intune reports a failed platform script result on all 12 managed devices that have a script result. "App Inventory 2" failed on 11 Windows 11 devices: error code 0x00000003 (3) on 6 and 0x00000063 (99) on 5. "BI-For-Intune-Lab-UC-2023" failed on the 1 macOS device with error code 0x00000000 (0), reported as stated. No device failed both scripts.
- **Scope:** 12 of 12 managed devices with a platform script result (100%). Last check-in: 0 over 14 days, 0 over 30, 0 over 60, 0 over 90.
- **Status age:** 10 of the 12 failed results were reported within 7 days of the data refresh; the other 2 are 8 and 9 days old.
- **Concentration:** One script, "App Inventory 2", accounts for 11 of the 12 devices (92%).
- **Drill-down:** "App Inventory 2": 11 Windows 11 devices (6 with 0x00000003 (3), 5 with 0x00000063 (99)). "BI-For-Intune-Lab-UC-2023": 1 macOS device.
- **Overlap:** 6 of these devices are also in finding 2, 4 in finding 3, and 1 in finding 4.
- **Why it matters:** Whatever these scripts are deployed to do may not have completed on these devices. The error codes alone do not show why.
- **Based on:** Intune's platform script results for managed devices, counted once per device.
- **Next step:** In the Intune admin center, review the device status, output, and error for "App Inventory 2" on a few devices with each error code, and the result of "BI-For-Intune-Lab-UC-2023" on the macOS device.
- **Confidence:** High. The results are recent and every affected device checked in within the last 9 days.
- **Affected devices:** 12 devices, oldest check-in first.

*Device table omitted in this example. In a real briefing it lists each affected device with its serial number, primary user, department, OS, and days since last check-in.*

### 2. Managed Windows devices not enrolled in Windows Update for Business reports

- **What we found:** 9 managed Windows 11 devices are not enrolled in Windows Update for Business reports, so BI for Intune has no Windows update status for them. All 9 are Microsoft Entra joined; none are Microsoft Entra registered and none have an unknown join type. All 9 report the model "Virtual Machine" from Microsoft Corporation; none are Cloud PCs.
- **Scope:** 9 of 14 managed Windows devices that are Microsoft Entra joined or hybrid joined (64.3%). Last check-in: 0 over 14 days, 0 over 30, 0 over 60, 0 over 90.
- **Overlap:** All 7 devices in finding 3 are in this finding; 6 of these devices are also in finding 1 and 3 in finding 4.
- **Why it matters:** Windows update findings do not cover these devices: their security update and end-of-service status is unknown in this data.
- **Based on:** Each managed Windows device's Windows Update for Business reports enrollment flag and join type.
- **Next step:** Check the Windows Update for Business reports enrollment prerequisites for these devices, for example the data-sharing policy and the diagnostic data configuration.
- **Confidence:** Medium. Windows Update for Business reports can take from 72 hours to two weeks to include a newly configured device, and the data does not show when these devices were configured.
- **Affected devices:** 9 devices, oldest check-in first.

*Device table omitted in this example. In a real briefing it lists each affected device with its serial number, primary user, department, OS, and days since last check-in.*

### 3. Managed devices reporting Not Encrypted

- **What we found:** Intune reports "Not Encrypted" on 7 managed Windows 11 devices, all with encryption readiness "Not Ready". 3 of them report "Encryption method of OS Volume is different than that set by policy", which can mean the disk is encrypted with a different method (a policy mismatch, not proof of an unencrypted disk); the other 4 give no detail. All 7 report the model "Virtual Machine" from Microsoft Corporation; none are Cloud PCs. The other 6 devices with a status report "Encrypted".
- **Scope:** 7 of 13 managed devices with an encryption status (53.8%). Last check-in: 0 over 14 days, 0 over 30, 0 over 60, 0 over 90. 2 managed devices have no encryption status and are unknown.
- **Drill-down:** No detail: 4 devices. "Encryption method of OS Volume is different than that set by policy": 3 devices.
- **Overlap:** All 7 devices are also in finding 2; 4 are in finding 1 and 3 in finding 4.
- **Why it matters:** Devices whose disks are not encrypted are exposed if the device or disk is lost.
- **Based on:** Intune's per-device encryption status, readiness, and status details for managed devices.
- **Next step:** For the 3 devices with a method mismatch, compare the encryption method on the device with the method set by the encryption policy. For the other 4, check the encryption policy assignment and why readiness reports "Not Ready" on these virtual machines.
- **Confidence:** Medium. 3 of the 7 statuses describe a method mismatch, which may not mean the disk is unencrypted.
- **Affected devices:** 7 devices, oldest check-in first.

*Device table omitted in this example. In a real briefing it lists each affected device with its serial number, primary user, department, OS, and days since last check-in.*

### 4. Managed devices not reporting custom inventory

- **What we found:** 4 managed devices (3 Windows 11, 1 macOS) are not reporting PowerStacks custom inventory, so their hardware details, disk health, app inventory, and driver inventory are not present. For the 3 Windows devices, this includes their Microsoft 365 Apps data (their Microsoft 365 Apps status shows "Unknown").
- **Scope:** 4 of 15 managed Windows and macOS devices (26.7%). Last check-in: 0 over 14 days, 0 over 30, 0 over 60, 0 over 90.
- **Overlap:** The 3 Windows devices are also in findings 2 and 3; the macOS device is also in finding 1.
- **Why it matters:** Disk health, inventory, and Microsoft 365 Apps findings do not cover these devices.
- **Based on:** Each managed device's custom inventory flags in BI for Intune.
- **Next step:** Check that the inventory script is assigned to these devices and review its recent results in Intune.
- **Confidence:** High. All 4 devices checked in within the last day.
- **Affected devices:** 4 devices, oldest check-in first.

*Device table omitted in this example. In a real briefing it lists each affected device with its serial number, primary user, department, OS, and days since last check-in.*

### 5. Devices in Windows Update for Business reports but not in Intune

- **What we found:** 2 Windows 11 device records appear in Windows Update for Business reports with no Intune record. Both last scanned with Windows Update 13 days before the data refresh. They are outside the managed population.
- **Scope:** 2 of 7 Windows devices known to Windows Update for Business reports (28.6%). Last Windows Update scan: 2 within 14 days. They have no Intune check-in.
- **Why it matters:** A recent scan means the device is active but not managed by Intune, which indicates a problem with its management state.
- **Based on:** Windows Update for Business reports device records that have no matching Intune record.
- **Next step:** Find these devices in Microsoft Entra ID and Intune by device ID and check why they are not enrolled or why their Intune record is missing.
- **Confidence:** Medium. The data shows the records and their scan dates but cannot show whether these devices are still in use.
- **Affected devices:** 2 devices, oldest check-in first.

*Device table omitted in this example. In a real briefing it lists each affected device with its serial number, primary user, department, OS, and days since last check-in.*

### Additional Findings

Findings identified by the completed checks that are not in the main briefing. This is not a complete list of every possible issue.

| Finding | Affected devices | Applicable | % | Why not in the main briefing |
| --- | --- | --- | --- | --- |
| Endpoint Analytics startup performance "Needs Attention" (Microsoft's scoring; app reliability results not present) | 1 | 4 | 25% | Ranked below the top five by scale |
| Windows security update status "Not Latest" per Windows Update for Business reports (Windows 11, version 25H2 Enterprise) | 1 | 5 | 20% | Ranked below the top five by scale |
| Microsoft 365 Apps reported as "Outdated" (8 other Windows devices report "Unknown") | 1 | 5 | 20% | Ranked below the top five by scale |
| Windows app (Win32) install failures: 20 apps on 1 device. 0x87D30000 (-2016215040) on 19 apps, "Unknown error."; 0x87D30068 (-2016214936) on 1 app, "Error downloading content."; also 1 "Uninstall Failed", 0x80070864 (-2147022748). No Microsoft description found for these codes. | 1 | 8 | 12.5% | Ranked below the top five by scale |
| Device reported "Non Compliant" ("Is active" setting on the Default Device Compliance Policy) | 1 | 15 | 6.7% | Ranked below the top five by scale |
| Apple MDM Push Certificate (expired 10/29/2025), Apple DEP Token (expired 11/8/2025, last synced 557 days ago), and Apple VPP Token (expired 11/8/2025) report state "Error" | 1 (managed Apple device) | Tenant-level | Not determined | Always flagged; ranked below the top five by scale |
| Dell Inc. and HP devices with warranty records but no warranty dates (2 Dell Inc., 1 HP) | 3 | 3 | 100% | Possible warranty lookup problem |
| "BI-For-Intune-Lab-UC-2023" script failure on the macOS device | 1 | 12 | 8.3% | Part of finding 1 (drill-down) |

### Not Assessed

- Defender Antivirus health: the primary antivirus was not specified. Defender fields show only Defender's own state, which is expected to be off or out of date when another antivirus is in use.

### Data Notes

- Refresh history was not checked in this run.
- The oldest check-in among managed devices is 9 days. Devices silent for longer than this tenant's Intune device cleanup limit may already have been removed and cannot be counted.
- The latest monthly security update at the data refresh was the 10/13/2026 release; this date comes from Microsoft's second-Tuesday release schedule, not from the model.
- Endpoint Analytics app reliability results are not present in this refresh, while startup performance results loaded for 4 devices; this can be a data-collection setting. Contact PowerStacks support if you expected it.
- No failed enrollment attempts and no Autopilot deployments are recorded in this refresh, so no time window can be stated.
- Disk health: 11 devices report "Healthy"; no disk reports a predicted failure. The 4 devices without custom inventory have no disk health data and are unknown.
- The configuration profile "Standard Elevation Policy" shows "Unknown" on 3 devices; reported as unknown, not as errors. No profile reports Error or Conflict.
- Every remediation result is "Skipped" (5 devices, 8 packages), meaning the detection scripts found nothing to remediate.
- App protection: status is linked to a device for 1 device user (Microsoft OneDrive on iOS/iPadOS), and the app is protected. No unprotected apps were found.
- 1 device record has a management source of "ConfigMgr"; it is outside the managed population.

### Devices Not Checked In for More Than 14 Days

0 managed devices: 0 over 14 days, 0 over 30, 0 over 60, 0 over 90. Every managed device checked in within 9 days of the data refresh.

Ask me to list the affected devices for any finding in Additional Findings.
Ask me to exclude devices that have not checked in for more than any number of days you choose (for example 14, 30, 60, or 90), to focus on a platform or group, or to change the briefing filters.
Ask me to rank by security relevance, scale, concentration, or nearest deadline, or to change the deadline window.

Email subject: Daily AI Generated Endpoint Briefing 10/23/2026
