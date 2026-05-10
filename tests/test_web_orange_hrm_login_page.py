import pytest
from playwright.sync_api import expect, Page
from pages.pw_login_page import *

orange_hrm_data = load_test_data("../testdata/orange_hrm_data.json")


@pytest.mark.positive
def test_valid_login_functionality(page: Page, load_base_url):
    load_base_url
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    page.wait_for_load_state("networkidle")
    print(f"Current page Title after login: {page.title()}")
    expect(page).to_have_title(orange_hrm_data["dashboard_page_title"])


@pytest.mark.positive
def test_logout_functionality(page: Page, load_base_url):
    load_base_url
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    expect(page.locator(user_profile)).to_be_visible()
    logout_from_orange_hrm(page)
    expect(page.locator(login_btn)).to_be_visible()


@pytest.mark.negative
def test_invalid_password_login(page: Page, load_base_url):
    load_base_url
    login_to_orange_hrm(
        page, orange_hrm_data["username"], orange_hrm_data["invalid_password"]
    )
    expect(
        page.get_by_text(orange_hrm_data["invalid_login_error_message"])
    ).to_be_visible()


@pytest.mark.negative
def test_invalid_username_login(page: Page, load_base_url):
    load_base_url
    login_to_orange_hrm(
        page, orange_hrm_data["invalid_username"], orange_hrm_data["password"]
    )
    expect(
        page.get_by_text(orange_hrm_data["invalid_login_error_message"])
    ).to_be_visible()
