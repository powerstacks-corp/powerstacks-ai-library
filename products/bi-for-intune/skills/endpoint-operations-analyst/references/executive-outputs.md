# Executive Outputs (Reference)

Status: Preview 0.11.0. Written for BI for Intune version 69 and tested with version 70 on 2026-10-23.

Use this when the user asks for an executive presentation, a slide deck, or an HTML report of the briefing.

## What to Produce

- **Presentation:** a .pptx built with `build_deck.py` from the scripts folder in this skill. PowerStacks branding by default. If the user supplies a presentation template (.pptx or .potx), pass it with `--template`; the customer's template overrides the default.
- **HTML report:** one self-contained .html file built with `build_report.py` from the scripts folder in this skill. It is a snapshot with interactive charts and filters. It does not connect to the model or refresh itself. To show newer data, run the briefing again and regenerate it.
- **Local preview:** offer `serve_report.py`, which serves the report at `http://127.0.0.1` on the user's computer only. How to host the report for others is the customer's decision; do not suggest a hosting service.

Produce only what the user asked for. If they ask for "an executive version" without a format, ask which one they want.

## Steps

1. Run the briefing (Steps 0 to 6) with the user's inputs and scope. The executive outputs never use a different population, ranking, or filter from the briefing they come from.
2. Write a briefing data file (`briefing.json`) that follows `executive-data.schema.json` in the scripts folder, using only figures and statements from that briefing:
   - `collectedUtc`, `scope`, and `product` exactly as in the briefing header. Collection time stays in UTC.
   - `title`: include the briefing date (the user's local date, skill Step 4a), never the UTC date.
   - `checkIn`: the population line as `managed` (managed devices) and `bands` with device counts for `d0to14`, `d15to30`, `d31to60`, `d61to90`, and `over90` (derive each band from the briefing's over-14, over-30, over-60, and over-90 counts; the bands must add up to `managed`).
   - `thresholds` and `thresholdsNote`: the status-color thresholds. Use `{"good": 95, "warn": 85}` (PowerStacks provisional display defaults) unless the user gives other values. `thresholdsNote` says what the colors mean, for example "Colors: green when at least 95% of the relevant devices are not affected, amber from 85%, red below 85%. Display thresholds only, not a health rating or customer policy; change them in the data file." The colors are a display convention; never describe a color as a judgment of health in any text.
   - `summary.metrics` (up to three): managed devices, number of findings in the briefing, and devices checked in within 14 days (count and share). Give a metric a `status` (`good`, `warn`, or `bad`, using the same thresholds) only when it is a share of devices in a good state, such as devices checked in within 14 days; omit `status` on counts such as managed devices or number of findings.
   - `summary.text`: restate the largest finding and the next source-reported deadline. No trends, no judgments of overall health, no conclusions the briefing does not state.
   - `summary.caveat`: the most material caveat from the briefing (for example the share of devices not checked in for more than 14 days, or a partial data load).
   - `rankingNote`: the Method line's ranking method and filters, including any non-default filter values.
   - One `findings` entry per main-briefing finding, in briefing order: a unique `id` (the analysis area, with a suffix when an area has more than one finding, for example `A7-SU` and `A7-EOS`), `title`, `count`, `population` (null when not established or tenant-level; a finding with a null population gets no color), `share`, `observation` ("What we found"), `implication` ("Why it matters"), `nextStep`, and `caveat` (check-in call-out, status age, confidence, age mix).
   - `chart` for every finding: devices by last check-in band (0 to 14, 15 to 30, 31 to 60, 61 to 90, over 90 days) from the finding's check-in call-out. For records with no Intune check-in (A14a), chart the last Windows Update scan age in the same bands and title the chart "Last Windows Update scan". For a tenant-level finding with no device count (A1), give an empty chart with `emptyText`.
   - `breakdown` where the briefing has one: app type (A5), platform script or remediation package (A6), release and edition (A7), join type (A14b), manufacturer (A14d). Include the briefing's denominator and overlap notes in `context` and `scope`.
   - `deadlines`, `deadlineWindow`, and `deadlineWindowDays` from the Upcoming Deadlines section. Every deadline has `date` (as reported), `what`, `scope`, and `daysRemaining` (whole calendar days from the local briefing date, as in the briefing). Use an empty list with `deadlinesEmptyText` when there are none.
   - `notes` (up to three): population and scope, freshness and coverage, confidence and limitations.
   - `next`: the single most useful investigation from the briefing and the closing offer to narrow scope or change ranking.
   - `devices` (HTML report only): exactly the rows of the briefing's "Affected devices" tables, one entry per device per main finding, with `finding` (the finding's `id`), `device`, `serial`, `user`, `department`, `os`, and `lastCheckInDays` (null for records with no Intune check-in), values as stored. Each finding's rows are already limited to `DeviceDetailLimit`; when a finding has more devices, say so in `devicesNote` (for example "Showing up to 50 devices per finding; ask for the full list."). Do not add device rows that are not in the briefing. When no finding has device rows, omit `devices`.
3. Save the data file, the presentation, and the report in the user's current working folder or in a folder the user names (for example `Documents\PowerStacks\Briefings`), never inside the skills folder. Run the generators by their full path in this skill's scripts folder, with full paths for the data and output files:
   ```
   python "<skill folder>/scripts/build_deck.py" --data "<output folder>/briefing.json" --out "<output folder>/briefing.pptx" [--template <customer template>]
   python "<skill folder>/scripts/build_report.py" --data "<output folder>/briefing.json" --out "<output folder>/briefing.html"
   python "<skill folder>/scripts/serve_report.py" --file "<output folder>/briefing.html"
   ```
   The presentation needs the `python-pptx` package; the report and preview need only Python.
4. Tell the user the full path of each file created, which template was used (PowerStacks default, or the customer's template in named-shape or layout mode), the data collection time (UTC), the briefing date and time zone, and that both are snapshots to regenerate for newer data.

## Rules

- Same analysis rules as the briefing: source values as stated, distinct-device counts, full managed population unless the user narrowed it, check-in context, status age, scope, collection time, applicable denominators, and material caveats.
- Do not add figures that are not in the briefing, and do not round differently from it.
- Do not write executive conclusions, recommendations beyond the briefing's next steps, or trend language.
- The outputs can contain device identifiers and user names. Save them only where the user asks. Do not upload them anywhere.
- Charts must stay native and editable in the presentation. Do not replace them with images.
- If a generator fails (for example `python-pptx` is not installed), say so and offer the briefing text instead. Do not hand-build a presentation another way.
