def calculate_total_investment(job_offers):
    total_investment = {}
    
    for offer in job_offers:
        company = offer['company']
        cost = float(offer['estimated_cost'])
        
        if company in total_investment:
            total_investment[company] += cost
        else:
            total_investment[company] = cost
    
    return total_investment

# Exemple d'utilisation
total_investment = calculate_total_investment(job_offers)
