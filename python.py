import json

# Sample data
data = '''
[
    {
        "job_title": "Software Engineer",
        "estimated_annual_cost": 100000
    },
    {
        "job_title": "Data Analyst",
        "estimated_annual_cost": 80000
    },
    {
        "job_title": "Product Manager",
        "estimated_annual_cost": 120000
    }
]
'''

# Parse the JSON data
jobs = json.loads(data)

# Extract job titles and estimated annual costs
job_titles = [job["job_title"] for job in jobs]
estimated_costs = [job["estimated_annual_cost"] for job in jobs]

# Print the extracted information
print("Job Titles:", job_titles)
print("Estimated Annual Costs:", estimated_costs)
