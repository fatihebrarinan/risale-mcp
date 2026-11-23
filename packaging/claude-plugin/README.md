# Risale-i Nur Library — Claude plugin

This plugin lets Claude answer questions about the works of Bediüzzaman Said Nursî (1878–1960), the Qur'an, the hadith collections, classical tafsir and classical Arabic rhetoric from the texts themselves, with every quotation tied to a sentence the user can find. It bundles the four read-only libraries of [Risale MCP](https://risalemcp.com/en/) and the skills that teach Claude how to search, read, quote and cite them.

The plugin holds no texts: it holds the addresses of the four connectors and instructions. The texts stay on the servers.

## What it contains

**Four connectors** (remote MCP servers, read-only, no account needed):

| Connector | Address | Contents |
|---|---|---|
| Risale-i Nur Library | `https://mcp.risalemcp.com/mcp` | The complete works of Bediüzzaman Said Nursî (the Risale-i Nur Collection, the early works, the compilations, the Hizbs, the works he wrote in Arabic with their Turkish translations, Ottoman volumes), the Qur'an, risaleoku.com's dictionary |
| Hadith Library | `https://hadis.risalemcp.com/mcp` | The Six Books, the Muwatta, Ahmad's Musnad, al-Mustadrak and other collections, with grades where the books hold them |
| Tafsir Library | `https://tefsir.risalemcp.com/mcp` | Thirteen classical works of tafsir, from al-Tabari to al-Alusi, divided into verse units |
| Classical Islamic Library | `https://klasik.risalemcp.com/mcp` | Classical works on rhetoric, language and terms: al-Jurjani, al-Raghib al-Isfahani, al-Sakkaki, al-Sayyid al-Sharif al-Jurjani |

**Skills** (instructions Claude loads when a question calls for them):

| Skill | When it is used |
|---|---|
| `risale-library` | Any question answered from the libraries: search, read before relying, quote exactly, end with a list of sources, keep the text apart from interpretation |
| `verse-study` | A Qur'anic verse studied across the libraries: the verse, the Risale-i Nur's places, the tafsirs in order, hadith and rhetoric when they matter |
| `hadith-check` | A saying presented as a hadith: where the Risale-i Nur quotes it, the evidence, the reports and their grades as the books give them |
| `topic-survey` | Where a topic is treated across the works, grouped by work |
| `text-and-commentary` | "What the text says" and "interpretation" as separate parts, with differing readings tied to the sentences |
| `study-circle` | A müzakere: thinking a topic through together with the user |
| `self-test` | A quiz on a section, each answer checked against the text |
| `lesson-plan` | A cited lesson plan on a topic or a section |

## Installing

**Claude (web, desktop, mobile):** install the plugin from the directory, then open its Connectors tab and connect the libraries you want (the Risale-i Nur Library at least). The skills work with whichever connectors are connected.

**Claude Code:**

```
/plugin marketplace add fatihebrarinan/risale-library-plugin
/plugin install risale-library@risale-library
```

Without the plugin, the connectors can also be added one by one as custom connectors; see <https://risalemcp.com/en/claude.html>.

## Data and privacy

The plugin itself sends nothing and runs no code. When Claude uses a connector's tool, the server receives only that tool's input (a search phrase, a section or sentence id, the words quoted for a citation), never the rest of the conversation. The servers log the time, the connector, the tool, the duration and the error type of each request for 90 days; search phrases, quotations and IP addresses are not logged. For search by meaning (`semantic_search`) the search phrase is sent to Voyage AI to be turned into a vector. Full policy: <https://risalemcp.com/en/privacy.html>. Terms of use: <https://risalemcp.com/en/terms.html>.

## Sources and permissions

The texts are served with the permission of their sources (e-Risale, risaleoku.com, nurpedia.org and others; the Qur'an from the Tanzil Project), on condition that the source is named; Claude's answers name it in their list of sources. Translations of verses and hadiths are the publishers', and anything Claude translates itself is labelled as an AI translation. Nothing Claude writes is presented as tafsir.

## About

Risale MCP is a volunteer, non-commercial, independent project; it is not an official service of any publisher or community. Questions and corrections: destek@risalemcp.com, or <https://risalemcp.com/en/contribute.html>.

The plugin's files are released under the MIT License (see `LICENSE`). The texts on the servers are not part of this repository and are not covered by it.
