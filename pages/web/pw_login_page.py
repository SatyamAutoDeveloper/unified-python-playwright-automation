from helpers.pw_page_actions import *
from locators.web.orange_hrm_locators import *

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
    

def verify_forgot_password_functionality(page):
    """
    Verifies the forgot password link and popup functionality.
    """
    page.get_by_text(forgot_password_link_text).wait_for(state="visible")
    if page.get_by_text(forgot_password_link_text).is_visible():
        page.get_by_text(forgot_password_link_text).click()
        page.get_by_role("heading", name=reset_password_popup_heading_text).wait_for(state="visible")
        if not page.get_by_role("heading", name=reset_password_popup_heading_text).is_visible():
            raise Exception("Reset Password popup did not appear after clicking forgot password link.")
    else:
        raise Exception("Forgot password link not visible on login page.")