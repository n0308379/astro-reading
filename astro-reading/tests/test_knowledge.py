from astro_reading.knowledge import InMemoryKnowledgeBase

PASSAGES = [
    "The tenth house describes career, public standing and long-term purpose.",
    "The seventh house describes partnerships, marriage and close relationships.",
    "Mercury governs communication, learning and short journeys across the chart.",
]


def test_returns_best_match_first():
    kb = InMemoryKnowledgeBase(PASSAGES)
    assert kb.search("career and purpose")[0] == PASSAGES[0]


def test_returns_nothing_when_no_word_matches():
    assert InMemoryKnowledgeBase(PASSAGES).search("volcano") == []


def test_respects_limit():
    assert len(InMemoryKnowledgeBase(PASSAGES).search("house chart", limit=1)) == 1


def test_empty_query_returns_nothing():
    assert InMemoryKnowledgeBase(PASSAGES).search("   ") == []


def test_loads_text_files_by_paragraph(tmp_path):
    (tmp_path / "notes.md").write_text(
        f"{PASSAGES[0]}\n\nshort\n\n{PASSAGES[1]}\n", encoding="utf-8"
    )
    (tmp_path / "ignored.pdf").write_bytes(b"%PDF")
    kb = InMemoryKnowledgeBase.from_directory(tmp_path)
    assert len(kb) == 2
