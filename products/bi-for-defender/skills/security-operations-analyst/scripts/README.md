# Executive Outputs

Status: Preview 0.2.0.

Turns a briefing produced by a PowerStacks skill into an executive presentation and an interactive HTML report. The generators do not query the semantic model. They only lay out figures that the skill already produced, so every number in the outputs comes from the briefing.

## Files

| File | Purpose |
| --- | --- |
| [executive-data.schema.json](executive-data.schema.json) | The briefing data file both generators read |
| [build_deck.py](build_deck.py) | Builds a .pptx presentation with native, editable charts |
| [build_report.py](build_report.py) | Builds a single self-contained HTML report (snapshot) |
| [serve_report.py](serve_report.py) | Previews the report at `http://127.0.0.1` on this computer only (serves the one file) |
| [make_template.py](make_template.py) | Regenerates the default presentation template |
| [templates/powerstacks-executive.pptx](templates/powerstacks-executive.pptx) | Default PowerStacks presentation template: near-black background, indigo title bar, slate cards, status colors |
| [templates/report-template.html](templates/report-template.html) | HTML report template |
| [templates/powerstacks-logo.png](templates/powerstacks-logo.png) | Logo used in the report header |

## Requirements

- Python 3.9 or later.
- The presentation generator needs the `python-pptx` package. The report generator and preview server use only the Python standard library.

## Presentation

Run the commands from the skill folder (the folder that contains SKILL.md), and point `--data` and `--out` at full paths in your working folder (for example a Briefings folder in Documents). Don't save outputs in the skills folder.

```
python scripts/build_deck.py --data briefing.json --out briefing.pptx
python scripts/build_deck.py --data briefing.json --out briefing.pptx --template customer-template.pptx
```

- Default: the PowerStacks template.
- Customer template (.pptx or .potx): if it contains the shape names used by the PowerStacks template, its slides are filled in (named-shape mode). Otherwise its slide layouts are used and its theme applies (layout mode). Existing slides in a customer template are not kept.
- Charts are native PowerPoint charts with their data embedded, so they can be edited in PowerPoint.

## HTML Report

```
python scripts/build_report.py --data briefing.json --out briefing.html
python scripts/serve_report.py --file briefing.html
```

- One file with the data, charts, and filters embedded. It makes no network requests.
- It is a snapshot. It does not refresh or connect to the model. Ask the skill to regenerate it for newer data.
- The preview server listens on the loopback address only. Production hosting is the customer's choice and is out of scope.
- The report can contain device names, serial numbers, users, and departments. Treat the file like the data it came from.

## Status Colors

Both outputs color each finding by the share of the relevant devices that are not affected: green at or above `thresholds.good` (default 95%), amber from `thresholds.warn` (default 85%) up to that, red below it. The thresholds are shown on the report and can be changed in the data file. A finding without an applicable population gets no color.

## Named Shapes (Template Contract)

A customer template can opt in to named-shape mode by naming shapes as in the PowerStacks template: `presentation_title`, `product`, `audience`, `collection_time`, `scope` (cover); `slide_title`, `source_footer`, `page_number`, `brand_footer` (every slide); `metric_label_0..2`, `metric_value_0..2`, `metric_status_0..2`, `summary`, `summary_caveat`; a table plus `ranking_note`; `main_metric`, `donut_placeholder`, `chart_placeholder`, `narrative_stripe`, `finding_observation`, `finding_implication`, `finding_investigation`, `finding_caveat`; `breakdown_summary`, `breakdown_context`, `breakdown_scope`; a table plus `deadline_window`; `note_title_0..2`, `note_body_0..2`; `investigation`, `supporting_context`, `followup`.
