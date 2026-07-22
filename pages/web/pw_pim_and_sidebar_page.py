from ai_agents.auto_healer import AutoHealer
from locators.web import orange_hrm_locators

class OrangeHrmPimAndSideBarPage:
    def __init__(self, page):
        self.page = page

    def get_element(self, locator_def):
        """Helper to resolve the static LC definition into a real Playwright locator."""
        return AutoHealer.resolve_or_heal(self.page, locator_def)
    
    def verify_side_bar_functionality(self):
        """
        Verifies the side bar expand/collapse functionality.
        """
        # Wait for the sidebar arrow icon to be visible
        self.get_element(orange_hrm_locators.side_bar_arrow_icon).wait_for(state="visible")
        
        if self.get_element(orange_hrm_locators.side_bar_arrow_icon).is_visible():
            # Click to collapse the sidebar
            self.get_element(orange_hrm_locators.side_bar_arrow_icon).click()
            # Verify that the sidebar is collapsed
            if not self.get_element(orange_hrm_locators.side_bar_collapsed).is_visible():
                raise Exception("Sidebar did not collapse after clicking the arrow icon.")
            
            # Click to expand the sidebar again
            self.get_element(orange_hrm_locators.side_bar_arrow_icon).click()
            # Verify that the sidebar is expanded
            if not self.get_element(orange_hrm_locators.side_bar_expanded).is_visible():
                raise Exception("Sidebar did not expand after clicking the arrow icon again.")
        else:
            raise Exception("Sidebar arrow icon not visible - cannot verify sidebar functionality.")
        

    def navigate_to_pim_page(self, page):
        """
        Navigates to the PIM page from the dashboard.
        """
        # Click on the PIM menu item in the sidebar
        pim_locator = self.get_element(orange_hrm_locators.side_menu_pim)  # Adjust the locator as needed
        print("PIM Element Identified...................................")
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the element is interactable
        if pim_locator.is_visible():
            print("PIM menu item is visible in the sidebar, clicking to navigate to PIM page.")
            pim_locator.click()
            page.wait_for_load_state("domcontentloaded")  # Wait for the page to load after clicking
        else:
            raise Exception("PIM menu item not visible in the sidebar - cannot navigate to PIM page.")
        

    def search_in_side_bar(self, page, search_text):
        """
        Searches for a menu item in the sidebar using the search functionality.
        """
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the sidebar is fully loaded
        # Check if the sidebar search input is visible
        search_input_element = self.get_element(orange_hrm_locators.side_bar_search)
        if search_input_element.is_visible():
            print("Sidebar search input is visible, performing search for:", search_text)
            search_input_element.click()  # Click to focus the search input
            search_input_element.fill(search_text)  # Fill the search input with the provided search text
        else:
            raise Exception("Sidebar search input not visible - cannot perform search in sidebar.")
        # Wait for search results to appear
        page.wait_for_timeout(1000)


    def verify_user_profile_dropdown_options(self, page, expected_options):
        """
        Verifies that the user profile dropdown contains the expected options.
        """
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the page is fully loaded
        # Click on the user profile image to open the dropdown
        self.get_element(orange_hrm_locators.user_profile).click()

        # Wait for the dropdown options to be visible
        dropdown_options_elems = self.get_element(orange_hrm_locators.user_profile_dropdown_list)

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


    def add_employee(self, page, first_name, last_name, employee_id):
        """
        Creates a new employee in the PIM page.
        """
        self.navigate_to_pim_page(page)  # Ensure we are on the PIM page before trying to create an employee

        #if not self.get_element(orange_hrm_locators.add_employee_link).is_visible():
            #self.get_element(orange_hrm_locators.more_btn).click()
        # Click on the "Add Employee" link
        self.get_element(orange_hrm_locators.add_employee_link).click()
        page.wait_for_timeout(10000)  # Wait for 10 seconds to ensure the form is fully loaded and interactable
        # Fill in the first name and last name input fields
        try:
            first_name_locator = self.get_element(orange_hrm_locators.first_name_input_box)
            last_name_locator = self.get_element(orange_hrm_locators.last_name_input_box)
            employee_id_locator = self.get_element(orange_hrm_locators.employee_id_input_box)

            if not first_name_locator:
                raise Exception("First name input locator could not be resolved.")
            if not last_name_locator:
                raise Exception("Last name input locator could not be resolved.")
            if not employee_id_locator:
                raise Exception("Employee ID input locator could not be resolved.")

            first_name_locator.fill(first_name)
            last_name_locator.fill(last_name)
            # Clear the employee ID input box before filling it with the new employee ID
            # Use try/except around clear/fill in case the control does not support clear()
            try:
                employee_id_locator.clear()
            except Exception:
                # Some input implementations may not have clear(); ignore and proceed to fill
                pass
            self.get_element(orange_hrm_locators.employee_id_focused_input_box).fill(employee_id)
        except AttributeError as e:
            raise Exception(f"Unable to interact with input fields: {e}")
        if not self.get_element(orange_hrm_locators.employee_id_exists_msg).is_visible():
            print("Employee ID is unique, proceeding to save the new employee.")
            # Click the "Save" button to create the employee
            self.get_element(orange_hrm_locators.save_btn).click()  
            page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the employee is created and the page is updated
            return True
        else:
            print(f"Employee ID '{employee_id}' already exists - cannot create employee with duplicate ID.")
            return False


    def search_employee_in_employee_list(self, page, employee_id):
        """
        Searches for an employee in the employee list based on the employee ID.
        """
        self.navigate_to_pim_page(page)  # Ensure we are on the PIM page before trying to search for an employee

        #if not self.get_element(orange_hrm_locators.employee_list_link).is_visible():
            #self.get_element(orange_hrm_locators.more_btn).click()
        # Click on the "Employee List" link to view the list of employees
        self.get_element(orange_hrm_locators.employee_list_link).click()
        
        # Wait for the employee list to load
        page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the employee list is loaded

        # Search for the employee in the list using the search functionality
        self.get_element(orange_hrm_locators.employee_id_input_box).fill(employee_id)  # Fill the employee ID in the search input
        self.get_element(orange_hrm_locators.search_btn).click()  # Click the search button to filter the employee list

        # Wait for search results to appear
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the search results are loaded
        # Check if the employee is visible in the search results
        
        employee_locator = self.get_element(orange_hrm_locators.table_row)
        employee_locator.scroll_into_view_if_needed(timeout=10000)  # Scroll to the employee row to ensure it is in view before checking visibility
        if not employee_locator.is_visible():
            raise Exception(f"Employee with ID '{employee_id}' not found in the employee list - cannot delete.")
        print(f"Employee with ID '{employee_id}' found in the employee list.")
        return employee_locator


    def upload_profile_photo_for_employee(self, page, photo_path):
        """
        Uploads a profile photo for an employee in the PIM page.
        """
        # Click on the profile avatar to open the profile photo options
        self.get_element(orange_hrm_locators.edit_icon).click()
        self.get_element(orange_hrm_locators.profile_avatar).click()
        
        # Click on the "Add Profile Photo" button to open the file upload dialog
        #self.get_element(orange_hrm_locators.add_profile_photo_btn).wait_for(state="visible", timeout=5000).click()
        
        # Use the file chooser to select the photo to upload
        with page.expect_file_chooser() as file_chooser_info:
            self.get_element(orange_hrm_locators.add_profile_photo_btn).click()  # Click again to trigger the file chooser
        file_chooser = file_chooser_info.value
        file_chooser.set_files(photo_path)  # Set the file path for the photo to upload

        self.get_element(orange_hrm_locators.save_btn).click()  # Click the "Save" button to save the uploaded profile photo
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the changes are saved and the photo is displayed in the profile avatar
        print(f"Profile photo uploaded successfully from path: {photo_path}")


    def get_employee_from_employee_list(self, page, employee_id):
        """
        Retrieves an employee from the employee list based on the full name.
        """
        employee_locator = self.search_employee_in_employee_list(page, employee_id)  # Search for the employee in the list first
        employee_data = employee_locator.all_text_contents()
        print(f"Employee with ID '{employee_id}' found in the employee list.")
        return employee_data


    def delete_employee_from_employee_list(self, page, employee_id):
        """
        Deletes an employee from the employee list based on the employee ID.
        """
        employee_locator = self.search_employee_in_employee_list(page, employee_id)  # Search for the employee in the list first to ensure it exists before trying to delete

        # Click on the delete icon for the employee
        self.get_element(orange_hrm_locators.delete_icon).click()

        # Confirm deletion in the popup dialog
        self.get_element(orange_hrm_locators.confirm_delete_btn).click()

        # Wait for deletion to complete and verify that the employee is no longer visible in the list
        page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the deletion is complete and the page is updated
        if employee_locator.is_visible():
            raise Exception(f"Employee with ID '{employee_id}' was not deleted successfully.")
        
        print(f"Employee with ID '{employee_id}' deleted successfully from the employee list.")
    