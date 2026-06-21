from locators.mobile.fast_shopping_locators import *
from helpers.native_app_actions import MobileActions
import logging

logger = logging.getLogger(__name__)

def verify_fast_shopping_page_title_and_logo_presence(driver):
    """Verifies that the fast shopping page title is present with logo."""
    MobileActions.wait_for_element_present(driver, app_name_with_logo)
    title_displayed = MobileActions.is_element_displayed(driver, app_name_with_logo)
    logger.info(f"Fast Shopping page title with logo displayed: {title_displayed}")
    return title_displayed


def verify_no_list_selected_message_displayed(driver):
    """Verifies that the 'No list selected' message is displayed when no shopping list is selected."""
    MobileActions.wait_for_element_present(driver, no_list_selected_list_elem)
    message_displayed = MobileActions.is_element_displayed(driver, no_list_selected_list_elem)
    logger.info(f"'No list selected' message displayed: {message_displayed}")
    return message_displayed


def verify_show_menu_button_displayed(driver):
    """Verifies that the 'Show menu' button is displayed on the fast shopping page."""
    MobileActions.wait_for_element_present(driver, show_menu_btn)
    button_displayed = MobileActions.is_element_displayed(driver, show_menu_btn)
    logger.info(f"'Show menu' button displayed: {button_displayed}")
    return button_displayed


