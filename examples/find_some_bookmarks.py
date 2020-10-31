from chromemarks import load_bookmarks

bookmarks = load_bookmarks()

github_bookmark = bookmarks.find_bookmark(lambda bm: "JosXa/chromemarks" in bm.name)

if github_bookmark:
    print("Yep, bookmark found! Well done :)")
    assert github_bookmark.url == "https://github.com/JosXa/chromemarks"
else:
    print(
        "What a shame, you haven't added a bookmark for https://github.com/JosXa/chromemarks yet :("
    )


print("=======================")


pypi_bookmarks = list(
    filter(lambda bm: "pypi" in bm.name.lower(), bookmarks.iter_bookmarks())
)

print(f"Aha, we found {len(pypi_bookmarks)} PyPI links in your bookmarks:")

for bm in pypi_bookmarks:
    print(bm.name, bm.url)
