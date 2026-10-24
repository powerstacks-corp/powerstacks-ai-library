# Security

## Reporting a Security Issue

Please don't report security issues in public GitHub issues, discussions, or pull requests.

To report an issue privately, go to this repository's **Security** tab and select **Report a vulnerability**, or email support@powerstacks.com. Reports are visible only to PowerStacks.

## What Not to Include

Don't post credentials, access tokens, tenant identifiers, customer data, or exports from your environment anywhere in this repository, including in issues. If you need to show an example, remove or replace identifying values first.

## How the Skills Handle Data

- The skills run inside the AI assistant you choose and query your semantic model with your own permissions. PowerStacks doesn't receive your data.
- Queries are read-only DAX queries. The skills never change your semantic model, Intune, or Microsoft Defender.
- The skills never read connection credentials stored in the semantic model's parameters.
- Your AI assistant's provider processes the prompts and query results under your agreement with that provider.
- Generated presentations and HTML reports can contain device names, serial numbers, and user names. Store and share them like the data they came from.
