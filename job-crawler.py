from scrapy import Spider, Request
from datetime import datetime
import json
from typing import Dict, Any
import logging

class LinkedInJobSpider(Spider):
    name = 'linkedin_jobs'
    allowed_domains = ['linkedin.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': 'Mozilla/5.0 (compatible; JobAnalytics/1.0;)'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def start_requests(self):
        # URL de base pour la recherche d'emploi LinkedIn
        base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        
        # Paramètres de recherche initiaux
        params = {
            'keywords': '',
            'location': 'France',
            'start': 0
        }
        
        yield Request(
            url=f"{base_url}?{self.build_params(params)}",
            callback=self.parse,
            meta={'params': params}
        )

    def parse(self, response):
        try:
            jobs = response.xpath('//li[@class="job-result-card"]')
            
            for job in jobs:
                yield {
                    'job_id': job.attrib.get('data-id'),
                    'title': self.extract_text(job, './/h3/text()'),
                    'company': self.extract_text(job, './/h4/a/text()'),
                    'location': self.extract_text(job, './/span[@class="job-result-card__location"]/text()'),
                    'posted_date': self.extract_text(job, './/time/text()'),
                    'url': job.xpath('.//a[@class="result-card__full-card-link"]/@href').get(),
                    'collected_at': datetime.utcnow().isoformat()
                }

            # Pagination
            params = response.meta['params']
            params['start'] += 25
            
            if len(jobs) == 25:  # S'il y a encore des résultats
                yield Request(
                    url=f"{self.allowed_domains[0]}?{self.build_params(params)}",
                    callback=self.parse,
                    meta={'params': params}
                )

        except Exception as e:
            self.logger.error(f"Erreur lors du parsing: {str(e)}")

    def extract_text(self, selector, xpath):
        return selector.xpath(xpath).get(default='').strip()

    def build_params(self, params: Dict[str, Any]) -> str:
        return '&'.join(f"{k}={v}" for k, v in params.items())

class JobProcessor:
    def __init__(self):
        self.nlp = None  # À initialiser avec spaCy ou autre

    def process_job(self, job_data):
        """Traite les données d'une offre d'emploi pour extraire les informations pertinentes"""
        processed_data = {
            'original_data': job_data,
            'extracted_skills': self.extract_skills(job_data.get('description', '')),
            'domain_classification': self.classify_domain(job_data),
            'salary_estimation': self.estimate_salary(job_data),
            'investment_indicators': self.extract_investment_indicators(job_data)
        }
        return processed_data

    def extract_skills(self, description):
        # À implémenter : extraction des compétences avec NLP
        pass

    def classify_domain(self, job_data):
        # À implémenter : classification du domaine d'investissement
        pass

    def estimate_salary(self, job_data):
        # À implémenter : estimation des fourchettes de salaire
        pass

    def extract_investment_indicators(self, job_data):
        # À implémenter : identification des indicateurs d'investissement
        pass
