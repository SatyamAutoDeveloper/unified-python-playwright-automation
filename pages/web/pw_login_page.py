from locators.web import orange_hrm_locators


class OrangeHrmLoginPage:
    def __init__(self, page):
        self.page = page

    def get_element(self, locator_def):
        """Helper to resolve the static LC definition into a real Playwright locator."""
        return locator_def.resolve(self.page)

    def login_to_orange_hrm(self, username: str, password: str):
        """
        Logs in to the application using provided credentials.
        """
        username_field = self.get_element(orange_hrm_locators.username_input_box)
        password_field = self.get_element(orange_hrm_locators.password_input_box)
        login_button = self.get_element(orange_hrm_locators.login_btn)

        username_field.wait_for(state="visible")
        if not username_field.is_visible():
            raise Exception("Login page did not load properly - username input box not visible.")

        username_field.fill(username)
        password_field.fill(password)
        login_button.click()

        # Wait for any navigation or page load after submitting the login form.
        self.page.wait_for_load_state("load")


    def logout_from_orange_hrm(self):
        """
        Logs out of the application.
        """
        # Click on user profile dropdown
        user_profile = self.get_element(orange_hrm_locators.user_profile)
        user_profile.wait_for(state="visible")
        if user_profile.is_visible():
            user_profile.click()
            logout_btn = self.get_element(orange_hrm_locators.logout_btn)
            logout_btn.wait_for(state="visible")  # Wait for logout option to be visible
            logout_btn.click()  # Click on logout option
        else:
            raise Exception("User profile dropdown not visible - logout failed.")
    

    def verify_forgot_password_functionality(self):
        """
        Verifies the forgot password link and popup functionality.
        """
        forgot_password_link = self.get_element(orange_hrm_locators.forgot_password_link)
        forgot_password_link.wait_for(state="visible")
        if forgot_password_link.is_visible():
            forgot_password_link.click()
            reset_password_popup_heading = self.get_element(orange_hrm_locators.reset_password_popup_heading)
            reset_password_popup_heading.wait_for(state="visible")
            if not reset_password_popup_heading.is_visible():
                raise Exception("Reset Password popup did not appear after clicking forgot password link.")
        else:
            raise Exception("Forgot password link not visible on login page.")