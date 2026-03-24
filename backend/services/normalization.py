from __future__ import annotations

import re
import string


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_harmless_punctuation(value: str) -> str:
    punctuation = ''.join(ch for ch in string.punctuation if ch not in "-_/:")
    return value.strip().strip(punctuation)


def normalize_for_matching(value: str, lowercase: bool = True, strip_punctuation: bool = True) -> str:
    normalized = normalize_whitespace(value)
    if strip_punctuation:
        normalized = strip_harmless_punctuation(normalized)
    if lowercase:
        normalized = normalized.lower()
    return normalized


def triple_key(subject: str, relation: str, obj: str, relaxed: bool = False) -> str:
    if relaxed:
        subject = normalize_for_matching(subject)
        relation = normalize_for_matching(relation)
        obj = normalize_for_matching(obj)
    return f"{subject}|||{relation}|||{obj}"
