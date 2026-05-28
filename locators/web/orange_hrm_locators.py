
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
add_employee_link = "Add Employee"
first_name_input_box = "First Name"
last_name_input_box = "Last Name"
employee_id_input_box = "//div[@class='oxd-input-group oxd-input-field-bottom-space']//div//input[@class='oxd-input oxd-input--active']"
employee_id_focused_input_box = "//div[@class='oxd-input-group oxd-input-field-bottom-space']//div//input[@class='oxd-input oxd-input--focus']"
save_btn = "Save"
employee_list_link = "Employee List"
search_btn = "Search"
table_row = "//body/div[@id='app']/div[@class='oxd-layout orangehrm-upgrade-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']/div[@class='orangehrm-background-container']/div[@class='orangehrm-paper-container']/div[@class='orangehrm-container']/div[@role='table']/div[@role='rowgroup']/div[@class='oxd-table-card']/div[@role='row']"
delete_icon = "//i[@class='oxd-icon bi-trash']"
edit_icon = "i.oxd-icon.bi-pencil-fill"
profile_avatar = "div.orangehrm-edit-employee-image"
add_profile_photo_btn = "button.oxd-icon-button.oxd-icon-button--solid-main.employee-image-action" 
confirm_delete_btn = "Yes, Delete"


#logout locators
user_profile = "//img[@class='oxd-userdropdown-img']"
logout_btn = "//a[normalize-space()='Logout']"
