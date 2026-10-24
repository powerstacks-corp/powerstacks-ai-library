"""Build an interactive HTML report (a snapshot) from a briefing data file.

Usage:
    python build_report.py --data briefing.json --out briefing.html

The output is one self-contained HTML file: the data, charts, filters, and
logo are embedded, and the page makes no network requests. It does not
refresh itself. To see newer data, ask the skill to regenerate the report.
Uses only the Python standard library.
"""

import argparse
import base64
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "templates", "report-template.html")
LOGO = os.path.join(HERE, "templates", "powerstacks-logo.png")


def embed_json(data):
    """Serialize for a <script type="application/json"> block safely."""
    text = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    return text.replace("</", "<\\/").replace("<!--", "<\\!--")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", required=True, help="Briefing data file (JSON)")
    ap.add_argument("--out", required=True, help="Output .html path")
    ap.add_argument("--logo", default=LOGO, help="PNG logo for the header (default: PowerStacks)")
    args = ap.parse_args(argv)

    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)
    for key in ("title", "collectedUtc", "scope", "findings"):
        if key not in data:
            sys.exit(f"Data file is missing required field '{key}'.")
    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    with open(args.logo, "rb") as f:
        logo = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

    page = page.replace("{{TITLE}}", html.escape(data["title"]))
    page = page.replace("{{LOGO_DATA_URI}}", logo)
    page = page.replace("{{DATA_JSON}}", embed_json(data))
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"Wrote {args.out} ({len(data['findings'])} findings, {len(data.get('devices', []))} devices)")


if __name__ == "__main__":
    main()
