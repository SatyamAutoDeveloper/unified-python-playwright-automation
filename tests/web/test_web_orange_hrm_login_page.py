import pytest
from playwright.sync_api import expect, Page
from helpers.pw_common_helpers import *
from pages.web.pw_login_page import *
from locators.web.orange_hrm_locators import *

orange_hrm_data = load_test_data("../../testdata/web/orange_hrm_data.json")


@pytest.mark.positive
def test_valid_login_functionality(login_page, page: Page):
    login_page.login_to_orange_hrm(orange_hrm_data["username"], orange_hrm_data["password"])
    page.wait_for_load_state("networkidle")
    print(f"Current page Title after login: {page.title()}")
    expect(page).to_have_title(orange_hrm_data["dashboard_page_title"])


@pytest.mark.positive
def test_logout_functionality(login_page, page: Page):
    login_page.login_to_orange_hrm(orange_hrm_data["username"], orange_hrm_data["password"])
    page.wait_for_load_state("load")
    expect(login_page.get_element(orange_hrm_locators.user_profile)).to_be_visible()
    login_page.logout_from_orange_hrm()
    expect(login_page.get_element(orange_hrm_locators.login_btn)).to_be_visible()


@pytest.mark.negative
def test_invalid_password_login(login_page, page: Page):
    login_page.login_to_orange_hrm(orange_hrm_data["username"], orange_hrm_data["invalid_password"])
    expect(page.get_by_text(orange_hrm_data["invalid_login_error_message"])).to_be_visible()


@pytest.mark.negative
def test_invalid_username_login(login_page, page: Page):
    login_page.login_to_orange_hrm(orange_hrm_data["invalid_username"], orange_hrm_data["password"])
    expect(page.get_by_text(orange_hrm_data["invalid_login_error_message"])).to_be_visible()


@pytest.mark.negative
def test_empty_credentials_login(login_page):
    login_page.login_to_orange_hrm("", "")
    # Expect both username and password required messages to be visible
    expect(login_page.get_element(orange_hrm_locators.empty_username_msg)).to_be_visible()  # Username required message
    expect(login_page.get_element(orange_hrm_locators.empty_password_msg)).to_be_visible()  # Password required message


@pytest.mark.positive
def test_forgot_password_link(login_page):
    login_page.verify_forgot_password_functionality()
    expect(login_page.get_element(orange_hrm_locators.reset_password_popup_cancel_btn)).to_be_visible()
    expect(login_page.get_element(orange_hrm_locators.reset_password_popup_reset_btn)).to_be_visible()
