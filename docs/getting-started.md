# Getting Started

This guide sets up a PowerStacks AI skill and runs your first briefing. It takes about 15 minutes once the prerequisites are in place.

## Before You Begin

You need:

- **A PowerStacks BI product with data.** BI for Intune or BI for Defender deployed in a Power BI workspace, with at least one completed data refresh.
- **Build permission** on that product's semantic model (`bi_for_intune` or `bi_for_defender`).
- **The Power BI MCP tenant setting.** A Power BI administrator turns on **Users can use the Power BI Model Context Protocol server endpoint (preview)** in the Power BI admin portal, under **Tenant settings**.
- **An AI assistant** that can load skill folders (`SKILL.md`) and connect to remote MCP servers. Check your assistant's documentation for where skill folders go and how to add an MCP server.
- **Optional, for presentations and HTML reports:** Python 3.9 or later on the same computer as the assistant. For presentations, also install the `python-pptx` package:

  ```
  python -m pip install python-pptx
  ```

## Step 1: Download the Skills

Clone this repository or download it as a ZIP file:

```
git clone https://github.com/powerstacks-corp/powerstacks-ai-library.git
```

## Step 2: Install the Skill Folder

Copy the folder for your product into your AI assistant's skills folder. Copy the whole folder; the skill uses the files inside it.

| Product | Folder to copy |
| --- | --- |
| BI for Intune | `products/bi-for-intune/skills/endpoint-operations-analyst` |
| BI for Defender | `products/bi-for-defender/skills/security-operations-analyst` |

If you own both products, install both folders.

## Step 3: Connect the Power BI MCP Server

Add the Microsoft Power BI MCP server to your AI assistant as a remote (HTTP) MCP server:

```
https://api.fabric.microsoft.com/v1/mcp/powerbi
```

When the assistant first uses the server, sign in with your Microsoft Entra work account. Queries run with your permissions, and row-level security applies. For details, see Microsoft's article [Power BI Consumption MCP server](https://learn.microsoft.com/power-bi/developer/mcp/remote-mcp-server-get-started).

## Step 4: Find Your Semantic Model ID

1. Sign in to the [Power BI service](https://app.powerbi.com).
2. Open the workspace that contains BI for Intune or BI for Defender.
3. Select the semantic model (`bi_for_intune` or `bi_for_defender`).
4. Copy the ID from the URL. It's the GUID after `/datasets/` or `/modeling/`, depending on the page you open:

   ```
   https://app.powerbi.com/groups/{workspaceId}/datasets/{semanticModelId}
   https://app.powerbi.com/groups/{workspaceId}/modeling/{semanticModelId}/modelView
   ```

## Step 5: Ask for Your First Briefing

Start a new conversation and ask:

- BI for Intune: "Act as my endpoint operations analyst. Use semantic model `<ID>` and give me the five things my team should investigate this morning."
- BI for Defender: "Act as my security operations analyst. Use semantic model `<ID>` and give me today's security briefing."

The assistant saves any files it creates (briefing data, presentation, report) in your working folder or a folder you name, not in the skills folder. The skill first checks that the model has the tables and columns it needs. If something is missing, it tells you which data it couldn't assess instead of guessing.

## Step 6: Narrow or Rerank (Optional)

You can follow up in plain English, for example:

- "Only include devices that checked in within the last 30 days."
- "Show me just the Windows devices."
- "Rank by security relevance instead."
- "List the devices behind the second finding, with serial numbers and users."

## Step 7: Create an Executive Presentation or HTML Report (Optional)

Ask: "Turn this briefing into an executive presentation and an HTML report."

- **Presentation:** a PowerPoint file in the PowerStacks design, with editable charts. To use your own design, give the assistant your template file (.pptx or .potx) and ask it to use that template.
- **HTML report:** one self-contained file with status tiles, charts, and filters. It's a snapshot; ask again to regenerate it with newer data. To preview it, ask the assistant to open it locally. The preview runs only on your computer.
- **Status colors:** each finding is green when at least 95% of the relevant devices are not affected, amber from 85% to 95%, and red below 85%. These are starting defaults, not a judgment of risk. Ask the assistant to use different thresholds if they don't fit your environment.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The assistant can't find the MCP tools | The Power BI MCP server is added and connected in your assistant. |
| Sign-in or permission errors | The tenant setting is on, and you have Build permission on the semantic model. |
| "Missing columns" at the start of a briefing | Update BI for Intune or BI for Defender to the latest version, then refresh the data. |
| Old data in the briefing | Check the semantic model's refresh history in the Power BI service. The briefing always shows when the data was collected. |
| Presentation fails | Python 3.9 or later and `python-pptx` are installed on the computer that runs the assistant. |
