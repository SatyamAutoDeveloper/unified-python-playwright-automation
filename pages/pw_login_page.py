from helpers.pw_page_actions import *
from locators.orange_hrm_locators import *

def login_to_orange_hrm(page, username: str, password: str):
    """
    Logs in to the application using provided credentials.
    """
    # Wait for username field and fill it
    page.locator(username_input_box).wait_for(state="visible")
    if page.locator(username_input_box).is_visible():
       page.locator(username_input_box).fill(username)
       page.locator(password_input_box).fill(password)
       page.locator(login_btn).click()
       page.wait_for_load_state("load")
    else:
       raise Exception("Login page did not load properly - username input box not visible.")


def logout_from_orange_hrm(page):
    """
    Logs out of the application.
    """
    # Click on user profile dropdown
    page.locator(user_profile).wait_for(state="visible")
    if page.locator(user_profile).is_visible():
        page.locator(user_profile).click() 
        page.locator(logout_btn).wait_for(state="visible")  # Wait for logout option to be visible
        page.locator(logout_btn).click()  # Click on logout option
    else:
        raise Exception("User profile dropdown not visible - logout failed.")
    