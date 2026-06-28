import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/alerts');
      setAlerts(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch alerts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (alertId) => {
    try {
      await axios.put(`http://localhost:5000/api/alerts/${alertId}/read`);
      fetchAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="loader"></div>;

  return (
    <div className="alerts">
      <h1>الإنذارات 🔔</h1>
      
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        {alerts.length === 0 ? (
          <p>لا توجد إنذارات</p>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className="alert" style={{ marginBottom: '1rem' }}>
              <strong>{alert.alert_type}</strong>: {alert.message}
              <button
                onClick={() => handleMarkAsRead(alert.id)}
                className="btn btn-success"
                style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}
              >
                تحديد كمقروء
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Alerts;
