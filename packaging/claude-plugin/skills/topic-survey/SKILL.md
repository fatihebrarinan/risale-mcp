---
name: topic-survey
description: Survey where a topic is treated across Bediüzzaman Said Nursî's works, grouped by work, with citations, marking the central treatments. Use when the user asks where or in which treatises a topic appears, or wants an overview of all the passages on a subject rather than one answer, e.g. "Risale-i Nur'da şefkat nerelerde geçiyor?", "Haşir hangi risalelerde anlatılıyor?", "Konu taraması: tevekkül", "Where does Bediüzzaman write about patience?".
license: MIT
---

# Topic survey

Follow the `risale-library` rules. If the user limits the survey (a work, a group of works), keep to that limit.

1. **Find the passages** on the Risale-i Nur Library. `semantic_search` with the topic as a concept and as a question: its `sections` show where the topic concentrates. `search` for the text's own terms: Ottoman and modern spellings, word beginnings with `*` (`haşr*`); `by_work` shows the spread across the works. Search more than once.
2. **Read before listing.** For the main passages read enough context (`get_passage` with context, or `read_section`) to be sure the passage is really about the topic, not a passing mention. When a passage sends the reader to another place for this topic ("tafsilen", "müracaat et"), read that place too.
3. **Report by work, in the works' order:** for each place, one sentence on what is said there, with a short quotation where it helps, ending with its source number. Mark the central treatments (where the topic is the section's subject) apart from the passing ones.
4. **End with the gaps:** what you could not find, what remains uncertain, which searches you made.
5. **Cite:** call `cite` once with every place you list (and the exact words of every quotation) and finish with the "Kaynaklar" list it returns, unchanged. A survey can be long: if it would exceed what is useful, give the central treatments fully and list the rest briefly.
