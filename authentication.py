import re

from playwright.sync_api import Page, expect

from config import AutomationConfig
from navigation import wait_for_initial_loading_to_finish


def wait_for_application(page: Page):
    print("8. Attente de l'écran de chargement...")
    wait_for_initial_loading_to_finish(page)
    print("9. Écran de chargement terminé.")


def login(page: Page, config: AutomationConfig):
    print("1. Ouverture de RAiD...")
    page.goto(config.url, wait_until="domcontentloaded")

    print("2. Attente du formulaire...")
    username_field = page.get_by_label("Username")
    password_field = page.get_by_label("Password")

    username_field.wait_for(state="visible", timeout=60000)
    password_field.wait_for(state="visible", timeout=60000)

    print("3. Saisie des identifiants...")
    username_field.fill(config.username)
    password_field.fill(config.password)

    print("4. Attente de la fin du chargement...")
    login_button = page.locator("button.btn.btn-primary[type='submit']")

    expect(login_button).to_have_text(
        re.compile(r"^\s*sign\s*in\s*$", re.IGNORECASE),
        timeout=120000,
    )
    expect(login_button).to_be_enabled(timeout=30000)

    print("5. Bouton Sign In disponible !")
    print("6. Connexion à RAiD...")
    login_button.click()

    print("7. Bouton cliqué. Vérification de la réponse...")
    wait_for_application(page)
