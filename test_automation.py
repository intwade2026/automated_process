import re
import unittest

from authentication import wait_for_application
from navigation import (
    NAVIGATION_STEPS,
    SETTINGS_TOOLBOX_ICON_POSITION,
    follow_navigation,
)


class FakeLocator:
    def __init__(self, page, label, visible=True):
        self.page = page
        self.label = label
        self.visible = visible

    @property
    def first(self):
        return self

    def filter(self, **kwargs):
        if kwargs.get("visible") and not self.visible:
            return FakeLocator(self.page, self.label, visible=False)
        return self

    def count(self):
        return int(self.visible)

    def wait_for(self, state, timeout):
        self.page.waits.append((self.label, state, timeout))

    def click(self):
        self.page.clicks.append(self.label)
        if self.page.error_after_click and len(self.page.clicks) == 1:
            self.page.error_message = self.page.error_after_click


class FakeMouse:
    def __init__(self, page):
        self.page = page

    def click(self, x, y):
        self.page.clicks.append("Settings Toolbox icon")
        self.page.mouse_position = (x, y)
        if self.page.error_after_click:
            self.page.error_message = self.page.error_after_click


class FakeErrorElement:
    def __init__(self, message):
        self.message = message

    def is_visible(self):
        return True

    def inner_text(self):
        return self.message


class FakeErrorElements:
    def __init__(self, message):
        self.message = message

    def count(self):
        return 1 if self.message else 0

    def nth(self, index):
        return FakeErrorElement(self.message)


class FakePage:
    def __init__(self, error_message=None, error_after_click=None):
        self.clicks = []
        self.waits = []
        self.error_message = error_message
        self.error_after_click = error_after_click
        self.mouse = FakeMouse(self)

    def locator(self, selector):
        if selector.startswith("[role='alert']"):
            return FakeErrorElements(self.error_message)
        raise AssertionError(f"Unexpected CSS locator: {selector}")

    def get_by_text(self, text, exact=None):
        if isinstance(text, re.Pattern):
            if text.fullmatch("Loading"):
                return FakeLocator(self, "Loading")

            candidates = (
                "Configuration Area",
                "Smart Data Stream",
                "Scheduler",
            )
            matches = [label for label in candidates if text.search(label)]
            if len(matches) != 1:
                raise AssertionError(f"Unexpected text locator: {text.pattern}")
            return FakeLocator(self, matches[0])

        raise AssertionError(f"Unexpected text locator: {text}")


class AutomationTests(unittest.TestCase):
    def test_application_waits_for_loading_before_navigation(self):
        page = FakePage()

        wait_for_application(page)

        self.assertEqual(
            page.waits,
            [
                ("Loading", "visible", 0),
                ("Loading", "hidden", 0),
            ],
        )

    def test_navigation_clicks_toolbox_icon_then_follows_steps(self):
        page = FakePage()

        follow_navigation(page)

        expected = [
            "Settings Toolbox icon",
            *NAVIGATION_STEPS,
        ]
        self.assertEqual(
            [label.casefold() for label in page.clicks],
            [label.casefold() for label in expected],
        )
        self.assertEqual(page.mouse_position, SETTINGS_TOOLBOX_ICON_POSITION)

    def test_navigation_stops_and_reports_visible_application_error(self):
        page = FakePage(error_after_click="Application error")

        with self.assertRaisesRegex(RuntimeError, "Application error"):
            follow_navigation(page)

        self.assertEqual(page.clicks, ["Settings Toolbox icon"])


if __name__ == "__main__":
    unittest.main()
