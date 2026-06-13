import sys
import pytest
from pathlib import Path
import json
from playwright.sync_api import Page, sync_playwright, APIRequestContext
from pages.web.pw_login_page import OrangeHrmLoginPage
from pages.web.pw_pim_and_sidebar_page import OrangeHrmPimAndSideBarPage
from api_clients.pet_store_client import PetStoreClient
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
def login_page(page: Page):
    """
    Navigates to the Base URL and yields the natively provided 'page' object.
    """
    print(f"Loading base URL: {BASE_URL}")
    page.goto(BASE_URL, wait_until="networkidle")
    page.wait_for_timeout(5000)  # Wait for 2 seconds to ensure the page is fully loaded
    return OrangeHrmLoginPage(page)


@pytest.fixture(scope="function")
def pim_page_and_side_bar(page: Page):
    """
    Navigates to the Base URL and yields the natively provided 'page' object.
    """
    return OrangeHrmPimAndSideBarPage(page)


@pytest.fixture(scope="session")
def pet_store_client():
    """Fixture to provide an instance of the PetStoreClient."""
    return PetStoreClient()


@pytest.fixture(autouse=True)
def patch_api_request_context_json_support(monkeypatch):
    def patch_method(method):
        def wrapper(self, url, **kwargs):
            if 'json' in kwargs:
                json_payload = kwargs.pop('json')
                if 'data' in kwargs or 'body' in kwargs:
                    raise TypeError("Cannot specify both json and data/body")
                kwargs['data'] = json.dumps(json_payload)
                headers = kwargs.get('headers') or {}
                if isinstance(headers, dict):
                    if not any(k.lower() == 'content-type' for k in headers):
                        headers['Content-Type'] = 'application/json'
                kwargs['headers'] = headers
            return method(self, url, **kwargs)
        return wrapper

    for verb in ["post", "put", "patch"]:
        original = getattr(APIRequestContext, verb)
        monkeypatch.setattr(APIRequestContext, verb, patch_method(original))
    yield