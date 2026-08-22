#!/usr/bin/env python3
"""Validate public Yeno Journal posts before deployment."""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"

REQUIRED = {
    "layout",
    "title",
    "slug",
    "description",
    "date",
    "author",
    "published",
    "category",
    "noindex",
}

BANNED_TRANSLATIONS = {
    "nilai proposisi": "value proposition",
    "proposisi nilai": "value proposition",
    "value proposisi": "value proposition",
    "halaman arahan": "landing page",
    "corong pemasaran": "marketing funnel or funnel",
    "tingkat konversi": "conversion rate",
    "peta jalan produk": "product roadmap or roadmap",
}

STOPWORDS = {
    "ada", "agar", "akan", "atau", "bagi", "bahwa", "bisa", "dalam", "dan",
    "dari", "dengan", "di", "ini", "itu", "jika", "juga", "karena", "ke",
    "lebih", "maka", "pada", "sebagai", "sebuah", "setelah", "tidak", "untuk",
    "yang", "anda", "kamu", "mereka", "kami", "kita",
}


def parse_post(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError("missing valid YAML front matter")

    front: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = value.strip().strip('"\'')
    return front, match.group(2).strip()


def is_true(value: str) -> bool:
    return value.lower() == "true"


def words(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [token for token in tokens if len(token) > 2 and token not in STOPWORDS]


def cosine(left: list[str], right: list[str]) -> float:
    a, b = Counter(left), Counter(right)
    numerator = sum(count * b.get(term, 0) for term, count in a.items())
    denominator = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
    return numerator / denominator if denominator else 0.0


def jaccard(left: list[str], right: list[str]) -> float:
    a, b = set(left), set(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def main() -> int:
    errors: list[str] = []
    public: list[tuple[Path, dict[str, str], str]] = []

    for path in sorted(POSTS.glob("*.md")):
        try:
            front, body = parse_post(path)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
            continue

        missing = sorted(key for key in REQUIRED if not front.get(key))
        if missing:
            errors.append(f"{path.name}: missing front matter: {', '.join(missing)}")

        if not is_true(front.get("published", "false")) or is_true(front.get("noindex", "false")):
            continue

        public.append((path, front, body))
        lower = body.lower()
        for phrase, preferred in BANNED_TRANSLATIONS.items():
            if phrase in lower:
                errors.append(f"{path.name}: use '{preferred}', not '{phrase}'")

        if front.get("automation") == "daily-journal":
            for field in ("lang", "editorial_track", "topic_key"):
                if not front.get(field):
                    errors.append(f"{path.name}: automated post requires '{field}'")
            if front.get("lang") != "id":
                errors.append(f"{path.name}: automated Journal posts must use lang: id")
            if front.get("editorial_track") not in {"product-management", "digital-marketing"}:
                errors.append(f"{path.name}: invalid editorial_track")
            count = len(words(body))
            if not 700 <= count <= 1600:
                errors.append(f"{path.name}: automated post has {count} substantive words; expected 700–1600")

    for field in ("title", "slug", "topic_key"):
        seen: dict[str, Path] = {}
        for path, front, _ in public:
            value = re.sub(r"\s+", " ", front.get(field, "").strip().lower())
            if not value:
                continue
            if value in seen:
                errors.append(f"{path.name}: duplicate {field} with {seen[value].name}")
            else:
                seen[value] = path

    for index, (path_a, front_a, body_a) in enumerate(public):
        for path_b, front_b, body_b in public[index + 1:]:
            title_score = jaccard(words(front_a.get("title", "")), words(front_b.get("title", "")))
            body_score = cosine(words(body_a), words(body_b))
            if title_score >= 0.78 or body_score >= 0.86:
                errors.append(
                    f"{path_a.name} and {path_b.name}: possible duplicate "
                    f"(title={title_score:.2f}, body={body_score:.2f})"
                )

    if errors:
        print("Journal validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Journal validation passed for {len(public)} public posts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
