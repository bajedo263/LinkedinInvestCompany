import torch
import torch_geometric
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import Data
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple

class JobMarketGNN(torch.nn.Module):
    def __init__(self, num_features: int, hidden_channels: int, num_classes: int):
        super(JobMarketGNN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, num_classes)
        
    def forward(self, x, edge_index, batch):
        # Premier layer de convolution
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = torch.dropout(x, p=0.2, training=self.training)
        
        # Deuxième layer
        x = self.conv2(x, edge_index)
        x = torch.relu(x)
        
        # Layer final
        x = self.conv3(x, edge_index)
        
        return x

class InvestmentAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.domain_encoder = None
        
    async def prepare_graph_data(self, jobs_data: List[Dict]) -> Data:
        """Prépare les données pour le GNN"""
        # Conversion des offres d'emploi en features
        features = []
        edges = []
        
        for i, job in enumerate(jobs_data):
            # Création des features pour chaque offre
            job_features = self._extract_job_features(job)
            features.append(job_features)
            
            # Création des edges entre offres similaires
            for j in range(i):
                if self._are_jobs_related(jobs_data[j], job):
                    edges.append([i, j])
                    edges.append([j, i])  # Graphe non dirigé
        
        # Conversion en tenseurs PyTorch
        x = torch.FloatTensor(features)
        edge_index = torch.LongTensor(edges).t().contiguous()
        
        return Data(x=x, edge_index=edge_index)
    
    def _extract_job_features(self, job: Dict) -> np.ndarray:
        """Extrait les features pertinentes d'une offre d'emploi"""
        features = []
        
        # Salaire normalisé
        salary_feature = (job.get('salary_min', 0) + job.get('salary_max', 0)) / 2
        features.append(salary_feature)
        
        # One-hot encoding du domaine
        domain_encoded = self._encode_domain(job.get('domain', ''))
        features.extend(domain_encoded)
        
        # Embedding des compétences
        skills_embedding = self._embed_skills(job.get('skills', []))
        features.extend(skills_embedding)
        
        return np.array(features)
    
    async def analyze_company_investments(self, company_id: int) -> Dict:
        """Analyse les investissements d'une entreprise"""
        # Récupération des données
        jobs_data = await self._get_company_jobs(company_id)
        
        # Préparation des données pour le GNN
        graph_data = await self.prepare_graph_data(jobs_data)
        
        # Prédiction avec le modèle
        with torch.no_grad():
            self.model.eval()
            predictions = self.model(graph_data.x, graph_data.edge_index, None)
        
        # Analyse des résultats
        investment_analysis = self._analyze_predictions(predictions, jobs_data)
        
        return investment_analysis
    
    def _analyze_predictions(
        self, 
        predictions: torch.Tensor, 
        jobs_data: List[Dict]
    ) -> Dict:
        """Analyse les prédictions du modèle"""
        # Conversion des prédictions en scores d'investissement
        scores = torch.softmax(predictions, dim=1).numpy()
        
        # Agrégation par domaine
        domain_investments = {}
        for i, job in enumerate(jobs_data):
            domain = job.get('domain', 'Unknown')
            if domain not in domain_investments:
                domain_investments[domain] = {
                    'score': 0,
                    'job_count': 0,
                    'avg_salary': 0,
                    'key_skills': set()
                }
            
            domain_investments[domain]['score'] += scores[i].mean()
            domain_investments[domain]['job_count'] += 1
            domain_investments[domain]['avg_salary'] += (
                job.get('salary_min', 0) + job.get('salary_max', 0)
            ) / 2
            domain_investments[domain]['key_skills'].update(job.get('skills', []))
        
        # Normalisation des scores
        for domain in domain_investments:
            info = domain_investments[domain]
            info['score'] /= info['job_count']
            info['avg_salary'] /= info['job_count']
            info['key_skills'] = list(info['key_skills'])
        
        return {
            'domain_investments': domain_investments,
            'total_investment_score': sum(
                d['score'] * d['job_count'] 
                for d in domain_investments.values()
            ),
            'primary_investment_areas': sorted(
                domain_investments.items(),
                key=lambda x: x[1]['score'] * x[1]['job_count'],
                reverse=True
            )[:3]
        }

    async def train_model(self, training_data: List[Dict]):
        """Entraîne le modèle GNN"""
        graph_data = await self.prepare_graph_data(training_data)
        
        # Configuration de l'entraînement
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        criterion = torch.nn.CrossEntropyLoss()
        
        self.model.train()
        for epoch in range(100):
            optimizer.zero_grad()
            out = self.model(graph_data.x, graph_data.edge_index, None)
            loss = criterion(out, graph_data.y)
            loss.backward()
            optimizer.step()
