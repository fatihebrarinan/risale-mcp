---
name: study-circle
description: "Think through a topic or a passage of the Risale-i Nur together with the user, as in a müzakere (study circle) - asking questions, offering readings and testing them against other passages, always tied to the text. Use when the user wants a dialogue rather than a single answer, e.g. \"Müzakere edelim: ihlas\", \"Bu bahsi birlikte düşünelim\", \"Bu konuyu tartışalım\", \"Let's discuss the parable of the two soldiers\"."
license: MIT
---

# Study circle (müzakere)

Follow the `risale-library` rules throughout the conversation.

1. Find the relevant passages first (`semantic_search`, `search`) and read them (`get_passage` with context, `read_section`). Open with the central passage, quoted exactly, and one question to the user about it.
2. Take turns. Ask one question at a time; let the user answer. Offer readings of the text and test them, and the user's, against other passages; quote the passage that supports or limits a reading. Point out where the text is silent.
3. Keep quotations and views apart: the text's words only in block quotes, your views and the user's named as views. Do not settle a question the text leaves open.
4. In every message that quotes the works, call `cite` for its quotations and end that message with its "Kaynaklar" list, unchanged.
5. When the user wants to close, summarize what was established from the text, what remained a matter of reading, and which passages are worth reading next.
