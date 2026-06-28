import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({
    total_scans: 0,
    completed_scans: 0,
    threats_detected: 0,
    critical_threats: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/dashboard/stats');
      setStats(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loader"></div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard 📊</h1>
      
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="grid wide">
        <div className="stat-card">
          <h3>إجمالي الفحوصات</h3>
          <div className="stat-value">{stats.total_scans}</div>
        </div>
        
        <div className="stat-card">
          <h3>الفحوصات المكتملة</h3>
          <div className="stat-value">{stats.completed_scans}</div>
        </div>
        
        <div className="stat-card">
          <h3>التهديدات المكتشفة</h3>
          <div className="stat-value">{stats.threats_detected}</div>
        </div>
        
        <div className="stat-card">
          <h3>التهديدات الحرجة</h3>
          <div className="stat-value" style={{ color: '#dc2626' }}>
            {stats.critical_threats}
          </div>
        </div>
      </div>

      <div className="card">
        <h2>مرحباً بك في منصة الأمن السيبراني الدفاعي 🛡️</h2>
        <p>منصة متكاملة للفحص الأمني والكشف عن التهديدات الإلكترونية</p>
        <ul>
          <li>✅ فحص المواقع والروابط المشبوهة</li>
          <li>✅ كشف البرامج الضارة والفيروسات</li>
          <li>✅ تحليل الملفات الخطرة</li>
          <li>✅ قاعدة بيانات تهديدات محدثة</li>
          <li>✅ إنذارات فورية وتقارير مفصلة</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
