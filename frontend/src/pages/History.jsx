import React, { useState, useEffect } from 'react';
import axios from 'axios';

function History() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/scans');
      setScans(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch scan history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loader"></div>;

  return (
    <div className="history">
      <h1>سجل الفحوصات 📜</h1>
      
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        {scans.length === 0 ? (
          <p>لا توجد فحوصات بعد</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>المعرف</th>
                <th>النوع</th>
                <th>الهدف</th>
                <th>الحالة</th>
                <th>مستوى الخطر</th>
                <th>التاريخ</th>
              </tr>
            </thead>
            <tbody>
              {scans.map((scan) => (
                <tr key={scan.id}>
                  <td>#{scan.id}</td>
                  <td>{scan.scan_type}</td>
                  <td>{scan.target.substring(0, 50)}...</td>
                  <td>{scan.status}</td>
                  <td>
                    <span className={`risk-level risk-${scan.risk_level.toLowerCase()}`}>
                      {scan.risk_level}
                    </span>
                  </td>
                  <td>{new Date(scan.created_at).toLocaleDateString('ar-SA')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default History;
