import pathlib
import sys
import time
import pytest
from pathlib import Path
import json
import logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
from playwright.sync_api import Page, sync_playwright, APIRequestContext
from helpers.native_app_actions import MobileActions
from pages.web.pw_login_page import OrangeHrmLoginPage
from pages.web.pw_pim_and_sidebar_page import OrangeHrmPimAndSideBarPage
from api_clients.pet_store_client import PetStoreClient
from configparser import ConfigParser

sys.dont_write_bytecode = True

# --- Configuration Setup ---
CONFIG = ConfigParser()
CONFIG.read(Path(__file__).resolve().parent / "config.ini")
BASE_URL = CONFIG.get("Web", "BASE_URL", fallback="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

FAST_SHOPPING_APP_CONFIG = json.loads(
    CONFIG.get(
        "Mobile",
        "FAST_SHOPPING_APP",
        fallback='{"app": "apps/fastshopping.apk", "package": "me.wolszon.fastshopping", "activity": ".MainActivity"}'
    )
)

def pytest_addoption(parser):
    """Add a command line option to select the app."""
    parser.addoption("--app_name", action="store", default="fastshopping_app", help="Key for the app configuration defined in APP_CONFIGS")


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


@pytest.fixture(scope="function")
def android_driver(request):
    """
    Initializes the Appium UIAutomator2 driver for Android tests.
    """

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android_Emulator"
    options.automation_name = "UiAutomator2"

    # Dynamic capabilities based on selected app
    options.app = str(pathlib.Path(FAST_SHOPPING_APP_CONFIG["app"]).absolute())
    options.app_package = FAST_SHOPPING_APP_CONFIG["package"]
    options.app_activity = FAST_SHOPPING_APP_CONFIG["activity"]

    options.set_capability("appium:disableWindowAnimation", True)
    options.set_capability("appium:adbExecTimeout", 90000)

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver

    # Teardown: Quit the driver after the test
    try:
        driver.quit()
    except Exception as e:
        print(f"Error quitting driver: {e}")


@pytest.fixture(scope="function")
def NativeDriver(android_driver):
    return MobileActions(android_driver)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook to attach the report object (rep_call, rep_setup, etc.) to the test item.
    This allows fixtures to inspect the test result, specifically for failure detection.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    # Check if the test failed during the 'call' phase (the actual test execution)
    if report.when == 'call' and report.failed:
        # Access the driver instance from the test function's arguments
        try:
            driver = item.funcargs['android_driver']
            # 2. Get the screenshot as Base64 encoded PNG
            screenshot_base64 = driver.get_screenshot_as_base64()
            if isinstance(screenshot_base64, bytes):
                screenshot_base64 = screenshot_base64.decode('utf-8')
            # 3. Embed the Base64 image into the HTML report
            # The extras.png method handles embedding a base64 encoded image string
            extra.append(pytest_html.extras.png(screenshot_base64, name="Failure Screenshot"))
            
            # 4. Update the report's extra list
            report.extra = extra

            print("\nScreenshot successfully embedded in HTML report.")
        except KeyError:
            # Handle cases where the 'driver' fixture isn't used
            print("\nWebDriver fixture 'driver' not found for screenshot.")
            return
        except Exception as e:
            print(f"\nFailed to capture screenshot: {e}")
            return

        # Create a unique filename with the test name and a timestamp
        test_name = item.name.replace('/', '_').replace(':', '_') # Clean up name for filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = pathlib.Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True) # Create 'screenshots' directory if it doesn't exist
        
        screenshot_filename = str(screenshot_dir / f"FAIL_{test_name}_{timestamp}.png")
        
        # Take the screenshot
        try:
            driver.save_screenshot(screenshot_filename)
            print(f"\nScreenshot saved: {screenshot_filename}")
        except Exception as e:
            print(f"\nFailed to take screenshot: {e}")


@pytest.fixture(scope="function", autouse=True)
def capture_test_level_logs(request):
    """
    Fixture to set up a function-scoped log file for each test case.
    The log file is named after the test function and placed in a 'logs' directory.
    """
    # 1. Define Log File Path
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist

    # Get the test name (e.g., test_login_success)
    test_name = request.node.name
    log_file_path = log_dir / f"{test_name}.log"

    # 2. Configure Logger
    # Get the root logger
    logger = logging.getLogger() 
    logger.setLevel(logging.INFO) # Set the minimum logging level (e.g., INFO, DEBUG)

    # Remove any existing custom handlers (to prevent duplicate logging or inherited handlers)
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    
    # 3. Create File Handler
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8') # 'w' overwrites, use 'a' to append
    
    # 4. Define Log Format
    # You can customize this format as needed
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # 5. Add Handler to Logger
    logger.addHandler(file_handler)
    
    # Log a start message
    logger.info(f"--- STARTING TEST: {test_name} ---")

    # The 'yield' pauses the fixture and runs the actual test function
    yield logger

    # --- TEARDOWN phase (after the test function runs) ---
    logger.info(f"--- FINISHED TEST: {test_name} ---")
    
    # 6. Clean Up
    # Remove the file handler to ensure it doesn't leak into the next test
    logger.removeHandler(file_handler)
    file_handler.close()