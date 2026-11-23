"""Claude eklentisi (S4.7): kaynaklar üretilebiliyor mu, proje talimatı değişince eklenti geride kalıyor mu."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("claude_plugin", ROOT / "scripts" / "claude-plugin.py")
plugin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plugin)


def test_files_build_and_validate():
    files = plugin.files()            # yer tutucular, üst bilgi, README ve boyutlar validate() ile denetlenir
    main = files["skills/risale-library/SKILL.md"].decode()
    assert "Answer every question about the Risale-i Nur with the tools of the Risale-i Nur Library connector." in main
    assert "### Citations and quotations" in main
    servers = json.loads(files[".mcp.json"])["mcpServers"]
    assert set(servers) == set(plugin.SERVERS)
    assert all(s["type"] == "http" and s["url"].startswith("https://") for s in servers.values())


def test_skill_names_are_unique_and_referenced():
    files = plugin.files()
    skills = {p.split("/")[1] for p in files if p.startswith("skills/")}
    readme = files["README.md"].decode()
    assert all(f"`{s}`" in readme for s in skills), "README her skill'i anmalı"
    for prompt in json.loads(plugin.PROMPTS.read_text()):
        assert set(prompt["expect"]) <= skills
