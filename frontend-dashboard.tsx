import React, { useState, useEffect } from 'react';
import { LineChart, XAxis, YAxis, CartesianGrid, Line, Tooltip } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Search, Filter, RefreshCw } from 'lucide-react';

const Dashboard = () => {
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [investmentData, setInvestmentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchInvestmentData = async (companyId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `/api/companies/${companyId}/investment-analysis`,
        {
          headers: {
            'X-API-Key': localStorage.getItem('apiKey')
          }
        }
      );
      
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des données');
      }
      
      const data = await response.json();
      setInvestmentData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCompany) {
      fetchInvestmentData(selectedCompany.id);
    }
  }, [selectedCompany]);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Sélection de l'entreprise */}
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="w-5 h-5" />
              Rechercher une entreprise
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <input
                type="text"
                className="flex-1 p-2 border rounded"
                placeholder="Nom de l'entreprise..."
              />
              <button className="px-4 py-2 bg-blue-600 text-white rounded">
                Rechercher
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Graphique des investissements */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Analyse des investissements</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <RefreshCw className="w-8 h-8 animate-spin" />
              </div>
            ) : investmentData ? (
              <LineChart
                width={600}
                height={300}
                data={Object.entries(investmentData.domain_investments).map(
                  ([domain, data]) => ({
                    domain,
                    score: data.score * 100,
                    jobs: data.job_count
                  })
                )}
              >
                <XAxis dataKey="domain" />
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#8884d8"
                  name="Score d'investissement"
                />
                <Line
                  type="monotone"
                  dataKey="jobs"
                  stroke="#82ca9d"
                  name="Nombre d'offres"
                />
              </LineChart>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500">
                Sélectionnez une entreprise pour voir l'analyse
              </div>
            )}
          </CardContent>
        </Card>

        {/* Statistiques */}
        <Card>
          <CardHeader>
            <CardTitle>Statistiques clés</CardTitle>
          </CardHeader>
          <CardContent>
            {investmentData && (
              <div className="space-y-4">
                <div>
                  <h3 className="font-medium">Domaines principaux</h3>
                  <ul className="mt-2 space-y-2">
                    {investmentData.primary_investment_areas.map(
                      ([domain, data]) => (
                        <li key={domain} className="flex justify-between">
                          <span>{domain}</span>
                          <span className="font-medium">
                            {(data.score * 100).toFixed(1)}%
                          </span>
                        </li>
                      )
                    )}
                  </ul>
                </div>
                <div>
                  <h3 className="font-medium">Score total</h3>
                  <p className="text-2xl font-bold mt-1">
                    {(investmentData.total_investment_score * 100).toFixed(1)}
                  </p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