def verify_presence_fast_shopping_menu_options(driver):
    """Verifies that the expected options are present in the fast shopping menu."""
    MobileActions.wait_for_element_present(driver, show_menu_btn)
    MobileActions.click_on_element(driver, show_menu_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    archive_list_option_disabled = MobileActions.is_element_disabled(driver, archive_list_btn)
    logger.info(f"'Archive list' option disabled in menu: {archive_list_option_disabled}")
    settings_option_clickable = MobileActions.is_element_clickable(driver, settings_btn)
    logger.info(f"'Settings' option clickable in menu: {settings_option_clickable}")
    return archive_list_option_disabled, settings_option_clickable


def navigate_to_settings_from_fast_shopping_menu(driver):
    """Navigates to the settings page from the fast shopping menu."""
    MobileActions.wait_for_element_present(driver, show_menu_btn)
    MobileActions.click_on_element(driver, show_menu_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    MobileActions.click_on_element(driver, settings_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for settings page to load


def verify_default_behavior_of_multiple_shopping_lists_option(driver):
    """Verifies that the 'Multiple shopping lists' option is selected by default in settings."""
    multiple_lists_option_selected = MobileActions.is_element_checked(driver, multiple_shopping_lists_radio_btn)
    logger.info(f"'Multiple shopping lists' option selected by default: {multiple_lists_option_selected}")
    return multiple_lists_option_selected


def navigate_back_to_main_page(driver):
    """Navigates back to the main page from settings or any other subpage."""
    MobileActions.wait_for_element_present(driver, navigate_back_btn)
    MobileActions.click_on_element(driver, navigate_back_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for navigation to complete


def navigate_to_shopping_lists_page_from_main_page(driver):
    """Navigates to the shopping lists page from the main page."""
    MobileActions.wait_for_element_present(driver, no_list_selected_list_elem)
    MobileActions.click_on_element(driver, no_list_selected_list_elem)
    MobileActions.implicit_wait(driver, 2) # Wait for shopping lists page to load


def navigate_to_shopping_lists_page_after_adding_list(driver):
    """Navigates to the shopping lists page after adding a new shopping list from the main page."""
    MobileActions.wait_for_element_present(driver, groceries_list_elem)
    MobileActions.click_on_element(driver, groceries_list_elem)
    MobileActions.implicit_wait(driver, 2) # Wait for shopping lists page to load


def verify_default_behavior_and_presence_of_shopping_lists_page_elements(driver):
    """Verifies the default behavior and presence of key elements on the shopping lists page."""
    MobileActions.wait_for_element_present(driver, shoppings_list_page_title)
    title_displayed = MobileActions.is_element_displayed(driver, shoppings_list_page_title)
    logger.info(f"Shopping lists page title displayed: {title_displayed}")
    
    no_current_list_message_displayed = MobileActions.is_element_displayed(driver, current_tab_no_current_list_msg)
    logger.info(f"'There are no current lists' message displayed: {no_current_list_message_displayed}")

    new_list_button_displayed = MobileActions.is_element_displayed(driver, current_tab_new_list_btn)
    logger.info(f"'NEW LIST' button displayed: {new_list_button_displayed}")
    
    # Verify that we are on the Current tab by default
    current_tab_selected = MobileActions.is_element_displayed(driver, current_tab)
    logger.info(f"Current tab is selected by default: {current_tab_selected}")

    # Verify that the Archived tab is clickable
    archived_tab_clickable = MobileActions.is_element_clickable(driver, archived_tab)
    logger.info(f"Archived tab is clickable: {archived_tab_clickable}")

    return title_displayed, no_current_list_message_displayed, new_list_button_displayed, current_tab_selected, archived_tab_clickable


def click_new_list_button(driver):
    """Clicks on the 'NEW LIST' button on the shopping lists page."""
    MobileActions.wait_for_element_present(driver, current_tab_new_list_btn)
    MobileActions.click_on_element(driver, current_tab_new_list_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for new list popup to appear


def verify_presence_of_add_new_shopping_list_popup_elements(driver):
    """Verifies the presence of key elements in the 'Add new shopping list' popup."""
    MobileActions.wait_for_element_present(driver, new_list_popup_title)
    popup_title_displayed = MobileActions.is_element_displayed(driver, new_list_popup_title)
    logger.info(f"'Add new shopping list' popup title displayed: {popup_title_displayed}")

    cancel_button_displayed = MobileActions.is_element_displayed(driver, new_list_popup_cancel_btn)
    logger.info(f"'CANCEL' button in new list popup displayed: {cancel_button_displayed}")

    add_button_displayed = MobileActions.is_element_displayed(driver, new_list_popup_add_btn)
    logger.info(f"'ADD' button in new list popup displayed: {add_button_displayed}")

    input_field_displayed = MobileActions.is_element_displayed(driver, new_list_popup_input_field)
    logger.info(f"Input field in new list popup displayed: {input_field_displayed}")

    return popup_title_displayed, cancel_button_displayed, add_button_displayed, input_field_displayed


def add_new_shopping_list(driver, list_name):
    """Adds a new shopping list with the given name."""
    MobileActions.implicit_wait(driver, 2) # Wait for the 'Add new shopping list' popup to be fully loaded
    MobileActions.move_to_element_and_type_value(driver, new_list_popup_input_field, list_name)
    MobileActions.move_to_element_and_click(driver, new_list_popup_add_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for the new list to be added and page to update


def verify_new_shopping_list_added(driver, list_name):
    """Verifies that a new shopping list with the given name has been added successfully."""
    # We can verify this by checking for the presence of the new list name in the list of current shopping lists
    new_list_locator = (AppiumBy.XPATH, f'//*[@content-desc="{list_name}"]')
    MobileActions.wait_for_element_present(driver, new_list_locator)
    new_list_displayed = MobileActions.is_element_displayed(driver, new_list_locator)
    logger.info(f"New shopping list '{list_name}' added and displayed: {new_list_displayed}")
    return new_list_displayed


def verify_presence_of_options_in_added_shopping_list_menu(driver):
    """Verifies the presence of expected options in the menu of an added shopping list."""
    MobileActions.wait_for_element_present(driver, groceries_list_elem)
    MobileActions.click_on_element(driver, groceries_list_elem) # Click on the added shopping list to select it
    MobileActions.implicit_wait(driver, 2) # Wait for the list to be selected and page to update
    MobileActions.wait_for_element_present(driver, current_tab_list_show_menu_btn)
    MobileActions.click_on_element(driver, current_tab_list_show_menu_btn) # Click on 'Show menu' button for the selected shopping list
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    rename_option_displayed = MobileActions.is_element_displayed(driver, current_tab_rename_list_btn)
    logger.info(f"'RENAME' option displayed in shopping list menu: {rename_option_displayed}")
    archive_option_displayed = MobileActions.is_element_displayed(driver, current_tab_archive_list_btn)
    logger.info(f"'ARCHIVE' option displayed in shopping list menu: {archive_option_displayed}")
    return rename_option_displayed, archive_option_displayed


def verify_presence_of_rename_shopping_list_popup_elements(driver):
    """Verifies the presence of key elements in the 'Rename shopping list' popup."""
    MobileActions.wait_for_element_present(driver, groceries_list_elem)
    MobileActions.click_on_element(driver, groceries_list_elem) # Click on the added shopping list to select it
    MobileActions.implicit_wait(driver, 2) # Wait for the list to be selected and page to update
    MobileActions.wait_for_element_present(driver, current_tab_list_show_menu_btn)
    MobileActions.click_on_element(driver, current_tab_list_show_menu_btn) # Click on 'Show menu' button for the selected shopping list
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    MobileActions.click_on_element(driver, current_tab_rename_list_btn) # Click on 'Rename' option in the menu
    MobileActions.implicit_wait(driver, 2) # Wait for rename shopping list popup to appear
    MobileActions.wait_for_element_present(driver, rename_shopping_list_popup_title)
    popup_title_displayed = MobileActions.is_element_displayed(driver, rename_shopping_list_popup_title)
    logger.info(f"'Rename shopping list' popup title displayed: {popup_title_displayed}")

    cancel_button_displayed = MobileActions.is_element_displayed(driver, rename_shopping_list_popup_cancel_btn)
    logger.info(f"'CANCEL' button in rename shopping list popup displayed: {cancel_button_displayed}")

    rename_button_displayed = MobileActions.is_element_displayed(driver, rename_shopping_list_popup_rename_btn)
    logger.info(f"'RENAME' button in rename shopping list popup displayed: {rename_button_displayed}")

    input_field_displayed = MobileActions.is_element_displayed(driver, rename_shopping_list_popup_input_field)
    logger.info(f"Input field in rename shopping list popup displayed: {input_field_displayed}")

    return popup_title_displayed, cancel_button_displayed, rename_button_displayed, input_field_displayed


def rename_shopping_list(driver, new_name):
    """Renames a shopping list from old name to new name."""
    MobileActions.wait_for_element_present(driver, groceries_list_elem)
    MobileActions.click_on_element(driver, groceries_list_elem) # Click on the added shopping list to select it
    MobileActions.implicit_wait(driver, 2) # Wait for the list to be selected and page to update
    MobileActions.wait_for_element_present(driver, current_tab_list_show_menu_btn)
    MobileActions.click_on_element(driver, current_tab_list_show_menu_btn) # Click on 'Show menu' button for the selected shopping list
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    MobileActions.click_on_element(driver, current_tab_rename_list_btn) # Click on 'Rename' option in the menu
    MobileActions.implicit_wait(driver, 2) # Wait for rename shopping list popup to appear
    MobileActions.move_to_element_and_type_value(driver, rename_shopping_list_popup_input_field, new_name)
    MobileActions.move_to_element_and_click(driver, rename_shopping_list_popup_rename_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for the shopping list to be renamed and page to update


def verify_shopping_list_renamed(driver, new_name):
    """Verifies that a shopping list has been renamed successfully to the new name."""
    # We can verify this by checking for the presence of the new list name in the list of current shopping lists
    renamed_list_locator = (AppiumBy.XPATH, f'//*[@content-desc="Groceries{new_name}"]')
    MobileActions.wait_for_element_present(driver, renamed_list_locator)
    renamed_list_displayed = MobileActions.is_element_displayed(driver, renamed_list_locator)
    logger.info(f"Shopping list renamed to '{"Groceries"}{new_name}' and displayed: {renamed_list_displayed}")
    return renamed_list_displayed


def archive_shopping_list(driver):
    """Archives a shopping list."""
    MobileActions.wait_for_element_present(driver, groceries_list_elem)
    MobileActions.click_on_element(driver, groceries_list_elem) # Click on the added shopping list to select it
    MobileActions.implicit_wait(driver, 2) # Wait for the list to be selected and page to update
    MobileActions.wait_for_element_present(driver, current_tab_list_show_menu_btn)
    MobileActions.click_on_element(driver, current_tab_list_show_menu_btn) # Click on 'Show menu' button for the selected shopping list
    MobileActions.implicit_wait(driver, 2) # Wait for menu to open
    MobileActions.click_on_element(driver, current_tab_archive_list_btn) # Click on 'Archive' option in the menu
    MobileActions.implicit_wait(driver, 2) # Wait for the shopping list to be archived and page to update


def verify_shopping_list_archived(driver):
    """Verifies that a shopping list has been archived successfully."""
    MobileActions.click_on_element(driver, archived_tab)  
    MobileActions.wait_for_element_present(driver, archived_groceries_list_elem)
    shopping_list_present = MobileActions.is_element_displayed(driver, archived_groceries_list_elem)
    logger.info(f"Shopping list archived and displayed in Archived tab: {shopping_list_present}")
    return shopping_list_present


def delete_archived_shopping_list(driver):
    """Delete the Shopping List"""
    MobileActions.click_on_element(driver, archived_tab)  
    MobileActions.wait_for_element_present(driver, archived_groceries_list_elem)
    MobileActions.click_on_element(driver, archived_tab_list_show_menu_btn)
    MobileActions.implicit_wait(driver, 2)
    MobileActions.click_on_element(driver, archive_tab_delete_btn)
    MobileActions.implicit_wait(driver, 2)
    MobileActions.click_on_element(driver, delete_list_confirmation_popup_delete_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for the shopping list to be deleted


def verify_shopping_list_deleted(driver):
    """Verifies that a shopping list has been deleted successfully."""
    shopping_list_deleted = not MobileActions.is_element_displayed(driver, archived_groceries_list_elem)
    logger.info(f"Shopping list deleted and not displayed in Archived tab: {shopping_list_deleted}")
    return shopping_list_deleted


def click_add_item_button(driver):
    """Clicks on the 'Add item' button in the shopping list page."""
    MobileActions.wait_for_element_present(driver, current_tab_add_item_btn)
    MobileActions.click_on_element(driver, current_tab_add_item_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for add item popup to appear


def verify_presence_of_add_item_popup_elements(driver):
    """Verifies the presence of key elements in the 'Add item' popup."""
    click_add_item_button(driver) # Ensure we are on the add item popup before verifying elements
    MobileActions.wait_for_element_present(driver, add_item_popup_title)
    popup_title_displayed = MobileActions.is_element_displayed(driver, add_item_popup_title)
    logger.info(f"'Add item' popup title displayed: {popup_title_displayed}")

    cancel_button_displayed = MobileActions.is_element_displayed(driver, add_item_popup_cancel_btn)
    logger.info(f"'CANCEL' button in add item popup displayed: {cancel_button_displayed}")

    add_button_displayed = MobileActions.is_element_displayed(driver, add_item_popup_add_btn)
    logger.info(f"'ADD' button in add item popup displayed: {add_button_displayed}")

    input_field_displayed = MobileActions.is_element_displayed(driver, add_item_popup_input_field)
    logger.info(f"Input field in add item popup displayed: {input_field_displayed}")

    return popup_title_displayed, cancel_button_displayed, add_button_displayed, input_field_displayed


def add_new_item_to_shopping_list(driver, item_name):
    """Adds a new item with the given name to the shopping list."""
    click_add_item_button(driver) # Ensure we are on the add item popup before trying to add an item
    MobileActions.implicit_wait(driver, 2) # Wait for the 'Add item' popup to be fully loaded
    MobileActions.move_to_element_and_type_value(driver, add_item_popup_input_field, item_name)
    MobileActions.move_to_element_and_click(driver, add_item_popup_add_btn)
    MobileActions.implicit_wait(driver, 2) # Wait for the new item to be added and page to update


def verify_new_item_added_to_shopping_list(driver, item_name):
    """Verifies that a new item with the given name has been added to the shopping list successfully."""
    # We can verify this by checking for the presence of the new item name in the list of items in the shopping list
    new_item_locator = (AppiumBy.XPATH, f'//*[@content-desc="{item_name}"]')
    MobileActions.wait_for_element_present(driver, new_item_locator)
    new_item_displayed = MobileActions.is_element_displayed(driver, new_item_locator)
    logger.info(f"New item '{item_name}' added to shopping list and displayed: {new_item_displayed}")
    return new_item_displayed