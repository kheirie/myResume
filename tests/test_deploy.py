import importlib.util
from pathlib import Path

import gradio

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("deploy_space", ROOT / "scripts" / "deploy_space.py")
deploy_space = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(deploy_space)

FILES = deploy_space.space_files()


def test_space_gets_the_app_its_package_and_every_approved_corpus_file():
    assert {"app.py", "README.md", "requirements.txt"} <= FILES.keys()
    assert "src/resumebot/answering.py" in FILES and "src/resumebot/chat.py" in FILES
    corpus = {f"corpus/approved/{p.name}" for p in (ROOT / "corpus" / "approved").glob("*.md")}
    assert corpus <= FILES.keys()


def test_nothing_private_or_unneeded_reaches_the_space():
    for name, source in FILES.items():
        relative = source.resolve().relative_to(ROOT).as_posix()
        assert not relative.startswith(("raw/", "evals/", "tests/", ".env", "CLAUDE")), relative
        assert "secrets" not in relative


def test_space_runs_the_gradio_version_used_locally():
    readme = FILES["README.md"].read_text(encoding="utf-8")
    assert f"sdk_version: {gradio.__version__}" in readme
    assert "app_file: app.py" in readme
