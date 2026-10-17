import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def names(requirements):
    return {re.split(r"[<>=!~ ]", r.strip(), maxsplit=1)[0].lower() for r in requirements if r.strip()}


def test_host_requirements_cover_every_project_dependency():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    needed = names(project["dependencies"]) | names(project["optional-dependencies"]["app"])
    lines = [l for l in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    assert needed <= names(lines)
