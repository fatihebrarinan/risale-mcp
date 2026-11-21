"""scripts/site-uret.py: Markdown eklemeleri ve taslağın siteye çıkmaması (S9)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_uret", ROOT / "scripts" / "site-uret.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


def test_table_box_and_arabic():
    out = S.markdown(":::kisa\nKısa **cevap**.\n:::\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n> قال الله تعالى\n\nMetin «لا يستحيي» burada.")
    assert '<div class="note box box-kisa">' in out and "<strong>Kısa cevap</strong>" in out
    assert "<th>A</th>" in out and "<td>2</td>" in out
    assert '<blockquote dir="rtl" lang="ar">' in out
    assert '<span lang="ar" dir="rtl">لا يستحيي</span>' in out


def test_heading_ids():
    assert S.markdown("## Neden \"tefsir\" denmiyor") == '<h2 id="neden-tefsir-denmiyor">Neden "tefsir" denmiyor</h2>'


def test_draft_meta(tmp_path):
    p = tmp_path / "2026-01-01-x.md"
    p.write_text("---\nbaslik: X\ntarih: 2026-01-01\nozet: Ö\ndurum: taslak\n---\n\nGövde.\n", encoding="utf-8")
    post = S.read_post(p, S.KINDS["calismalar"])
    assert post.draft and post.preview_path == "/taslak/onizleme/calismalar/2026-01-01-x.html"
    assert "noindex" in S.post_page(post, preview=True)
    assert "noindex" not in S.post_page(post)


def test_set_meta():
    text = "---\nbaslik: X\ntarih: 2026-01-01\ndurum: taslak\n---\n\nGövde.\n"
    new = S._set_meta(S._set_meta(text, "durum", "yayinda"), "tarih", "2026-02-02")
    assert "durum: yayinda" in new and "tarih: 2026-02-02" in new and new.endswith("Gövde.\n")
