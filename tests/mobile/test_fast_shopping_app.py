import pytest
import logging
from pages.mobile.pw_fast_shopping_activities import *

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_presence_of_fast_shopping_page_elements(NativeDriver):
    """Test case to verify the presence of key elements on the fast shopping page."""
    # Verify page title and logo
    title_with_logo_displayed = verify_fast_shopping_page_title_and_logo_presence(NativeDriver)
    assert title_with_logo_displayed, "Expected fast shopping page title with logo to be displayed."

    # Verify 'No list selected' message
    no_list_selected_message_displayed = verify_no_list_selected_message_displayed(NativeDriver)
    assert no_list_selected_message_displayed, "Expected 'No list selected' message to be displayed."

    # Verify 'Show menu' button
    show_menu_button_displayed = verify_show_menu_button_displayed(NativeDriver)
    assert show_menu_button_displayed, "Expected 'Show menu' button to be displayed."


@pytest.mark.smoke
def test_presence_of_fast_shopping_page_show_menu_options(NativeDriver):
    """Test case to verify the presence and state of options in the fast shopping page menu."""
    archive_list_disabled, settings_clickable = verify_presence_fast_shopping_menu_options(NativeDriver)
    assert archive_list_disabled, "Expected 'Archive list' option to be disabled in the menu."
    assert settings_clickable, "Expected 'Settings' option to be clickable in the menu."


@pytest.mark.smoke
def test_default_behavior_of_multiple_shopping_lists_option_in_settings(NativeDriver):
    """Test case to verify that the 'Multiple shopping lists' option is selected by default in settings."""
    navigate_to_settings_from_fast_shopping_menu(NativeDriver)
    multiple_lists_option_selected = verify_default_behavior_of_multiple_shopping_lists_option(NativeDriver)
    assert multiple_lists_option_selected, "Expected 'Multiple shopping lists' option to be selected by default in settings."


@pytest.mark.smoke
def test_navigate_back_to_main_page_from_settings(NativeDriver):
    """Test case to verify that the user can navigate back to the main page from settings."""
    navigate_to_settings_from_fast_shopping_menu(NativeDriver)
    navigate_back_to_main_page(NativeDriver)
    # Verify that we are back on the main page by checking for the presence of the page title with logo
    title_with_logo_displayed = verify_fast_shopping_page_title_and_logo_presence(NativeDriver)
    assert title_with_logo_displayed, "Expected to be navigated back to the main page with title and logo displayed."


@pytest.mark.smoke
def test_presence_of_shopping_lists_page_elements(NativeDriver):
    """Test case to verify the presence of key elements on the shopping lists page."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    shopping_page_title_displayed, no_current_list_message_displayed, new_list_button_displayed, current_tab_selected, archived_tab_clickable = verify_default_behavior_and_presence_of_shopping_lists_page_elements(NativeDriver)
    assert shopping_page_title_displayed, "Expected shopping lists page title to be displayed."
    assert no_current_list_message_displayed, "Expected 'There are no current lists' message to be displayed when no lists are present."
    assert new_list_button_displayed, "Expected 'NEW LIST' button to be displayed on the shopping lists page."
    assert current_tab_selected, "Expected to be on the Current tab by default on the shopping lists page."
    assert archived_tab_clickable, "Expected Archived tab to be clickable on the shopping lists page."


@pytest.mark.smoke
def test_presence_of_add_new_shopping_list_popup_elements(NativeDriver):
    """Test case to verify the presence of key elements in the 'Add new shopping list' popup."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    popup_title_displayed, cancel_button_displayed, add_button_displayed, input_field_displayed = verify_presence_of_add_new_shopping_list_popup_elements(NativeDriver)
    assert popup_title_displayed, "Expected 'Add new shopping list' popup title to be displayed."
    assert input_field_displayed, "Expected input field to be displayed in the 'Add new shopping list' popup."
    assert cancel_button_displayed, "Expected 'CANCEL' button to be displayed in the 'Add new shopping list' popup."
    assert add_button_displayed, "Expected 'ADD' button to be displayed in the 'Add new shopping list' popup."


