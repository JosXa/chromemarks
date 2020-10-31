from datetime import datetime, timezone
from pathlib import Path
import pytest
from chrome_bookmarks import load_bookmarks, BookmarksModel, Bookmark


@pytest.fixture(scope="function")
def bm() -> BookmarksModel:
    skeleton_path = Path(__file__).parent / "data" / "skeleton.json"
    return load_bookmarks(skeleton_path, create_backup=False)


def test_skeleton(bm: BookmarksModel) -> None:
    roots = bm.roots
    assert roots.bookmark_bar
    assert roots.other
    assert roots.synced

    assert (
        roots.bookmark_bar.date_added
        == datetime(2020, 6, 22, 15, 59, 9, 575355, tzinfo=timezone.utc).astimezone()
    )


def test_find_bookmark(bm: BookmarksModel) -> None:
    it = Bookmark(
        date_added=13237315149575355,
        date_modified=None,
        guid="abc",
        id="kek",
        name="Kektus",
        type="url",
        url="https://lala.com",
    )
    bm.roots.bookmarks_bar.children.append(it)

    res = bm.find_bookmark(lambda bm: bm.name == it.name)

    assert res is not None
    assert res.json() == it.json()