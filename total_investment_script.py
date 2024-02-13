# total_investment_script.py
import pandas as pd

# Charger les données depuis le fichier CSV ou JSON
data = pd.read_csv('linkedin_jobs_data.csv')  # ou pd.read_json('linkedin_jobs_data.json')

# Calculer l'investissement total par entreprise
total_investment = data.groupby('company')['estimated_annual_cost'].sum()

# Afficher l'investissement total par entreprise
print("Total Investment by Company:")
print(total_investment)
