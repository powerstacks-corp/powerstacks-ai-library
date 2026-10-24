# PowerStacks AI Library

AI skills for PowerStacks BI products. A skill teaches an AI assistant how to read the PowerStacks semantic model you already have, so you can ask for a briefing in plain English and get an answer built from your own data.

> **Preview.** These skills are early versions. They're tested against PowerStacks demo environments, and their results can change between versions. Check important findings in the product reports before you act on them, and tell us what you find.

## Skills

| Skill | Product | What it does | Status |
| --- | --- | --- | --- |
| [Endpoint Operations Analyst](products/bi-for-intune/skills/endpoint-operations-analyst/SKILL.md) | BI for Intune | A daily endpoint briefing: up to five issues to investigate today, ranked by how many devices each affects, with check-in context, device details, Microsoft guidance for app error codes, and next steps. | Preview |
| [Security Operations Analyst](products/bi-for-defender/skills/security-operations-analyst/SKILL.md) | BI for Defender | A security briefing from your Microsoft Defender data: how current the data is and which devices lack assessment data, devices with active critical or exploitable vulnerabilities, missing Microsoft security updates, end-of-support software, and devices not seen recently. | Preview |

Both skills can also turn a briefing into an executive PowerPoint presentation and a one-page interactive HTML report.

## How It Works

1. Your AI assistant loads the skill folder.
2. It connects to your BI for Intune or BI for Defender semantic model through the Microsoft Power BI MCP server, signed in as you.
3. It runs read-only DAX queries, follows the skill's rules for populations, counts, and caveats, and writes the briefing.

The skills don't send your data to PowerStacks, and they never change your semantic model, Intune, or Microsoft Defender.

## Requirements

- BI for Intune or BI for Defender deployed in your Power BI workspace, with a completed data refresh.
- Build permission on that product's semantic model.
- Your Power BI administrator enables the tenant setting **Users can use the Power BI Model Context Protocol server endpoint (preview)**.
- An AI assistant that can load skill folders (`SKILL.md`) and connect to remote MCP servers.
- For presentations and HTML reports only: Python 3.9 or later on the computer that runs the assistant, and the `python-pptx` package for presentations.

## Get Started

Follow the [getting started guide](docs/getting-started.md). In short:

1. Download this repository (clone it or download the ZIP).
2. Copy the skill folder for your product into your AI assistant's skills folder.
3. Add the Microsoft Power BI MCP server to your assistant: `https://api.fabric.microsoft.com/v1/mcp/powerbi`.
4. Copy your semantic model ID from the model's URL in the Power BI service.
5. Ask for a briefing, for example: "Act as my endpoint operations analyst. Use semantic model `<ID>` and give me today's briefing."

## Documentation

- [Getting started](docs/getting-started.md)
- [Compatibility](docs/compatibility.md)
- [Known limitations](docs/known-limitations.md)
- [Changelog](CHANGELOG.md)
- [Security](SECURITY.md)

## Feedback

Open a [GitHub issue](https://github.com/powerstacks-corp/powerstacks-ai-library/issues) for Preview feedback. Don't include tenant data, device names, or user names. For anything private, email support@powerstacks.com.

## License

[MIT](LICENSE), with the exceptions listed in [NOTICE](NOTICE.md).
