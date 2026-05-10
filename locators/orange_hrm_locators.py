
#login page locators
username_input_box = "input[name='username']"
password_input_box = "input[name='password']"
login_btn = "button[type='submit']"
empty_login_msg = "//span[normalize-space()='Required']" #2 elements matching this locator, one for username and one for password.
forgot_password_link = "//p[normalize-space()='Forgot your password?']"
reset_password_popup_heading = "//h6[normalize-space()='Reset Password']"
reset_password_cancel_btn = "//button[normalize-space()='Cancel']"

#logout locators
user_profile = "//img[@class='oxd-userdropdown-img']"
logout_btn = "//a[normalize-space()='Logout']"
