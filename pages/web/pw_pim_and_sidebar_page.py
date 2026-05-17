from helpers.pw_page_actions import *
from locators.web.orange_hrm_locators import *


def verify_side_bar_functionality(page):
    """
    Verifies the side bar expand/collapse functionality.
    """
    # Wait for the sidebar arrow icon to be visible
    page.locator(side_bar_arrow_icon).wait_for(state="visible")
    
    if page.locator(side_bar_arrow_icon).is_visible():
        # Click to collapse the sidebar
        page.locator(side_bar_arrow_icon).click()
        # Verify that the sidebar is collapsed
        if not page.locator(side_bar_collapsed).is_visible():
            raise Exception("Sidebar did not collapse after clicking the arrow icon.")
        
        # Click to expand the sidebar again
        page.locator(side_bar_arrow_icon).click()
        # Verify that the sidebar is expanded
        if not page.locator(side_bar_expanded).is_visible():
            raise Exception("Sidebar did not expand after clicking the arrow icon again.")
    else:
        raise Exception("Sidebar arrow icon not visible - cannot verify sidebar functionality.")
    

def navigate_to_pim_page(page):
    """
    Navigates to the PIM page from the dashboard.
    """
    # Click on the PIM menu item in the sidebar
    pim_locator = page.locator(f"span:has-text('{side_menu_pim}')")  # Adjust the locator as needed
    print("PIM Element Identified...................................")
    page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the element is interactable
    if pim_locator.is_visible():
        print("PIM menu item is visible in the sidebar, clicking to navigate to PIM page.")
        pim_locator.click()
        page.wait_for_load_state("domcontentloaded")  # Wait for the page to load after clicking
    else:
        raise Exception("PIM menu item not visible in the sidebar - cannot navigate to PIM page.")
    

def search_in_side_bar(page, search_text):
    """
    Searches for a menu item in the sidebar using the search functionality.
    """
    page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the sidebar is fully loaded
    # Check if the sidebar search input is visible
    search_input_element = page.get_by_placeholder(side_bar_search)
    if search_input_element.is_visible():
        print("Sidebar search input is visible, performing search for:", search_text)
        search_input_element.click()  # Click to focus the search input
        search_input_element.fill(search_text)  # Fill the search input with the provided search text
    else:
        raise Exception("Sidebar search input not visible - cannot perform search in sidebar.")
    # Wait for search results to appear
    page.wait_for_timeout(1000)


def verify_user_profile_dropdown_options(page, expected_options):
    """
    Verifies that the user profile dropdown contains the expected options.
    """
    page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the page is fully loaded
    # Click on the user profile image to open the dropdown
    page.locator(user_profile).click()

    # Wait for the dropdown options to be visible
    dropdown_options_elems = page.locator(user_profile_dropdown_list)

    expected_options_count = len(expected_options)
    actual_options_count = dropdown_options_elems.count()
    print(f"Actual number of options in user profile dropdown: {actual_options_count}")
    
    if actual_options_count != expected_options_count:
        raise Exception(f"Expected {expected_options_count} options in user profile dropdown, but found {actual_options_count}.")
    
    # Get the list of dropdown options
    dropdown_options = dropdown_options_elems.all_text_contents()
    print("User profile dropdown options found:", dropdown_options)

    # Verify that all expected options are present in the dropdown
    for option in expected_options:
        if option not in dropdown_options:
            raise Exception(f"Expected option '{option}' not found in user profile dropdown.")