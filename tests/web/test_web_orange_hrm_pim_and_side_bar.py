import pytest
from playwright.sync_api import expect, Page
from pages.web.pw_login_page import *
from pages.web.pw_pim_and_sidebar_page import *

orange_hrm_data = load_test_data("../testdata/orange_hrm_data.json")

@pytest.mark.positive
def test_verify_side_bar_functionality(page: Page, load_base_url):
    """
    Test to verify the side bar expand/collapse functionality on the OrangeHRM dashboard page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    # Verify the side bar functionality
    verify_side_bar_functionality(page)