from pathlib import Path
from playwright.sync_api import Playwright

PROFILE_DIR = Path("./browser-profile")


def create_browser(playwright: Playwright):
    return playwright.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=False,
        no_viewport=True,
        args=["--window-size=1280,720", "--window-position=0,0"],
    )
