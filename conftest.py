import sys
import pytest
from pathlib import Path
from playwright.sync_api import Page, sync_playwright
from configparser import ConfigParser

sys.dont_write_bytecode = True

# --- Configuration Setup ---
CONFIG = ConfigParser()
CONFIG.read("config.ini")
BASE_URL = CONFIG.get('BASE_URL', 'Web', fallback="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

# --- Pytest Hooks ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to attach the test result to the request node.
    This allows fixtures to peek at the test outcome (pass/fail) after it runs.
    """
    outcome = yield
    rep = outcome.get_result()
    # Attach the report to the test item for the specific phase (setup, call, teardown)
    setattr(item, "rep_" + rep.when, rep)


# --- Pytest-Playwright Native Overrides ---
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, browser_name):
    """Overrides native playwright launch arguments."""
    # Only apply the anti-automation flag if the browser is Chromium
    if browser_name == "chromium":
        print("Launching Chromium...................................")
        return {
            **browser_type_launch_args,
            "args": ["--disable-blink-features=AutomationControlled", "--start-maximized"],
        }
    return browser_type_launch_args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Overrides native playwright context arguments."""
    return {
        **browser_context_args,
        "no_viewport": True
    }


# --- Custom Helper Fixtures ---
@pytest.fixture(scope="function")
def load_base_url(page: Page):
    """
    Navigates to the Base URL and yields the natively provided 'page' object.
    """
    print(f"Loading base URL: {BASE_URL}")
    page.goto(BASE_URL, wait_until="networkidle")
    page.wait_for_timeout(5000)  # Wait for 2 seconds to ensure the page is fully loaded
