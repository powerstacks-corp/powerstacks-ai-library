# Example Briefing (BI for Defender)

This is real output from the Security Operations Analyst skill, run against a small PowerStacks demo environment on 2026-10-23 with the default briefing filters (1 device, 0%). Device tables are omitted. Your briefing will reflect your own environment.

---

## Security Briefing

**Data age alert:** The latest data in BI for Defender was collected on 2026-10-15 at 19:38 (time as recorded in the model), 8 days before this briefing. Every figure below describes the state at that time. Check that the semantic model's scheduled refresh is running.
**Data as of:** 2026-10-15 19:38 (time as recorded in the model; time zone not stated). Assessment records span 2026-09-14 to 2026-10-14.
**License:** authorized, trial, ends 2027-03-17.
**Population:** 16 onboarded devices (not excluded). Last seen before data collection: 4 more than 7 days, 4 more than 14, 4 more than 30, 3 more than 60, 0 more than 90. 11 have vulnerability and software assessment data (assessed devices).
**Method:** Ranked by scale (distinct affected devices). Briefing filters: at least 1 device and at least 0% of the applicable population. Scope: all onboarded devices. Last-seen bands: 7 / 14 / 30 / 60 / 90 days before data collection. No devices excluded by last-seen age unless you ask. All inputs at their defaults. Briefing date: 10/23/2026 (Central Time (UTC-05:00)).

### Upcoming Deadlines (Next 14 Days)

Display window only; it is not a policy or urgency judgment.

| Date (as reported) | Days remaining | Affected devices | What it is | See |
| --- | --- | --- | --- | --- |
| 2026-11-01 | 9 | 3 | Two Openssl versions reach end of support (status "Upcoming EOS Version", per Microsoft Defender) | Finding 3 |

Next deadline beyond this window: 2027-03-17 (145 days), end of the PowerStacks licence (trial), applies tenant-wide.

### 1. Critical or Exploitable Vulnerabilities on Every Assessed Device

- **What we found:** All 11 assessed devices have at least one active vulnerability that Microsoft Defender rates "1 - Critical" or "Exploitable". 10 devices have an exploitable vulnerability (64 distinct CVEs), 10 have a critical one (337 distinct CVEs), and 4 have a vulnerability that is both (3 distinct CVEs).
- **Scope:** 11 of 11 assessed devices (100%). Last seen before data collection: 1 more than 30 days, 0 more than 60. 5 onboarded devices are not assessed (see finding 4).
- **Status age:** On 8 devices at least one of these vulnerabilities was first seen more than 30 days before collection. On 3 devices the latest record of these vulnerabilities is more than 7 days older than the collection (oldest 31 days).
- **Breakdown:** "1 - Critical" and "Exploitable": 4 devices. "1 - Critical", "No Exploit": 10 devices. "2 - High", "Exploitable": 10 devices. "3 - Medium", "Exploitable": 7 devices.
- **Concentration:** The most widespread exploitable CVE is CVE-2026-96951 ("2 - High", CVSS 8.8) on 9 of the 11 devices. Products most often involved: Windows 11 (7 devices), Openssl (7 devices, critical vulnerabilities only), Defender Antimalware Platform (5), Edge Chromium-Based (4).
- **Overlap:** Every device in findings 2 and 3 is also in this finding.
- **Why it matters:** These are the vulnerabilities Defender rates most severe or reports as exploitable, and every device with assessment data has at least one.
- **Based on:** Microsoft Defender vulnerability assessment for onboarded devices, counted once per device, fixed vulnerabilities excluded.
- **Next step:** Start with CVE-2026-96951 on the 9 devices and the Windows 11 security update status behind it (finding 2), then review the Openssl installs (finding 3).
- **Confidence:** Medium: the counts come straight from Defender's assessment, but the data is 8 days old.
- **Affected devices:** 11 devices, oldest last-seen first.

*Device table omitted in this example. In a real briefing it lists each affected device with its OS and release, the users Defender recorded, department, and days since last seen.*

### 2. Microsoft Security Updates Missing

