import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ThreatDatabase() {
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchThreats();
  }, []);

  const fetchThreats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/threats');
      setThreats(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch threat database');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loader"></div>;

  return (
    <div className="threat-database">
      <h1>قاعدة بيانات التهديدات 🚨</h1>
      
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        {threats.length === 0 ? (
          <p>قاعدة البيانات فارغة</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>نوع التهديد</th>
                <th>التوقيع</th>
                <th>الشدة</th>
                <th>الوصف</th>
              </tr>
            </thead>
            <tbody>
              {threats.map((threat) => (
                <tr key={threat.id}>
                  <td>{threat.threat_type}</td>
                  <td><code>{threat.signature.substring(0, 40)}...</code></td>
                  <td>
                    <span className={`risk-level risk-${threat.severity.toLowerCase()}`}>
                      {threat.severity}
                    </span>
                  </td>
                  <td>{threat.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default ThreatDatabase;
