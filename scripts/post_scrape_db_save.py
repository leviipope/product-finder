"""Publish the scraped database snapshot to the data branch."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(command: list[str], cwd: Path) -> int:
    result = subprocess.run(command, cwd=cwd)
    return result.returncode


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    source_database = repo_root / "data" / "database.db"

    if not source_database.exists():
        print(f"Missing database file: {source_database}", file=sys.stderr)
        return 1

    worktree_path = Path(tempfile.mkdtemp(prefix="product-finder-data-"))

    try:
        commands = [
            ["git", "fetch", "origin", "data"],
            ["git", "worktree", "add", "--detach", str(worktree_path), "origin/data"],
        ]

        for command in commands:
            if run(command, repo_root) != 0:
                return 1

        target_database = worktree_path / "data" / "database.db"
        target_database.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_database, target_database)

        commands = [
            ["git", "add", "data/database.db"],
            ["git", "diff", "--cached", "--quiet"],
        ]

        if run(commands[0], worktree_path) != 0:
            return 1

        if run(commands[1], worktree_path) == 0:
            print("No database changes to commit.")
            return 0

        commit_message = f"Update database snapshot {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if run(["git", "commit", "-m", commit_message], worktree_path) != 0:
            return 1

        if run(["git", "push", "origin", "HEAD:data"], worktree_path) != 0:
            return 1

        print("Database snapshot published to data branch.")
        return 0
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree_path)], cwd=repo_root)


if __name__ == "__main__":
    raise SystemExit(main())