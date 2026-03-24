from __future__ import annotations

import re


def split_sentences(text: str) -> list[tuple[str, int, int]]:
    sentences: list[tuple[str, int, int]] = []
    for match in re.finditer(r"[^.!?]+[.!?]?", text):
        sentence = match.group(0).strip()
        if sentence:
            sentences.append((sentence, match.start(), match.end()))
    return sentences


def best_sentence_span(text: str, subject: str, obj: str) -> tuple[str, int, int]:
    sentences = split_sentences(text)
    fallback_end = min(len(text), 200)
    fallback = (text[:fallback_end], 0, fallback_end)
    if not sentences:
        return fallback

    subject_l = subject.lower()
    object_l = obj.lower()
    for sentence, start, end in sentences:
        lower = sentence.lower()
        if subject_l in lower and object_l in lower:
            return sentence, start, end

    for sentence, start, end in sentences:
        lower = sentence.lower()
        if subject_l in lower or object_l in lower:
            return sentence, start, end

    return sentences[0]
