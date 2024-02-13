# data_mapping_script.py

# Créer un dictionnaire de mapping
job_costs = {
    "Software Engineer": 80000,
    "Data Scientist": 100000,
    # ... Ajoutez d'autres titres de poste et coûts correspondants
}

# Exemple d'utilisation
job_title = "Software Engineer"
estimated_cost = job_costs.get(job_title, 0)
print(f"Estimated annual cost for {job_title}: ${estimated_cost}")
