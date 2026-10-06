# Overview

> No validated AI release is available yet. This page describes the purpose and structure of the library.

## Why an AI Library

PowerStacks BI products give you a semantic model with relationships, measures, and business logic already built. Until now, the main ways to use that model were the included reports and reports you build yourself in Power BI.

An AI tool connected to the model is another way to use it: you ask a question and get an answer without first building a report. AI tools work better when they understand the model they are querying, so this library will provide that understanding in a form you can reuse.

## What the Library Will Contain

- **Shared foundation.** Common guidance that applies across PowerStacks products, such as how to present results and how to separate findings from inference.
- **Product model context.** A description of each product's model, its terminology, and how its measures are meant to be used.
- **Skills.** Reusable instructions for a specific kind of analysis.
- **Prompts.** Simple, ready-to-use questions or tasks.
- **Examples.** Sample questions with the kind of result you can expect.
- **Integration guides.** Steps for using the library with a specific AI client or connector.

See [Terminology](terminology.md) for definitions.

## How It Is Organized

Core content is written to be provider-neutral, so it isn't tied to a single AI product. Anything specific to an AI client or connector is kept separately in [integrations](../integrations/README.md).

Each PowerStacks product is packaged and versioned on its own. If you only own BI for Intune, you won't need resources for other products.

## Product Status

| Product | Status |
| --- | --- |
| BI for Intune | In preparation. Not released. |
| BI for Defender | Not released. |
| BI for SCCM | Not released. |
