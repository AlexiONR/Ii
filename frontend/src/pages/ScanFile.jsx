import React, { useState } from 'react';
import axios from 'axios';

function ScanFile() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleScan = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('الرجاء اختيار ملف');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // إنشاء فحص جديد
      const response = await axios.post('http://localhost:5000/api/scans', {
        scan_type: 'file',
        target: file.name,
      });
      setResult(response.data.data);
    } catch (err) {
      setError('خطأ في الفحص: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scan-file">
      <h1>فحص الملفات 📁</h1>

      <div className="card">
        <form onSubmit={handleScan}>
          <div className="form-group">
            <label>اختر الملف:</label>
            <input
              type="file"
              onChange={handleFileChange}
              disabled={loading}
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading || !file}>
            {loading ? 'جاري الفحص...' : 'فحص الملف'}
          </button>
        </form>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {result && (
        <div className="card">
          <h2>نتائج الفحص</h2>
          <div className="result-info">
            <p><strong>الملف:</strong> {result.target}</p>
            <p><strong>الحالة:</strong> {result.status}</p>
            <p>
              <strong>مستوى الخطر:</strong>
              <span className={`risk-level risk-${result.risk_level.toLowerCase()}`}>
                {result.risk_level}
              </span>
            </p>
            {result.threat_detected && (
              <div className="alert alert-danger">
                ⛔ تم اكتشاف تهديد خطير!
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ScanFile;
