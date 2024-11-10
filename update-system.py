from celery import Celery
from celery.schedules import crontab
from typing import Optional, List, Dict
import logging
from datetime import datetime, timedelta
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Configuration Celery
celery_app = Celery(
    'job_market_updates',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1'
)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crawler = None
        self.analyzer = None

    async def initialize(self):
        """Initialise les composants nécessaires"""
        self.crawler = JobCrawler()
        self.analyzer = InvestmentAnalyzer()
        await self.analyzer.initialize_model()

    async def update_company_data(self, company_id: Optional[int] = None):
        """Met à jour les données pour une entreprise ou toutes les entreprises"""
        try:
            if company_id:
                companies = [await self.get_company(company_id)]
            else:
                companies = await self.get_all_companies()

            for company in companies:
                await self._process_company_update(company)

        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour: {str(e)}")
            raise

    async def _process_company_update(self, company: Dict):
        """Traite la mise à jour pour une entreprise spécifique"""
        logger.info(f"Mise à jour des données pour {company['name']}")

        # Collecte des nouvelles offres
        new_jobs = await self.crawler.collect_company_jobs(company['id'])
        
        # Mise à jour de la base de données
        await self._update_job_database(company['id'], new_jobs)
        
        # Mise à jour de l'analyse
        await self._update_analysis(company['id'])

    async def _update_job_database(self, company_id: int, new_jobs: List[Dict]):
        """Met à jour la base de données avec les nouvelles offres"""
        for job in new_jobs:
            # Vérifie si l'offre existe déjà
            existing_job = await self._get_existing_job(job['source_url'])
            
            if existing_job:
                # Met à jour l'offre existante
                await self._update_existing_job(existing_job['id'], job)
            else:
                # Crée une nouvelle offre
                await self._create_new_job(company_id, job)

    async def _update_analysis(self, company_id: int):
        """Met à jour l'analyse des investissements"""
        try:
            # Récupère les données mises à jour
            jobs = await self._get_company_jobs(company_id)
            
            # Effectue l'analyse
            analysis = await self.analyzer.analyze_company_investments(jobs)
            
            # Stocke les résultats
            await self._store_analysis_results(company_id, analysis)
            
            logger.info(f"Analyse mise à jour pour company_id: {company_id}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {str(e)}")
            raise

# Configuration des tâches périodiques Celery
@celery_app.task
def scheduled_update():
    """Tâche périodique de mise à jour"""
    async def run_update():
        async with get_async_session() as session:
            manager = UpdateManager(session)
            await manager.initialize()
            await manager.update_company_data()

    asyncio.run(run_update())

# Configuration des tâches périodiques
celery_app.conf.beat_schedule = {
    'weekly-update': {
        'task': 'update_system.scheduled_update',
        'schedule': crontab(day_of_week='monday', hour=0, minute=0),
    },
}

# API endpoints pour les mises à jour
async def trigger_update(company_id: Optional[int] = None):
    """Endpoint pour déclencher une mise à jour manuelle"""
    async with get_async_session() as session:
        manager = UpdateManager(session)
        await manager.initialize()
        await manager.update_company_data(company_id)
        
    return {"status": "success", "message": "Mise à jour déclenchée"}

async def get_update_status(company_id: Optional[int] = None):
    """Récupère le statut de la dernière mise à jour"""
    async with get_async_session() as session:
        query = select(UpdateLog).order_by(UpdateLog.created_at.desc())
        if company_id:
            query = query.filter(UpdateLog.company_id == company_id)
        result = await session.execute(query)
        log = result.first()
        
        if not log:
            return {"status": "unknown", "last_update": None}
            
        return {
            "status": log.status,
            "last_update": log.created_at,
            "next_update": log.created_at + timedelta(days=7)
        }
