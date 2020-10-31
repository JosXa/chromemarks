import sys
from pathlib import Path


def get_chromemarks_path() -> Path:
    platform = sys.platform.lower()
    if "linux" in platform:
        platform_specific_path = Path("~/.config/google-chrome/Default/Bookmarks")
    elif "darwin" in platform:
        platform_specific_path = Path(
            "~/Library/Application Support/Google/Chrome/Default/Bookmarks"
        )
    elif "win32" in platform:
        platform_specific_path = Path(
            "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
        )
    else:
        raise ValueError(
            f"It is unknown where the chrome bookmarks path for {sys.platform} is."
        )

    result = platform_specific_path.expanduser()

    if not result.exists():
        raise ValueError(
            f"Chrome bookmarks path determined to be at '{platform_specific_path}' "
            "according to system platform, but nothing exists at that location. Is Chrome installed?"
        )
    
    return result