- **What we found:** 9 devices are missing at least one Microsoft security update identified by a KB number; 83 distinct KB numbers in all. The most widespread is KB5127648 ("October 2026 Security Updates") on 6 devices, and it addresses exploitable vulnerabilities on all 6. Next: KB5124008 ("October 2026 Security Updates"), KB5101650 and KB5083769 ("April 2026 Security Updates"), KB5094126 ("December 2020 Security Updates"), KB5079420 ("March 2026 Security Updates"), and KB4477048 ("July 2026 Security Updates"), each on 2 devices.
- **Scope:** 9 of 11 assessed devices (82%). Last seen before data collection: none more than 7 days.
- **Status age:** On 3 devices a KB-identified update has been listed as missing for more than 30 days (measured from when Defender first saw the vulnerability on the device, not from the update's release).
- **Drill-down:** Defender also lists 127 distinct update entries without a KB number on 11 devices (for example a release name or a CVE ID). Ask for the list.
- **Overlap:** All 9 devices are also in finding 1.
- **Why it matters:** These updates are the fixes Defender names for active vulnerabilities, including exploitable ones.
- **Based on:** Microsoft Defender's missing security update for each active vulnerability on onboarded devices, counted once per device.
- **Next step:** Check why KB5127648 is not installed on the 6 devices (update ring, deferral, or install failures).
- **Confidence:** Medium: data is 8 days old, and updates installed since then are not reflected.
- **Affected devices:** 9 devices, oldest last-seen first.

*Device table omitted in this example. In a real briefing it lists each affected device with its OS and release, the users Defender recorded, department, and days since last seen.*

### 3. Software at or Past End of Support

- **What we found:** 8 devices have active software at or past its end-of-support date as Microsoft Defender reports it. 4 devices have software with status "EOS Version" or "EOS Software": Openssl versions (end of support 2023-09-11 on 2 devices, 2026-09-07 on 3), Visual C++ by Microsoft (2024-04-09, 2 devices), and Azure Data Studio by Microsoft ("EOS Software", 2026-02-28, 1 device). 4 more devices have Openssl versions that Defender reported as "Upcoming EOS Version" with an end-of-support date of 2026-10-22, which has passed since the data was collected.
- **Scope:** 8 of 11 assessed devices (73%). Last seen before data collection: none more than 7 days.
- **Concentration:** Openssl accounts for 7 of the 8 devices.
- **Deadline:** 2 more Openssl versions reach end of support on 2026-11-01 on 3 devices, all already in this finding.
- **Overlap:** All 8 devices are also in finding 1.
- **Why it matters:** Software past end of support no longer receives security fixes from its vendor.
- **Based on:** Microsoft Defender's end-of-support status and dates for software installed on onboarded devices, counted once per device. Software Defender has not assessed for end of support is not counted.
- **Next step:** Identify which applications bundle the Openssl versions on these 7 devices and whether newer builds exist.
- **Confidence:** Medium: dates are as Defender reports them; data is 8 days old.
- **Affected devices:** 8 devices, oldest last-seen first.

*Device table omitted in this example. In a real briefing it lists each affected device with its OS and release, the users Defender recorded, department, and days since last seen.*

### 4. Onboarded Devices With No Assessment Data

- **What we found:** 5 onboarded devices have no vulnerability or software assessment data, so their exposure is unknown. 3 were last seen 79 to 83 days before collection (Defender reports them as Inactive). 2 were seen on the collection day but first seen only 1 day before it; they may not have been assessed yet (inferred, not confirmed).
- **Scope:** 5 of 16 onboarded devices (31%). Last seen before data collection: 3 more than 60 days.
- **Overlap:** The 3 inactive devices are also in finding 5.
- **Why it matters:** Findings 1 to 3 cover only assessed devices; these 5 are not in them.
- **Based on:** Onboarded devices compared with Microsoft Defender's software and vulnerability assessment, counted once per device.
- **Next step:** Check the 2 recently onboarded devices in Defender for assessment status, and confirm whether the 3 inactive devices are still in use.
- **Confidence:** Medium.
- **Age mix:** 3 of these 5 devices (60%) were last seen more than 7 days before collection, so their status may be out of date.
- **Affected devices:** 5 devices, oldest last-seen first.

*Device table omitted in this example. In a real briefing it lists each affected device with its OS and release, the users Defender recorded, department, and days since last seen.*

### 5. Devices Not Seen for More Than 7 Days

- **What we found:** 4 onboarded devices were last seen more than 7 days before data collection: 1 at 31 days and 3 at 79 to 83 days. Defender reports all 4 as Inactive. None has a user recorded, and none reports a manufacturer or model.
- **Scope:** 4 of 16 onboarded devices (25%). Last seen before data collection: 4 more than 30 days, 3 more than 60, 0 more than 90.
- **Overlap:** 3 are also in finding 4 (no assessment data). The device last seen 31 days before collection still has assessment data and is in finding 1.
- **Why it matters:** Defender cannot assess or protect what does not report; these devices may be offline, retired, or rebuilt.
- **Based on:** Microsoft Defender's last-seen date for onboarded devices, measured to the data collection time.
- **Next step:** Confirm with the device owners or asset records whether these 4 devices are retired or offline.
- **Confidence:** High.
- **Affected devices:** 4 devices, oldest last-seen first.

*Device table omitted in this example. In a real briefing it lists each affected device with its OS and release, the users Defender recorded, department, and days since last seen.*

### Additional Findings

None: every finding from the completed checks is in the main briefing.

### Not Assessed

- Microsoft Defender Antivirus health, security configuration (including attack surface reduction rules), incidents and alerts, and Secure Score: not part of this Preview.

### Data Notes

- 2 Defender device IDs have assessment data but no device record. They are excluded from every count above. They hold about 23% of active vulnerability records (5,728 of 25,341), and both have critical or exploitable vulnerabilities. They may be earlier IDs of re-onboarded devices (inferred, not confirmed). Report pages that count these records directly show higher totals.
- The BI for Defender report page shows 62.50% of devices with an exploitable vulnerability because it divides by all 16 device records and counts fixed vulnerabilities; this briefing uses the 11 assessed devices and active vulnerabilities only.
- "Listed as missing for more than 30 days" is measured from when Defender first saw the vulnerability on the device, not from the update's release date.

Ask me to exclude devices not seen for more than any number of days you choose, to focus on one OS, or to change the briefing filters.
Ask me to rank by concentration or nearest deadline, or to change the deadline window.
