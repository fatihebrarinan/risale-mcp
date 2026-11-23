---
name: self-test
description: Quiz the user on a section of the Risale-i Nur, one question at a time, checking each answer against the text and quoting the sentence that settles it. Use when the user wants to be tested or to check their understanding of a treatise or section, e.g. "Onuncu Söz'den beni sına", "Bana Birinci Lem'a'dan soru sor", "Ne kadar anladım, test et", "Quiz me on the Twenty-Third Word".
license: MIT
---

# Self test

Follow the `risale-library` rules.

1. Find the section the user names (`search` for its title returns `matching_sections` with their ids; `get_outline` browses a work) and read it in full with `read_section`, following `next_cursor` until the end. Do not ask about a part you have not read.
2. Ask one question at a time about its arguments, examples, parables and terms, in the order of the text. Mix kinds: what the text says, why it says it, what an example shows, what a term means here.
3. After each answer, check it against the text: say what is right and what is missing, quote the sentence that settles it, then ask the next question. Do not reveal answers before the user tries.
4. When a reply quotes the works, call `cite` for its quotations and end it with the "Kaynaklar" list, unchanged.
5. At the end (or when the user stops), summarize: what the user knows well, and which passages to reread, with their sources.