@pytest.mark.smoke
def test_adding_new_shopping_list(NativeDriver):
    """Test case to verify that a new shopping list can be added successfully."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    # Verify that the new shopping list is added and displayed in the Current tab
    new_list_displayed = verify_new_shopping_list_added(NativeDriver, "Groceries")
    assert new_list_displayed, "Expected 'Groceries' shopping list to be added and displayed in the Current tab."


@pytest.mark.smoke
def test_presence_of_shopping_list_menu_options(NativeDriver):
    """Test case to verify the presence and state of options in the shopping list menu."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    rename_option_displayed, archive_option_displayed = verify_presence_of_options_in_added_shopping_list_menu(NativeDriver)
    assert rename_option_displayed, "Expected 'Rename' option to be displayed in the shopping list menu."
    assert archive_option_displayed, "Expected 'Archive' option to be displayed in the shopping list menu."


@pytest.mark.smoke
def test_presence_of_rename_shopping_list_popup_elements(NativeDriver):
    """Test case to verify the presence of key elements in the 'Rename shopping list' popup."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    popup_title_displayed, cancel_button_displayed, rename_button_displayed, input_field_displayed = verify_presence_of_rename_shopping_list_popup_elements(NativeDriver)
    assert popup_title_displayed, "Expected 'Rename shopping list' popup title to be displayed."
    assert input_field_displayed, "Expected input field to be displayed in the 'Rename shopping list' popup."
    assert cancel_button_displayed, "Expected 'CANCEL' button to be displayed in the 'Rename shopping list' popup."
    assert rename_button_displayed, "Expected 'RENAME' button to be displayed in the 'Rename shopping list' popup."


@pytest.mark.smoke
def test_renaming_shopping_list(NativeDriver):
    """Test case to verify that a shopping list can be renamed successfully."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    rename_shopping_list(NativeDriver, "Supermarket List")
    # Verify that the shopping list is renamed and displayed with the new name in the Current tab
    renamed_list_displayed = verify_shopping_list_renamed(NativeDriver, "Supermarket List")
    assert renamed_list_displayed, "Expected 'Groceries' shopping list to be renamed to 'Supermarket List' and displayed in the Current tab."


@pytest.mark.smoke
def test_presence_of_add_item_popup_elements(NativeDriver):
    """Test case to verify the presence of key elements in the 'Add item' popup."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    popup_title_displayed, cancel_button_displayed, add_button_displayed, input_field_displayed = verify_presence_of_add_item_popup_elements(NativeDriver)
    assert popup_title_displayed, "Expected 'Add item' popup title to be displayed."
    assert input_field_displayed, "Expected input field to be displayed in the 'Add item' popup."
    assert cancel_button_displayed, "Expected 'CANCEL' button to be displayed in the 'Add item' popup."
    assert add_button_displayed, "Expected 'ADD' button to be displayed in the 'Add item' popup."


@pytest.mark.smoke
def test_adding_new_item_to_shopping_list(NativeDriver):
    """Test case to verify that a new item can be added to a shopping list successfully."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    add_new_item_to_shopping_list(NativeDriver, "Bananas")
    # Verify that the new item is added and displayed in the shopping list
    new_item_displayed = verify_new_item_added_to_shopping_list(NativeDriver, "Bananas")
    assert new_item_displayed, "Expected 'Bananas' item to be added and displayed in the 'Groceries' shopping list."


@pytest.mark.smoke
def test_archive_shopping_list(NativeDriver):
    """Test case to verify that a shopping list is archived successfully."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    archive_shopping_list(NativeDriver)
    # Verify that the shopping list is archived and displayed in the Archived tab
    archived_shopping_list_displayed = verify_shopping_list_archived(NativeDriver)
    assert archived_shopping_list_displayed, "Expected 'Groceries' shopping list to be archived and displayed in the Archived tab."


@pytest.mark.smoke
def test_delete_shopping_list(NativeDriver):
    """Test case to verify that a shopping list is deleted successfully."""
    navigate_to_shopping_lists_page_from_main_page(NativeDriver)
    click_new_list_button(NativeDriver)
    add_new_shopping_list(NativeDriver, "Groceries")
    archive_shopping_list(NativeDriver)
    delete_archived_shopping_list(NativeDriver)
    shopping_list_deleted = verify_shopping_list_deleted(NativeDriver)
    assert shopping_list_deleted, "Expected 'Groceries' shopping list to be deleted and no longer displayed in the Archived tab."