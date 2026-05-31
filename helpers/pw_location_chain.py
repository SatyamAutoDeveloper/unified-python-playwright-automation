
class LocatorDef:
    """
    Stores the chain of locator strategies to be resolved later with a Page object.
    Allows for Playwright chaining (e.g., locating an element inside another element).
    """
    def __init__(self, method_name: str, *args, **kwargs):
        # Store the initial locator strategy
        self.chain = [(method_name, args, kwargs)]

    # --- Built-in Semantic Locators ---
    def get_by_role(self, *args, **kwargs):
        self.chain.append(("get_by_role", args, kwargs))
        return self

    def get_by_text(self, *args, **kwargs):
        self.chain.append(("get_by_text", args, kwargs))
        return self

    def get_by_label(self, *args, **kwargs):
        self.chain.append(("get_by_label", args, kwargs))
        return self

    def get_by_placeholder(self, *args, **kwargs):
        self.chain.append(("get_by_placeholder", args, kwargs))
        return self

    def get_by_alt_text(self, *args, **kwargs):
        self.chain.append(("get_by_alt_text", args, kwargs))
        return self

    def get_by_title(self, *args, **kwargs):
        self.chain.append(("get_by_title", args, kwargs))
        return self

    def get_by_test_id(self, *args, **kwargs):
        self.chain.append(("get_by_test_id", args, kwargs))
        return self

    # --- Generic Locators & Custom Engines (CSS, XPath, Layout, etc.) ---
    def locator(self, *args, **kwargs):
        self.chain.append(("locator", args, kwargs))
        return self

    # --- The Resolver ---
    def resolve(self, page):
        """
        Takes an active Playwright Page object and resolves the stored chain 
        into a real Playwright Locator object.
        """
        target = page
        for method_name, args, kwargs in self.chain:
            # Dynamically call the method (e.g., page.get_by_role(*args, **kwargs))
            func = getattr(target, method_name)
            target = func(*args, **kwargs)
        return target


class LocationChain:
    """
    Static factory class to initiate a locator chain. 
    Import this as LC in your locators file.
    """
    
    # --- Built-in Semantic Locators ---
    @staticmethod
    def get_by_role(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_role", *args, **kwargs)

    @staticmethod
    def get_by_text(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_text", *args, **kwargs)

    @staticmethod
    def get_by_label(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_label", *args, **kwargs)

    @staticmethod
    def get_by_placeholder(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_placeholder", *args, **kwargs)

    @staticmethod
    def get_by_alt_text(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_alt_text", *args, **kwargs)

    @staticmethod
    def get_by_title(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_title", *args, **kwargs)

    @staticmethod
    def get_by_test_id(*args, **kwargs) -> LocatorDef:
        return LocatorDef("get_by_test_id", *args, **kwargs)

    # --- Generic Locators & Custom Engines (CSS, XPath, Layout, etc.) ---
    @staticmethod
    def locator(*args, **kwargs) -> LocatorDef:
        """
        Used for CSS, XPath, pseudo-classes (:has-text), and Layout Selectors (right-of).
        """
        return LocatorDef("locator", *args, **kwargs)