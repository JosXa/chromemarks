from chromemarks import load_bookmarks

bookmarks = load_bookmarks()

print("============= Bookmarks Bar =============")
bookmarks_bar_items = bookmarks.roots.bookmarks_bar

for b in bookmarks_bar_items.iter_bookmarks():
    print(b.name, b.url)


print("============= Other =============")
other_items = bookmarks.roots.other

for b in other_items.iter_bookmarks():
    print(b.name, b.url)


print("============= Synced =============")
synced_items = bookmarks.roots.synced

for b in synced_items.iter_bookmarks():
    print(b.name, b.url)