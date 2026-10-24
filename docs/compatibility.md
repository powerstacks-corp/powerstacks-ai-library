# Compatibility

This page lists what each Preview skill was tested with. Any AI assistant and connection that meet the requirements in the [getting started guide](getting-started.md) can work, but PowerStacks tests only the configurations listed here.

## Tested Configuration

| Item | Tested with |
| --- | --- |
| Connection | Microsoft Power BI MCP server (`https://api.fabric.microsoft.com/v1/mcp/powerbi`), signed in with a Microsoft Entra work account |
| AI assistant | A desktop AI assistant on Windows 11 that loads skill folders and connects to remote MCP servers |
| Python (presentations and reports) | Python 3.14 with `python-pptx` 1.0.2 |
| Presentation viewer | Microsoft PowerPoint for Windows |
| HTML report viewer | Chromium-based browsers, light and dark mode, desktop and phone widths |

## Skills

| Skill | Version | Product version tested | Test data |
| --- | --- | --- | --- |
| Endpoint Operations Analyst | 0.12.0-preview | BI for Intune version 70 | PowerStacks demo environment, 2026-10-23; quick questions, PowerStacks test environment, 2026-10-24 |
| Security Operations Analyst | 0.2.0-preview | BI for Defender version 15 | PowerStacks demo environment, 2026-10-23; quick questions, PowerStacks test environment, 2026-10-24 |

The semantic models don't expose their version, so each skill checks at the start of every run that the tables and columns it needs exist. That check confirms the structure, not the meaning of every value. If you run an older product version, update it before you report a problem.
