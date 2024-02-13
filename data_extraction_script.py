# data_extraction_script.py
import pandas as pd

# Charger les données depuis le fichier CSV ou JSON
data = pd.read_csv('linkedin_jobs_data.csv')  # ou pd.read_json('linkedin_jobs_data.json')

# Extraire les titres de poste et les coûts annuels estimés
job_titles = data['job_title']
estimated_costs = data['estimated_annual_cost']

# Afficher les informations extraites
print("Job Titles:", job_titles)
print("Estimated Annual Costs:", estimated_costs)
