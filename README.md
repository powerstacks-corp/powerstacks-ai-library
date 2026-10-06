# PowerStacks AI Library

This repository is where PowerStacks will publish AI resources for its BI products: model context, skills, and prompts that help an AI tool work with the PowerStacks semantic model you already use.

> **Status: early scaffold.** No validated AI release is available yet. Nothing here is ready to install or use. BI for Intune resources are being prepared first.

## What This Repository Is For

PowerStacks BI products include a data model with the relationships, measures, and business logic already built. You never had to learn DAX or build the model yourself. The resources in this library will describe that model to an AI tool so it can answer questions using the same logic the reports use.

## Products

| Product | Status |
| --- | --- |
| [BI for Intune](products/bi-for-intune/README.md) | In preparation. Not released. |
| [BI for Defender](products/bi-for-defender/README.md) | Not released. |
| [BI for SCCM](products/bi-for-sccm/README.md) | Not released. |

Each product will be packaged and versioned on its own, so you only need the resources for the products you own. Resources for customers who use more than one product will live in [cross-product](cross-product/bi-for-intune-and-defender/README.md) and are also not released.

## Repository Layout

| Path | Contents |
| --- | --- |
| [docs/](docs/README.md) | Overview, terminology, getting started, compatibility, known limitations |
| [shared/](shared/README.md) | Common foundation shared by all products |
| [products/](products/bi-for-intune/README.md) | Product-specific model context, skills, prompts, and examples |
| [integrations/](integrations/README.md) | General guidance for connecting an AI tool to your model |
| [cross-product/](cross-product/bi-for-intune-and-defender/README.md) | Resources that span more than one product |
| [manifests/](manifests/README.md) | Package versions, dependencies, and compatibility records |

## Provider Neutrality

The library is written so it isn't tied to any AI provider. Its documentation doesn't name or recommend specific AI products, vendors, or connection services. Connection guidance under [integrations/](integrations/README.md) describes requirements in general terms, and [compatibility](docs/compatibility.md) lists only what has been tested.

## Distribution Terms

Distribution terms for this repository haven't been published yet. They will be added before any substantive resources are released.

## Security

See [SECURITY.md](SECURITY.md) for how to report a security issue.
