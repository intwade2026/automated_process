
from playwright.sync_api import sync_playwright

from authentication import login
from config import load_config
from navigation import follow_navigation, visible_error_messages


def main():
    config = load_config()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        page = browser.new_page(viewport={"width": 1440, "height": 800})

        try:
            login(page, config)

            print("URL actuelle :", page.url)
            print("Titre :", page.title())

            follow_navigation(page)

            messages = visible_error_messages(page)
            if messages:
                print("Message(s) d'erreur détecté(s) :")
                for message in messages:
                    print(f"- {message}")
            else:
                print("Aucun message d'erreur visible détecté sur la page.")

            page.screenshot(path="apres_parcours.png", full_page=True)
            input("Parcours terminé. Appuie sur Entrée pour fermer...")

        except Exception as error:
            print("ERREUR :", error)

            for message in visible_error_messages(page):
                print("Message d'erreur de l'application :", message)

            page.screenshot(path="erreur_raid.png", full_page=True)
            input("Appuie sur Entrée pour fermer...")

        finally:
            browser.close()


if __name__ == "__main__":
    main()
