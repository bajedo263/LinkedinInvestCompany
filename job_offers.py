import csv

def import_data(file_path):
    job_offers = []
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            job_offers.append(row)
    
    return job_offers

# Exemple d'utilisation
job_offers = import_data('job_offers.csv')
