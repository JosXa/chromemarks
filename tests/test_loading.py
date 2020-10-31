from datetime import datetime, timezone
import os
from pathlib import Path
import pytest
from chromemarks import load_bookmarks, BookmarksModel, Bookmark


def test_full() -> None:
    full_path = Path(__file__).parent / "data" / "full.json"
    bm = load_bookmarks(full_path, create_backup=False)
    for b in bm.iter_bookmarks():
        assert b.name is not None


def test_create_backup_creates_backup() -> None:
    load_bookmarks(Path(__file__).parent / "data" / "full.json", create_backup=True)
    backup_path = Path(os.getcwd(), Path("bookmarks-backup.json"))
    assert backup_path.exists()


def test_create_backup_false_creates_no_backup() -> None:
    backup_path = Path(os.getcwd(), Path("bookmarks-backup.json"))
    backup_path.unlink()

    load_bookmarks(Path(__file__).parent / "data" / "full.json", create_backup=False)

    assert not backup_path.exists()