"""Upload the chatbot to its Hugging Face Space, sending only the files it needs to run.

    python scripts/deploy_space.py            # dry run: list the files that would be uploaded
    python scripts/deploy_space.py --upload   # create the Space (private) if needed and upload

Uses the login from `hf auth login` (a token with write access). The allowlist below is the
only way a file reaches the Space: raw/ (CVs, keys, Q&A log), evals/ and tests/ never do.
API keys are set as Secrets in the Space settings, never uploaded.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPACE_ID = "Kira91/ask-kheirie"


def space_files(root: Path = ROOT) -> dict[str, Path]:
    """Map each path on the Space to its source file. The allowlist."""
    files = {
        "app.py": root / "app.py",
        "README.md": root / "deploy" / "space" / "README.md",
        "requirements.txt": root / "deploy" / "space" / "requirements.txt",
    }
    for path in sorted((root / "src" / "resumebot").glob("*.py")):
        files[f"src/resumebot/{path.name}"] = path
    for path in sorted((root / "corpus" / "approved").glob("*.md")):
        files[f"corpus/approved/{path.name}"] = path
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--upload", action="store_true", help="upload for real (default: dry run)")
    args = parser.parse_args()

    files = space_files()
    for name in files:
        print(name)
    print(f"{len(files)} files for {SPACE_ID}")
    if not args.upload:
        print("Dry run: nothing uploaded. Add --upload to send them.")
        return

    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(SPACE_ID, repo_type="space", space_sdk="gradio", private=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as staging:
        for name, source in files.items():
            target = Path(staging) / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        api.upload_folder(
            repo_id=SPACE_ID,
            repo_type="space",
            folder_path=staging,
            # Remove files deleted locally (a renamed corpus file must not linger online).
            delete_patterns=["src/**", "corpus/**"],
            commit_message="Deploy from scripts/deploy_space.py",
        )
    print(f"Uploaded. Open https://huggingface.co/spaces/{SPACE_ID}")


if __name__ == "__main__":
    sys.exit(main())
