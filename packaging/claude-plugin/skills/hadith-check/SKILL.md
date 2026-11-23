---
name: hadith-check
description: Check a saying presented as a hadith across the Risale MCP libraries - where the Risale-i Nur quotes it and the evidence for it, the reports in the hadith collections and their grades as the books give them - without ruling on it yourself. Use when the user asks whether something is a hadith, where a hadith comes from, or how a hadith in the Risale-i Nur is sourced, e.g. "Bu söz hadis mi?", "Risale'deki bu hadisin kaynağı ne?", "Buharî, Ezân: 148'deki hadis hangisi?", "Is 'the differences of my community are a mercy' a hadith?".
license: MIT
---

# Hadith check

Follow the `risale-library` rules; this skill adds the order of work for a single saying.

1. **In the Risale-i Nur.** If the saying is in the works or the user gives its Arabic, call `find_hadith(text)` on the Risale-i Nur Library: the places it is quoted, `hadith_support` (the evidence: found, partly_found, located_chapter, read_chapter, cited, phrase_found, marked, unsupported), the publisher's references (`cited_in`) and matching reports. If the user gives only Turkish or English words, find the passage first with `semantic_search` or `search`, then read it with `get_passage` to get the Arabic.
2. **In the hadith collections.** On the Hadith Library: `search_hadith` for the Arabic words (or `narrator` for a Companion or narrator in the chain), `semantic_search` for the meaning, `find_by_citation` for a reference such as "Buharî, Ezân: 148" or "Müsned 14870". Results are candidates: read each report you rely on with `get_hadith` (text, chain, printed page, other scholars' layers, places in the Risale-i Nur linked to it).
3. **Evidence, not a verdict.** Never call a report sound, weak or fabricated yourself or from memory. Give grades only as `get_hadith` lists them, with the scholar's name; layers are the notes of other scholars (al-Dhahabi, al-Albani, the editor), named as theirs. A match in a book that collects weak or fabricated reports (`book_note`, e.g. Kashf al-Khafa) means the saying is discussed there, not that it is sound. Not finding a report does not mean it is not a hadith: the author often gives a hadith in his own wording.
4. **Quote exactly.** Arabic exactly as returned, no added vowel marks, in a block quote; then your own translation on its own line, labelled "Yapay zekâ tercümesi:" in Turkish ("AI translation:" in English). Publishers' translations in the works (`publisher_translation`) are not the author's words.
5. **Cite once per connector, one list.** Call `cite` on the Risale-i Nur Library for the sentences you quote, then on the Hadith Library with `first` set to the next number, for the reports. Give one "Kaynaklar" list, in number order, unchanged.

Answer shape: where the saying stands in the Risale-i Nur (quoted, with its evidence); what the collections hold (reports, books, grades with their scholars); what could not be found; your own reading, marked as yours.
