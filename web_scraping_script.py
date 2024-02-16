import requests
from bs4 import BeautifulSoup
import csv
import json

def scrape_linkedin_jobs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        # Exemple : trouver les éléments d'offres d'emploi, ajustez selon la structure HTML
        job_elements = soup.find_all('div', class_='job-element-class')

        for job_element in job_elements:
            job_data = {
                'title': job_element.find('span', class_='job-card-list__title').text,
                'company': job_element.find('span', class_='job-card-container__primary-description').text,
                'location': job_element.find('span', class_='job-card-container__primary-description').text
                'date': job_element.find('span', class_='job-card-container__footer-item').text
                # Ajoutez d'autres champs nécessaires
            }
            jobs.append(job_data)

        return jobs
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    linkedin_url = 'https://www.linkedin.com/jobs/'
    jobs_data = scrape_linkedin_jobs(linkedin_url)

    if jobs_data:
        write_to_csv(jobs_data, 'linkedin_jobs_data.csv')
        # ou
        write_to_json(jobs_data, 'linkedin_jobs_data.json')
