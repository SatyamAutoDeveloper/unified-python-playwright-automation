import pytest
from playwright.sync_api import expect, Page
from pages.web.pw_login_page import *
from pages.web.pw_pim_and_sidebar_page import *

orange_hrm_data = load_test_data("../testdata/orange_hrm_data.json")
profile_photo_path = os.path.abspath("testdata/herbs.jpg")

'''
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


@pytest.mark.positive
def test_navigate_to_pim_page(page: Page, load_base_url):
    """
    Test to verify navigation to the PIM page from the dashboard.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    # Navigate to the PIM page
    navigate_to_pim_page(page)
    
    # Verify that we are on the PIM page
    expect(page).to_have_url(orange_hrm_data["pim_page_url"])


@pytest.mark.positive
def test_search_in_side_bar(page: Page, load_base_url):
    """
    Test to verify the search functionality in the sidebar of the OrangeHRM dashboard page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    # Search for a menu item in the sidebar
    search_in_side_bar(page, orange_hrm_data["side_bar_search_text"])
    
    # Verify that the expected menu item is visible in the search results (you may need to adjust this based on how results are displayed)
    expect(page.locator(searched_menu_item)).to_be_visible()


@pytest.mark.positive
def test_user_profile_dropdown_list(page: Page, load_base_url):
    """
    Test to verify the options available in the user profile dropdown list on the OrangeHRM dashboard page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    # Verify the options in the user profile dropdown list
    verify_user_profile_dropdown_options(page, orange_hrm_data["user_profile_dropdown_list_text"])
'''

@pytest.mark.positive
def test_add_employee_in_pim_page(page: Page, load_base_url):
    """
    Test to verify adding a new employee in the PIM page of OrangeHRM.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    add_employee(page, orange_hrm_data["first_name"], orange_hrm_data["last_name"], orange_hrm_data["employee_id"])
    expect(page.locator(f"h6:has-text('{orange_hrm_data['first_name']} {orange_hrm_data['last_name']}')")).to_be_visible(timeout=10000)


@pytest.mark.positive
def test_search_employee_in_employee_list(page: Page, load_base_url):
    """
    Test to verify searching for an employee in the employee list of the PIM page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    employee_data = get_employee_from_employee_list(page, orange_hrm_data["employee_id"])
    print(f"Employee data for ID '{orange_hrm_data['employee_id']}': {employee_data}")


@pytest.mark.positive
def test_upload_profile_photo_for_added_employee(page: Page, load_base_url):
    """
    Test to verify uploading a profile photo for an employee in the employee list of the PIM page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    search_employee_in_employee_list(page, orange_hrm_data["employee_id"])
    upload_profile_photo_for_employee(page, profile_photo_path)


@pytest.mark.positive
def test_delete_employee_from_employee_list(page: Page, load_base_url):
    """
    Test to verify deleting an employee from the employee list in the PIM page.
    """
    load_base_url
    # Perform login using the login page function
    login_to_orange_hrm(page, orange_hrm_data["username"], orange_hrm_data["password"])
    
    # Verify that we are on the dashboard page after login
    expect(page).to_have_url(orange_hrm_data["dashboard_page_url"])
    
    delete_employee_from_employee_list(page, orange_hrm_data["employee_id"])