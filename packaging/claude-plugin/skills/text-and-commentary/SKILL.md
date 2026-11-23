---
name: text-and-commentary
description: Answer a question about the Risale-i Nur in two clearly separated parts - what the text says (quoted, cited) and interpretation (yours, or several perspectives, each tied to the sentences it rests on). Use when the user asks for an interpretation, an explanation of meaning, a comparison of readings or a personal application, e.g. "Bu cümleden ne anlamalıyız?", "Farklı bakış açılarıyla yorumla", "Bu temsil bugün bize ne söyler?", "How should this passage be understood?".
license: MIT
---

# Text and commentary

Follow the `risale-library` rules. Search and read the passages first; then answer under two headings, in the user's language (in Turkish "Metin ne diyor" and "Yorum").

## What the text says

Only what the works say: block quotations copied exactly from the sentences you read, and close paraphrases, each ending with its source number. Include the author's own explanation ("Yani, …") as text. Publishers' translations of verses and hadiths are not the author's words.

## Interpretation

Your interpretation and synthesis, clearly marked as yours. Tie each point to the quotations above by their numbers. If readings differ, give each reading with the sentences it rests on and say where the text leaves the question open. Outside material (history, other authors, today's terms) belongs here, named as outside the works. Never present anything that does not rest on the text as if it were the text, and never call your own explanation a tafsir.

Before writing, call `cite` once with every sentence or range you quote or rely on and finish with the "Kaynaklar" list it returns, unchanged.
