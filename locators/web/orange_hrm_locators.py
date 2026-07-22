from helpers.pw_location_chain import LocationChain as LC

#login page locators
username_input_box = LC.locator("input[name='username']")
password_input_box = LC.locator("input[name='password']")
login_btn = LC.locator("button[type='submit']")
empty_username_msg = LC.locator("div.oxd-input-group:has(input[name='username']) span:has-text('Required')")
empty_password_msg = LC.locator("div.oxd-input-group:has(input[name='password']) span:has-text('Required')")
forgot_password_link = LC.get_by_text("Forgot your password?")
reset_password_popup_heading = LC.get_by_role("heading", name="Reset Password")
reset_password_popup_cancel_btn = LC.get_by_role("button", name="Cancel")
reset_password_popup_reset_btn = LC.get_by_role("button", name="Reset Password")

#dashboard page locators
side_bar_arrow_icon = LC.locator("button.oxd-icon-button.oxd-main-menu-button")
side_bar_collapsed = LC.locator("a.oxd-brand.toggled")
side_bar_expanded = LC.locator("a.oxd-brand")
side_menu_pim = LC.get_by_text("PIM")
side_bar_search = LC.get_by_placeholder("Search")
searched_menu_item = LC.locator("span:has-text('Leave')")
user_profile_dropdown_list = LC.locator(".oxd-dropdown-menu li")

#pim page locators
more_btn = LC.get_by_text("More")
add_employee_link = LC.locator("li:has-text('Add Employee')")
first_name_input_box = LC.get_by_placeholder("First Name")
last_name_input_box = LC.get_by_placeholder("Last Name")
employee_id_input_box = LC.locator("//div[@class='oxd-input-group oxd-input-field-bottom-space']//div//input[@class='oxd-input oxd-input--active']")
employee_id_focused_input_box = LC.locator("//div[@class='oxd-input-group oxd-input-field-bottom-space']//div//input[@class='oxd-input oxd-input--focus']")
employee_id_exists_msg = LC.locator("span:has-text('Employee Id already exists')")
save_btn = LC.get_by_role("button", name="Save")
employee_list_link = LC.get_by_text("Employee List")
search_btn = LC.get_by_role("button", name="Search")
table_row = LC.locator("div.oxd-table-row.oxd-table-row--with-border.oxd-table-row--clickable:visible")
delete_icon = LC.locator("//i[@class='oxd-icon bi-trash']")
edit_icon = LC.locator("i.oxd-icon.bi-pencil-fill")
profile_avatar = LC.locator("div.orangehrm-edit-employee-image")
add_profile_photo_btn = LC.locator("button.oxd-icon-button.oxd-icon-button--solid-main.employee-image-action")
confirm_delete_btn = LC.get_by_text("Yes, Delete")


#logout locators
user_profile = LC.locator("//img[@class='oxd-userdropdown-img']")
logout_btn = LC.locator("//a[normalize-space()='Logout']")
