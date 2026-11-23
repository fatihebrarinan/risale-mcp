---
name: lesson-plan
description: "Prepare a cited lesson (ders) plan on a topic or a section of the Risale-i Nur - aim, passages to read aloud in order, main points with the sentences they rest on, difficult words, questions for discussion. Use when the user wants to prepare a lesson, a study session or notes for teaching, e.g. \"Yarınki ders için Haşir Risalesi'nden plan hazırla\", \"Gençlere sabır üzerine bir ders hazırla\", \"Ders notu çıkar\", \"Prepare a lesson on the First Word\"."
license: MIT
---

# Lesson plan

Follow the `risale-library` rules.

1. If the subject is a section, read it in full (`read_section`, following `next_cursor`). If it is a topic, find its main passages first (`semantic_search`, `search`) and read them in context.
2. Give the plan as:
   - **Aim:** what the listeners should take away, in one or two sentences.
   - **Passages to read aloud,** in order: each as a block quotation (or, for a long passage, its opening words and the number of sentences) with its source number.
   - **Main points of each passage,** each with the sentence it rests on.
   - **Difficult words** and their meaning in this context. Look them up with `lookup_word` (risaleoku.com's dictionary): give the meaning in your own words, name the dictionary, and keep it out of the Kaynaklar list.
   - **Questions for discussion,** answerable from the passages.
3. Include nothing the text does not support; outside examples or applications go under a separate heading, marked as yours.
4. Call `cite` once with every passage you quote or rely on and finish with the "Kaynaklar" list it returns, unchanged.
