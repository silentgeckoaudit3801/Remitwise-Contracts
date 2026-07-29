from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
JUSTFILE = REPO_ROOT / "justfile"


def test_test_one_recipe_runs_workspace_cargo_test_with_pattern():
    text = JUSTFILE.read_text(encoding="utf-8")

    assert "test-one pattern:" in text
    assert 'cargo test --workspace "{{pattern}}"' in text


def test_test_one_recipe_rejects_empty_pattern_before_cargo():
    text = JUSTFILE.read_text(encoding="utf-8")
    recipe = text.split("test-one pattern:", 1)[1]

    assert 'test -n "{{pattern}}"' in recipe
    assert "usage: just test-one <pattern>" in recipe
    assert "exit 64" in recipe
