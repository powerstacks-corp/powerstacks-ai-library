# Executive Outputs (Reference)

Status: Preview 0.1.0. Written for and tested with the BI for Defender release 15 schema on 2026-10-23. Slide and report wording is provisional and may change in later releases.

Use this when the user asks for an executive presentation, a slide deck, or an HTML report of the briefing. The generators are product-neutral; see the shared [executive outputs package](../scripts/README.md).

## What to Produce

- **Presentation:** a .pptx built with `scripts/build_deck.py`. PowerStacks branding by default. If the user supplies a presentation template (.pptx or .potx), pass it with `--template`; the customer's template overrides the default.
- **HTML report:** one self-contained .html file built with `scripts/build_report.py`. It is a snapshot with interactive charts and filters. It does not connect to the model or refresh itself. To show newer data, run the briefing again and regenerate it.
- **Local preview:** offer `scripts/serve_report.py`, which serves the report at `http://127.0.0.1` on the user's computer only. How to host the report for others is the customer's decision; do not suggest a hosting service.

Produce only what the user asked for. If they ask for "an executive version" without a format, ask which one they want.

## Steps

1. Run the briefing (Steps 0 to 6) with the user's inputs and scope. The executive outputs never use a different population, ranking, or filter from the briefing they come from.
2. Write a briefing data file that follows `executive-data.schema.json`, using only figures and statements from that briefing:
   - `product`: "BI for Defender". `source`: "BI for Defender semantic model".
   - `collectedUtc`: the data collection time as the briefing states it. If the model does not state the time zone, say so in the value (for example "<date> <time> (time as recorded in the model)").
   - `scope`: the population line from the briefing.
   - `title`: include the briefing date (the user's local date), never the UTC date.
   - `summary.metrics` (up to three): onboarded devices, assessed devices with no critical or exploitable vulnerability (count and share of assessed devices), and data age in days. Give a metric a `status` (`good`, `warn`, or `bad`, using the same thresholds) only when it is a share of devices in a good state; omit `status` on counts and on data age.
   - `summary.text`: restate the largest finding and the next source-reported deadline. No trends, no judgments of overall security posture.
   - `summary.caveat`: the most material caveat (for example the data age alert, or devices without assessment data).
   - One `findings` entry per main-briefing finding, in briefing order: `id` (area, for example S2), `title`, `count`, `population` (the finding's applicable population), `share`, `observation`, `implication`, `nextStep`, and `caveat` (last-seen call-out, status age, confidence, age mix).
   - `chart` for every finding: affected devices by days last seen before data collection (0 to 14, 15 to 30, 31 to 60, 61 to 90, over 90).
   - `breakdown` where the briefing has one: severity and exploitability (S2), most widespread KBs (S4), end-of-support products (S5), assessment coverage (S1).
   - `checkIn`: the population and its last-seen bands. The `managed` value is the onboarded device count; the bands are days last seen before data collection. Also set `"title": "Device last seen"`, `"populationLabel": "onboarded devices"`, and `"measureLabel": "days since last seen"`, and set `"devicesDaysLabel": "Last seen (days)"`, so the report uses Defender wording. Leave `serial` out of device rows (the model has no serial numbers); the report hides empty columns.
   - `thresholds` and `thresholdsNote`: `{"good": 95, "warn": 85}` (PowerStacks provisional display defaults) unless the user gives others. `thresholdsNote` says what the colors mean, for example "Colors: green when at least 95% of the relevant devices are not affected, amber from 85%, red below 85%. Display thresholds only, not a security rating or customer policy; change them in the data file." Never describe a color as a judgment of security posture.
   - `deadlines`, `deadlineWindow`, and `deadlineWindowDays` from the Upcoming Deadlines section; an empty list with `deadlinesEmptyText` when there are none.
   - `notes` (up to three): data age and freshness, population and coverage, confidence and limitations (including that this is a Preview with five areas).
   - `next`: the single most useful investigation from the briefing and the closing offer to narrow scope or change ranking.
   - `devices` (HTML report only): exactly the rows of the briefing's "Affected devices" tables, one entry per device per main finding, with `finding` (the finding's `id`), `device`, `user`, `department`, `os`, and `lastCheckInDays` (days last seen before collection), values as stored. The model has no serial number; leave `serial` empty. Each finding's rows are already limited to `DeviceDetailLimit`; when a finding has more devices, say so in `devicesNote`. Do not add device rows that are not in the briefing.
3. Save the data file, the presentation, and the report in the user's current working folder or in a folder the user names (for example `Documents\PowerStacks\Briefings`), never inside the skills folder. Run the generators by their full path in this skill's scripts folder, with full paths for the data and output files:
   ```
   python "<skill folder>/scripts/build_deck.py" --data "<output folder>/briefing.json" --out "<output folder>/briefing.pptx" [--template <file>]
   python "<skill folder>/scripts/build_report.py" --data "<output folder>/briefing.json" --out "<output folder>/briefing.html"
   python "<skill folder>/scripts/serve_report.py" --file "<output folder>/briefing.html"
   ```
   The presentation needs the `python-pptx` package; the report and preview need only Python.
4. Tell the user the full path of each file created, which template was used, the data collection time, the briefing date and time zone, and that both are snapshots to regenerate for newer data. The report labels last-seen age with the generic "check-in" wording; say that for BI for Defender it means days last seen before data collection.

## Rules

- Same analysis rules as the briefing: source values as stated, distinct-device counts, full default population unless the user narrowed it, last-seen context, status age, scope, collection time, applicable denominators, and material caveats.
- Do not add figures that are not in the briefing, and do not round differently from it.
- Do not write executive conclusions, recommendations beyond the briefing's next steps, or trend language.
- The outputs can contain device names and user names. Save them only where the user asks. Do not upload them anywhere.
- Charts must stay native and editable in the presentation. Do not replace them with images.
- If a generator fails (for example `python-pptx` is not installed), say so and offer the briefing text instead. Do not hand-build a presentation another way.
