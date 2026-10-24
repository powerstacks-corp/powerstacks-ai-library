# Known Limitations

These apply to the Preview skills. Each skill's own folder lists the limitations specific to its product.

- **Current state only.** The semantic models hold current state, so the skills don't report trends over time (except where a product stores history, such as Secure Score in BI for Defender).
- **Scale is not risk.** Findings are ranked by how many devices are affected. A small finding can matter more than a large one; the skills say so instead of judging severity for you.
- **The data is only as current as the last refresh.** Every briefing shows when the data was collected. Devices that haven't checked in recently can show out-of-date status, and the briefing calls them out.
- **Defender fields describe Microsoft Defender only.** If you use another antivirus product, Defender protection fields can show as off. The skills don't infer anything about other products.
- **Status colors are defaults.** The 95% and 85% thresholds in presentations and reports are starting points, not a risk assessment. You can change them.
- **AI assistants vary.** Results depend on the assistant and model you use. Check important findings in the BI for Intune or BI for Defender reports before you act on them.
- **Large tenants.** A full briefing runs many queries. In very large tenants it can take several minutes.
