"""Only use this script if you want to scrape manually."""

from pathlib import Path
import subprocess


def restore_database_from_data_branch(repo_root: Path) -> int:
    commands = [
        ["git", "fetch", "origin", "data"],
        ["git", "restore", "--source", "origin/data", "--", "data/database.db"],
    ]

    for command in commands:
        result = subprocess.run(command, cwd=repo_root)
        if result.returncode != 0:
            return result.returncode

    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    scraper_dir = repo_root / "backend" / "scraper"

    restore_result = restore_database_from_data_branch(repo_root)
    if restore_result != 0:
        return restore_result

    command = [
        "uv",
        "run",
        "--with",
        "scrapy",
        "--with",
        "itemadapter",
        "scrapy",
        "crawl",
        "hardver",
    ]

    result = subprocess.run(command, cwd=scraper_dir)

    print("\033[91m\033[1mAfter the scrape, run python scripts/post_scrape_db_save.py to publish data/database.db to the data branch.\033[0m")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())