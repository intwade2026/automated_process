import re

from playwright.sync_api import Page


NAVIGATION_STEPS = (
    "Configuration Area",
    "Smart Data Stream",
    "Scheduler",
)

SETTINGS_TOOLBOX_ICON_POSITION = (40, 335)


def visible_error_messages(page: Page):
    error_elements = page.locator(
        "[role='alert'], .alert-danger, .alert-error, .error-message, "
        ".error, .toast-error, .text-danger"
    )
    messages = []

    for index in range(error_elements.count()):
        element = error_elements.nth(index)
        if element.is_visible():
            message = element.inner_text().strip()
            if message and message not in messages:
                messages.append(message)

    return messages


def wait_for_loading_to_finish(page: Page):
    loading_indicator = page.get_by_text(
        re.compile(r"^\s*Loading\s*$", re.IGNORECASE)
    )
    loading_indicator.wait_for(state="hidden", timeout=0)


def wait_for_initial_loading_to_finish(page: Page):
    loading_indicator = page.get_by_text(
        re.compile(r"^\s*Loading\s*$", re.IGNORECASE)
    )
    loading_indicator.wait_for(state="visible", timeout=0)
    loading_indicator.wait_for(state="hidden", timeout=0)


def click_navigation_target(page: Page, target, label: str):
    print(f"Navigation : {label}...")
    target.wait_for(state="visible", timeout=60000)
    messages = visible_error_messages(page)
    if messages:
        raise RuntimeError(
            f"Message d'erreur avant « {label} » : {' | '.join(messages)}"
        )

    target.click()

    wait_for_loading_to_finish(page)
    messages = visible_error_messages(page)
    if messages:
        raise RuntimeError(
            f"Message d'erreur après « {label} » : {' | '.join(messages)}"
        )


def click_settings_toolbox_icon(page: Page):
    print("Navigation : icône Settings Toolbox...")
    page.mouse.click(*SETTINGS_TOOLBOX_ICON_POSITION)
    wait_for_loading_to_finish(page)

    messages = visible_error_messages(page)
    if messages:
        raise RuntimeError(
            "Message d'erreur après le clic sur Settings Toolbox : "
            + " | ".join(messages)
        )


def click_navigation_step(page: Page, label: str):
    target = page.get_by_text(
        re.compile(rf"^\s*{re.escape(label)}\s*$", re.IGNORECASE)
    ).filter(visible=True).first
    click_navigation_target(page, target, label)


def follow_navigation(page: Page):
    click_settings_toolbox_icon(page)
    for label in NAVIGATION_STEPS:
        click_navigation_step(page, label)
