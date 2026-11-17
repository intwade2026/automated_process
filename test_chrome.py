
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    page = browser.new_page()

    page.goto("https://www.google.com")

    print("Chrome est opérationnel !")
    print("Titre :", page.title())

    input("Appuie sur Entrée pour fermer...")

    browser.close()
