from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import json
import time

def login_to_linkedin(username, password):
    # Utilisez le navigateur Chrome (téléchargez le driver sur https://sites.google.com/a/chromium.org/chromedriver/)
    driver = webdriver.Chrome(executable_path='/chemin/vers/chromedriver')

    # Ouvrir la page de connexion LinkedIn
    driver.get('https://www.linkedin.com/login')

    # Remplir le formulaire de connexion
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Attendre que la page de connexion se charge complètement
    WebDriverWait(driver, 10).until(EC.title_contains('LinkedIn'))

    return driver

def scrape_linkedin_jobs(driver, url):
    # Ouvrir la page LinkedIn Jobs après la connexion
    driver.get(url)
    time.sleep(5)  # Attendre quelques secondes pour permettre le chargement complet de la page

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = []

    # ... (la suite du code reste inchangée)

if __name__ == "__main__":
    linkedin_url = 'https://www.linkedin.com/jobs/'
    linkedin_username = 'VotreNomUtilisateurLinkedIn'
    linkedin_password = 'VotreMotDePasseLinkedIn'

    # Connexion à LinkedIn
    driver = login_to_linkedin(linkedin_username, linkedin_password)

    # Scraper les offres d'emploi après la connexion
    jobs_data = scrape_linkedin_jobs(driver, linkedin_url)

    if jobs_data:
        write_to_csv(jobs_data, 'linkedin_jobs_data.csv')
        # ou
        write_to_json(jobs_data, 'linkedin_jobs_data.json')

    # Fermer le navigateur après le scraping
    driver.quit()
