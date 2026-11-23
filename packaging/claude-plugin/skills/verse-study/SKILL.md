---
name: verse-study
description: "Study a Qur'anic verse across the Risale MCP libraries - the verse itself, where the Risale-i Nur quotes it or ties to it, what the classical tafsirs say in the order of their authors' death, and related hadiths or rhetoric when they matter - with one Kaynaklar list. Use when the user asks about a verse or a passage of a sura, e.g. \"Âyetü'l-Kürsî'yi Risale nasıl açıklar?\", \"Bakara 2:255 hakkında müfessirler ne der?\", \"Bu âyet Risale-i Nur'da nerede geçiyor?\", \"What do the tafsirs say about Yasin 36:82?\"."
license: MIT
---

# Verse study

Follow the `risale-library` rules; this skill adds the order of work when one verse (or a short range) is the subject.

1. **The verse.** Call `get_ayah(sura, ayah)` on the Risale-i Nur Library: the vowelled Arabic, the Türkiye Diyanet Vakfı translation (say whose it is, mention `covers_verses`), and how often the works quote it. If the user names the verse by its words or a common name, settle the number first and check the Arabic `get_ayah` returns against what they mean. Never write the Arabic from memory. Give the verse with `get_ayah`'s `ref` ("Bakara Sûresi, 2:255").
2. **The Risale-i Nur first.** Call `find_ayah(sura, ayah)` on the Risale-i Nur Library. It lists the sentences that quote the verse and the places that tie to it (`links`: kind, strength, evidence sentence; strong ones first). Read the places you will use with `get_passage` (with context) or `read_section` before saying anything about them. Name each tie by its kind (işaret, açılış, izah, dayanak, risale) and its evidence; a weak tie is one sentence's reference, not the section's topic. Never call a Risale passage "the tafsir of the verse".
3. **The classical tafsirs.** Call `find_ayah(sura, ayah)` on the Tafsir Library: for each work, in the order of its author's death, the unit that treats the verse and the sentences that quote it. Read the units you use (`read_section`, or `get_passage` for a range). Unless the user asks for all thirteen, choose the few that speak to the question, say which ones you read, and say the others also treat the verse. Quote the Arabic exactly as returned (no added vowel marks), then your own translation on its own line, labelled "Yapay zekâ tercümesi:" in Turkish ("AI translation:" in English). Keep each work apart, with its own citation.
4. **Hadith, when it matters** (occasion of revelation, a report the question names): search the Hadith Library (`search_hadith` for Arabic words, `semantic_search` for meaning) and read the report with `get_hadith`. Give grades only as the book holds them, with the scholar's name.
5. **Rhetoric, when it matters** (a question about the verse's wording, i'jaz, a figure of speech): `find_ayah` on the Classical Islamic Library shows where al-Jurjani, al-Sakkaki and the others quote it; read before citing.
6. **No invented relations.** Two works treating the same verse is not a relation. Never say one work follows, quotes, agrees with or rejects another unless the Tafsir Library's `text_links` records it. A relation you notice is your interpretation: put it under its own heading and quote both ends.
7. **Cite once per connector, one list.** Before writing, call `cite` on each connector you quote from: the first one numbers from 1, each next one with `first` set to the number after the last one used. Give all the lines in one "Kaynaklar" list, in number order, unchanged.

Answer shape (in the user's language): the verse; what the Risale-i Nur says (quoted, cited); what the tafsirs say (each work apart, quoted, cited); hadith or rhetoric if used; your interpretation, clearly marked as yours. Nothing you write is a tafsir; a classical tafsir is.
