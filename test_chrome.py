
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False
        )

        try:
            page = browser.new_page()
            page.goto("https://www.google.com")

            print("Chrome est opérationnel !")
            print("Titre :", page.title())

            input("Appuie sur Entrée pour fermer...")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
