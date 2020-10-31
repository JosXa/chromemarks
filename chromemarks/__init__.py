import os
from pathlib import Path
from shutil import copy
from typing import Optional

from pydantic.tools import parse_file_as
from .chrome_system_paths import get_chromemarks_path


from .models import BookmarksModel, Folder, Bookmark


def load_bookmarks(
    path: Optional[Path] = None,
    create_backup: bool = True,
    backup_path: Path = Path(os.getcwd(), "bookmarks-backup.json"),
) -> BookmarksModel:
    """Loads bookmarks from the specified `path` or from the standard system location.

    Args:
        path: Path to load bookmarks from. Defaults to None, meaning that it's determined automatically.
        create_backup: Whether to create a backup of the bookmarks json file at the specified `backup_path`. Defaults to True.
        backup_path: The path to create packups at. Defaults to a `bookmarks-backup.json` file in the current working directory.

    Returns:
        BookmarksModel: A pydantic model with the bookmarks as object hierarchy under the `roots` attribute.
    """
    if path is None:
        path = get_chromemarks_path()

    if create_backup:
        copy(path, backup_path)

    return parse_file_as(BookmarksModel, path, encoding="utf-8")


__all__ = ["load_bookmarks", "BookmarksModel", "Folder", "Bookmark"]
