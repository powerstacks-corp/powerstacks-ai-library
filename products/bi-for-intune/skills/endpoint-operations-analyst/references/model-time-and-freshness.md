# Time and Freshness

Status: draft. Not validated. Written for BI for Intune version 69.

## Establish Freshness First

Run these before any analysis and report the results at the top of the answer:

```dax
EVALUATE ROW(
    "Data collection time (UTC)", MAX ( Authorization[Refresh Time] ),
    "Latest device check-in", MAX ( Device[Last Check-In] ),
    "Query time (UTC)", UTCNOW ()
)
```

- `Authorization[Refresh Time]` is the time the data was collected, in **UTC**. Present it as UTC (or convert it for the user and say so).
- Times in the model are UTC. The latest device check-in can be later than the refresh time, because collection continues after the refresh time is recorded. The refresh time is recorded during the refresh, not at its end, so the data is a snapshot taken over the refresh window, not at one instant. Do not report later check-ins as an anomaly. **[Needs confirmation]**
- If the latest device check-in is much older than the refresh time, data collection may have stalled. Report it.
- If the refresh time is more than a day before the question time, say so, because `(Days)` columns have not advanced since the refresh.

## Time Columns by Meaning

| Meaning | Examples |
| --- | --- |
| Data collection (UTC) | `Authorization[Refresh Time]` |
| Device last contact | `Device[Last Check-In]`, `Device[Last Check-In (Days)]` |
| Status report time | `Configuration State[Last Status Configuration]`, `Proactive Remediation State[Last Status Update]`, `Script State[Last Update]`, `Windows Update Ring State[Last Status Update Ring]` |
| Scan time | `Device[Last WU Scan]`, `Windows Protection[Last Full Scan]`, `[Last Quick Scan]`, `Windows Feature Update State[Last Scan]` |
| User activity | `User Devices[Last Logon]`, `User[Last Successful Sign-In]` |
| Event time | `Device Enrollment Failure[Enrollment Failure Time]`, `Device Timeline Event[Event Time]` |
| Lifecycle | `Device[Enrolled Date]`, `Device Warranty[Warranty End Date]`, `Device[OS Feature Update EOS Date]` |
| Connector state | `Connector & Token[Last Sync]`, `[Expiration Date]` |

## Day-Count Columns

- `(Days)` columns are calculated at refresh as whole days.
- BLANK compares as 0. Filter with `NOT ISBLANK(...)` before `<=` comparisons.

## History

- Status tables are current state. No snapshots are kept, so no trend can be computed from them.
- Event tables cover limited windows. Check `MIN` and `MAX` of the time column before describing any period, and describe only the period actually covered.

## Refresh History Check (Optional)

When the AI has read-only access to the Power BI REST API for this dataset, compare the latest refresh's duration with recent refreshes.

**Source.** `GET https://api.powerbi.com/v1.0/myorg/groups/{workspaceId}/datasets/{datasetId}/refreshes` (read-only; scope `Dataset.Read.All`). Microsoft documents that the caller must also have Write permission on the dataset, so many users will not have access. The service returns the last 60 entries by default.

**What the timestamps measure** (Microsoft's REST reference, checked 2026-10-09):

- `startTime` and `endTime` are "the start date and time of the refresh" and "the end date and time of the refresh (may be empty if a refresh is in progress)", in UTC. They span the whole refresh request.
- `refreshAttempts` lists each attempt inside it: `Data` (loading data into the model) and `Query` (refreshing premium query caches and dashboard tiles), and any automatic retries after a failure.
- `status`: `Completed` (successfully completed), `Failed` (with `serviceExceptionJson`), `Unknown` (in progress or completion state unknown), `Disabled`.
- **Caveat:** duration = `endTime` minus `startTime` of the refresh, so it includes every attempt (retries and the query-cache step), not only the data load. Microsoft's reference does not say whether time spent waiting for capacity is included; PowerStacks has confirmed it is, so a long duration can come from a busy capacity rather than from BI for Intune's data sources.

**Method.**

1. The assessed refresh is the most recent refresh with status `Completed` (the data in the model comes from it). If a later refresh is in progress (`Unknown`) or `Failed`, say so in plain English; a failed refresh is reported from its status, not from its duration.
2. Baseline: the previous `RefreshBaselineCount` (default 10) refreshes with status `Completed` that started before the assessed refresh. The assessed refresh is never part of its own baseline.
3. If the baseline has fewer than `RefreshBaselineMinimum` (default 5) refreshes, report "insufficient history" with the number available, and do not assess duration.
4. Otherwise flag the assessed refresh when its duration is greater than `RefreshDurationMultiplier` (default 2) times the baseline median.

**Details (implementation choices, Needs confirmation).**

- Order refreshes by `startTime`, newest first; do not rely on the API's order.
- `Unknown` with no `endTime` is in progress; `Unknown` with an `endTime` has an unknown completion state. Neither is assessed or used in the baseline; mention the newest one if it is newer than the assessed refresh.
- The baseline is the 10 most recent `Completed` refreshes that started before the assessed refresh, skipping other statuses (so failures do not shrink it).
- Compare unrounded durations; "greater than" is strict (exactly twice the median is not flagged). Show minutes to one decimal place.
- HTTP 401 or 403 means no access ("could not be checked (no access)"); any other error means "could not be checked (service error)".

**Reporting.** When flagged: "The latest data refresh took <n> minutes, unusually long compared with recent refreshes (median <m> minutes over the previous <k> completed refreshes)." Always show the actual duration, the baseline median, and the sample size. Never infer missing or incomplete data from duration alone; completeness is judged only by the missing-data checks (model foundation, section 7). When access is not available, say once that refresh history could not be checked and continue.
