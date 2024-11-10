import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { RefreshCw, Check, AlertTriangle, Clock } from 'lucide-react';

const UpdateMonitor = ({ companyId }) => {
  const [updateStatus, setUpdateStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStatus = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `/api/updates/status${companyId ? `?company_id=${companyId}` : ''}`,
        {
          headers: {
            'X-API-Key': localStorage.getItem('apiKey')
          }
        }
      );

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération du statut');
      }

      const data = await response.json();
      setUpdateStatus(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const triggerUpdate = async () => {
    try {
      const response = await fetch(
        '/api/updates/trigger',
        {
          method: 'POST',
          headers: {
            'X-API-Key': localStorage.getItem('apiKey'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ company_id: companyId })
        }
      );

      if (!response.ok) {
        throw new Error('Erreur lors du déclenchement de la mise à jour');
      }

      await fetchStatus();
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Rafraîchissement toutes les 30 secondes
    return () => clearInterval(interval);
  }, [companyId]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <RefreshCw className="w-5 h-5" />
          Statut des mises à jour
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center p-4">
            <RefreshCw className="w-6 h-6 animate-spin" />
          </div>
        ) : error ? (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : updateStatus && (
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              {updateStatus.status === 'success' ? (
                <Check className="w-5 h-5 text-green-500" />
              ) : updateStatus.status === 'pending' ? (
                <Clock className="w-5 h-5 text-yellow-500" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-red-500" />
              )}
              <span className="font-medium">
                {updateStatus.status === 'success'
                  ? 'Données à jour'
                  : updateStatus.status === 'pending'
                  ? 'Mise à jour en cours'
                  : 'Mise à jour nécessaire'}
              </span>
            </div>

            <div className="text-sm text-gray-600 space-y-1">
              <p>
                Dernière mise à jour :{' '}
                {updateStatus.last_update
                  ? new Date(updateStatus.last_update).toLocaleString()
                  : 'Jamais'}
              </p>
              <p>
                Prochaine mise à jour :{' '}
                {updateStatus.next_update
                  ? new Date(updateStatus.next_update).toLocaleString()
                  : 'Non planifiée'}
              </p>
            </div>

            <button
              onClick={triggerUpdate}
              disabled={updateStatus.status === 'pending'}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
            >
              Forcer la mise à jour
            </button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default UpdateMonitor;
