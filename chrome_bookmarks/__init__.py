from pathlib import Path
from shutil import copy
from typing import Optional

from pydantic.tools import parse_file_as
from ._bookmark_system_path import get_chrome_bookmarks_path


from ._models import BookmarksModel, Folder, Bookmark


def load_bookmarks(
    path: Optional[Path] = None, create_backup: bool = True
) -> BookmarksModel:
    if path is None:
        path = get_chrome_bookmarks_path()

    if create_backup:
        copy(path, "bookmarks-backup.json")

    return parse_file_as(BookmarksModel, path, encoding="utf-8")


__all__ = ["load_bookmarks", "BookmarksModel", "Folder", "Bookmark"]
