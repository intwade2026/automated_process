
import os
import re

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect

# Chargement des variables d'environnement
load_dotenv()

URL = os.getenv("OM_URL")
USERNAME = os.getenv("OM_USERNAME")
PASSWORD = os.getenv("OM_PASSWORD")

if not all([URL, USERNAME, PASSWORD]):
    raise ValueError("Configuration .env incomplete")


with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    page = browser.new_page()

    try:
        # 1. OUVERTURE DE RAiD
        print("1. Ouverture de RAiD...")

        page.goto(URL, wait_until="domcontentloaded")

        # 2. ATTENTE DU FORMULAIRE
        print("2. Attente du formulaire...")

        username_field = page.get_by_label("Username")
        password_field = page.get_by_label("Password")

        username_field.wait_for(
            state="visible",
            timeout=60000
        )

        password_field.wait_for(
            state="visible",
            timeout=60000
        )

        # 3. REMPLISSAGE DES IDENTIFIANTS
        print("3. Saisie des identifiants...")

        username_field.fill(USERNAME)
        password_field.fill(PASSWORD)

        # 4. ATTENTE DE SIGN IN
        print("4. Attente de la fin du chargement...")

        login_button = page.locator(
            "button.btn.btn-primary[type='submit']"
        )

        expect(login_button).to_have_text(
            re.compile(r"^\s*sign\s*in\s*$", re.IGNORECASE),
            timeout=120000
        )

        expect(login_button).to_be_enabled(
            timeout=30000
        )

        print("5. Bouton Sign In disponible !")

        # 5. CLIQUER SUR SIGN IN
        print("6. Connexion à RAiD...")

        login_button.click()

        print("7. Bouton cliqué. Vérification de la réponse...")

        # Attendre la réponse de l'application
        page.wait_for_timeout(5000)

        print("URL actuelle :", page.url)
        print("Titre :", page.title())

        # Capture après tentative de connexion
        page.screenshot(
            path="apres_connexion.png",
            full_page=True
        )

        input(
            "Vérifie si la page d'accueil est affichée. "
            "Appuie sur Entrée pour fermer..."
        )

    except Exception as e:

        print("ERREUR :", e)

        page.screenshot(
            path="erreur_raid.png",
            full_page=True
        )

        input("Appuie sur Entrée pour fermer...")

    finally:
        browser.close()
