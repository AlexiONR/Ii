import React, { useState } from 'react';
import axios from 'axios';

function ScanURL() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!url.trim()) {
      setError('الرجاء إدخال رابط URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // إنشاء فحص جديد
      const response = await axios.post('http://localhost:5000/api/scans', {
        scan_type: 'url',
        target: url,
      });
      setResult(response.data.data);
    } catch (err) {
      setError('خطأ في الفحص: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scan-url">
      <h1>فحص الروابط 🔗</h1>

      <div className="card">
        <form onSubmit={handleScan}>
          <div className="form-group">
            <label>أدخل الرابط (URL):</label>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              disabled={loading}
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'جاري الفحص...' : 'فحص الرابط'}
          </button>
        </form>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {result && (
        <div className="card">
          <h2>نتائج الفحص</h2>
          <div className="result-info">
            <p><strong>الرابط:</strong> {result.target}</p>
            <p><strong>الحالة:</strong> {result.status}</p>
            <p>
              <strong>مستوى الخطر:</strong>
              <span className={`risk-level risk-${result.risk_level.toLowerCase()}`}>
                {result.risk_level}
              </span>
            </p>
            {result.threat_detected && (
              <div className="alert alert-warning">
                ⚠️ تم اكتشاف تهديد محتمل!
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ScanURL;
