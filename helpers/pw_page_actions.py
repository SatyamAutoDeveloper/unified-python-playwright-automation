from playwright.sync_api import Page, expect


def find_element(page: Page, selector: str):
    """
    Utility function to find an element using a selector.
    """
    return page.locator(selector)


def find_elements(page: Page, selector: str):
    """
    Utility function to find multiple elements using a selector.
    """
    return page.locator(selector)


def find_element_by_text(page: Page, selector: str, text: str):
    """
    Utility function to find an element by text using a selector.
    """
    return page.locator(selector, has_text=text)


def find_element_by_label(page: Page, label: str):
    """
    Utility function to find an element by its associated label text.
    """
    return page.get_by_label(label)


def type_value(page: Page, selector: str, value: str):
    """
    Utility function to fill an input field using a selector.
    """
    find_element(page, selector).fill(value)


def get_element_text(page: Page, selector: str) -> str:
    """
    Utility function to get text content of an element using a selector.
    """
    return find_element(page, selector).inner_text()


def get_element_attribute(page: Page, selector: str, attribute: str) -> str:
    """
    Utility function to get an attribute value of an element using a selector.
    """
    return find_element(page, selector).get_attribute(attribute)


def get_element_count(page: Page, selector: str) -> int:
    """
    Utility function to get the count of elements matching a selector.
    """
    return find_element(page, selector).count()


def get_elements_texts(page: Page, selector: str) -> list:
    """
    Utility function to get text contents of multiple elements matching a selector.
    """
    return find_elements(page, selector).all_inner_texts()


def wait_for_element_to_be_visible(page: Page, selector: str, timeout: int = 10000):
    """
    Utility function to wait for an element to be visible using a selector.
    """
    expect(find_element(page, selector)).to_be_visible(timeout=timeout)


def is_element_visible(page: Page, selector: str) -> bool:
    """
    Utility function to check if an element is visible using a selector.
    """
    return find_element(page, selector).is_visible()


def is_element_enabled(page: Page, selector: str) -> bool:
    """
    Utility function to check if an element is enabled using a selector.
    """
    return find_element(page, selector).is_enabled()


def is_element_disabled(page: Page, selector: str) -> bool:
    """
    Utility function to check if an element is disabled using a selector.
    """
    return find_element(page, selector).is_disabled()


def is_element_checked(page: Page, selector: str) -> bool:
    """
    Utility function to check if a checkbox or radio button is checked using a selector.
    """
    return find_element(page, selector).is_checked()


def select_option_from_dropdown(page: Page, selector: str, value: str):
    """
    Utility function to select an option from a dropdown using a selector.
    """
    find_element(page, selector).select_option(value)


def scroll_element_into_view_if_needed(page: Page, selector: str):
    """
    Utility function to scroll an element into view using a selector.
    """
    find_element(page, selector).scroll_into_view_if_needed()


def click_with_retries(page: Page, selector: str, max_retries: int = 3):
    """
    Utility function to Click on an element up to max_retries times.
    """
    for attempt in range(1, max_retries + 1):
        try:
           find_element(page, selector).click()
           print(f"✅ Successful click on attempt {attempt}.")
           return  # Exit the function if successful

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {type(e).__name__}. Retrying...")
            if attempt < max_retries:
                page.wait_for_timeout(2000)  # Wait 2 seconds before the next retry
            else:
                print(f"❌ All {max_retries} attempts failed for locator: {selector}")
                raise


def refresh_page(page: Page):
    """
    Utility function to refresh the current page.
    """
    page.reload()


def get_current_url(page: Page) -> str:
    """
    Utility function to get the current page URL.
    """
    return page.url


def move_to_element(page: Page, selector: str):
    """
    Utility function to move the mouse to an element using a selector.
    """
    find_element(page, selector).hover()


def move_to_element_and_click(page: Page, selector: str):
    """
    Utility function to move the mouse to an element and click it using a selector.
    """
    find_element(page, selector).hover()
    find_element(page, selector).click()


def double_click_on_element(page: Page, selector: str):
    """
    Utility function to double-click on an element using a selector.
    """
    find_element(page, selector).dblclick()
