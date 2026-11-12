"""Üç bölümlü eser listeleri: elle tutulan (b) ve (c) yeniden üretimde korunur (PLANLAR.md E1)."""

from risale_mcp.checklist import MANUAL_DEFAULT, MANUAL_MARK, write_parted


def test_new_file_gets_skeleton(tmp_path):
    path = tmp_path / "x.md"
    write_parted(path, "# Liste\n")
    assert path.read_text(encoding="utf-8") == f"# Liste\n\n{MANUAL_MARK}\n\n{MANUAL_DEFAULT}"


def test_manual_part_survives(tmp_path):
    path = tmp_path / "x.md"
    path.write_text(f"# Eski\n\n{MANUAL_MARK}\n\n## (b) Elle\n- bir eser\n", encoding="utf-8")
    write_parted(path, "# Yeni\n")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Yeni\n") and "# Eski" not in text
    assert text.endswith("## (b) Elle\n- bir eser\n") and text.count(MANUAL_MARK) == 1
    write_parted(path, "# Yeni\n")   # yeniden üretim boş satır biriktirmez
    assert path.read_text(encoding="utf-8") == text
