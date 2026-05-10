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