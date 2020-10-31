from pathlib import Path
from typing import Callable, Generator, Iterable, List, Optional, Union
from datetime import datetime, timedelta, timezone

from pydantic import validator
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


def _parse_date(timestamp: str) -> datetime:
    epoch_start = datetime(1601, 1, 1)
    delta = timedelta(microseconds=int(timestamp))
    return (epoch_start + delta).replace(tzinfo=timezone.utc).astimezone()

class MetaInfo:
    last_visited_desktop: str
    last_visited: Optional[str] = None


class Bookmark(BaseModel):
    date_added: datetime
    date_modified: Optional[datetime]
    guid: str
    id_: str = Field(..., alias="id")
    name: str
    type_: str = Field(..., alias="type")
    url: str

    @validator("type_")
    def check_type(cls, v: str) -> str:
        if v != "url":
            raise ValueError("Not a bookmark with URL")
        return v
    
    @validator("date_added", pre=True)
    def parse_date_added(cls, v: Optional[str]):
        return _parse_date(v) if v else None

    @validator("date_modified", pre=True)
    def parse_date_modified(cls, v: Optional[str]):
        return _parse_date(v) if v else None


class Folder(BaseModel):
    children: List[Union["Folder", Bookmark]] = Field(default_factory=list)
    date_added: datetime
    date_modified: Optional[datetime]
    guid: str
    id_: str = Field(..., alias="id")
    name: str
    type_: str = Field(..., alias="type")

    @validator("type_")
    def check_type(cls, v: str) -> str:
        if v != "folder":
            raise ValueError("Not a folder")
        return v

    @validator("date_added", pre=True)
    def parse_date_added(cls, v: Optional[str]):
        return _parse_date(v) if v else None

    @validator("date_modified", pre=True)
    def parse_date_modified(cls, v: Optional[str]):
        return _parse_date(v) if v else None


Folder.update_forward_refs()


def iter_bookmarks(item: Union[Folder, Bookmark]) -> Iterable[Bookmark]:
    if isinstance(item, Folder):
        for i in item.children:
            yield from iter_bookmarks(i)
    else:
        yield item


class Roots(BaseModel):
    other: Folder
    synced: Folder
    bookmarks_bar: Folder = Field(..., alias="bookmark_bar")

    def iter_bookmarks(self) -> Iterable[Bookmark]:
        for category in [self.bookmarks_bar, self.other, self.synced]:
            yield from iter_bookmarks(category)


class BookmarksModel(BaseModel):
    checksum: str
    roots: Roots
    sync_metadata: str
    version: int

    def find_bookmark(self, flt: Callable[[Bookmark], bool]) -> Optional[Bookmark]:
        for bm in self.roots.iter_bookmarks():
            if flt(bm):
                return bm

        return None

