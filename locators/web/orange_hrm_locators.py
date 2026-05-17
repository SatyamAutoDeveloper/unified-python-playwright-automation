
#login page locators
username_input_box = "input[name='username']"
password_input_box = "input[name='password']"
login_btn = "button[type='submit']"
empty_login_msg = "//span[normalize-space()='Required']" #2 elements matching this locator, one for username and one for password.
forgot_password_link_text = "Forgot your password?"
reset_password_popup_heading_text = "Reset Password"
reset_password_popup_cancel_btn_text = "Cancel"
reset_password_popup_reset_btn_text = "Reset Password"

#dashboard page locators
side_bar_arrow_icon = "button.oxd-icon-button.oxd-main-menu-button"
side_bar_collapsed = "a.oxd-brand.toggled"
side_bar_expanded = "a.oxd-brand"
side_menu_pim = "PIM"
side_bar_search = "Search"
searched_menu_item = "span:has-text('Leave')"
user_profile_dropdown_list = ".oxd-dropdown-menu li"

#pim page locators
add_employee_btn = "Add Employee"


#logout locators
user_profile = "//img[@class='oxd-userdropdown-img']"
logout_btn = "//a[normalize-space()='Logout']"
