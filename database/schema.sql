-- قاعدة بيانات الأمن السيبراني

-- جدول الفحوصات
CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    scan_type VARCHAR(50) NOT NULL,
    target VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    risk_level VARCHAR(20) DEFAULT 'unknown',
    threat_detected BOOLEAN DEFAULT false,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول قاعدة بيانات التهديدات
CREATE TABLE IF NOT EXISTS threat_database (
    id SERIAL PRIMARY KEY,
    threat_type VARCHAR(100) NOT NULL,
    signature VARCHAR(500) UNIQUE NOT NULL,
    description TEXT,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول الإنذارات
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id),
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول سجلات المستخدمين (اختياري)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول الفحوصات المجدولة
CREATE TABLE IF NOT EXISTS scheduled_scans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    target VARCHAR(500) NOT NULL,
    scan_type VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_scan TIMESTAMP,
    next_scan TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- الفهارس
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_created_at ON scans(created_at);
CREATE INDEX idx_threats_type ON threat_database(threat_type);
CREATE INDEX idx_alerts_scan_id ON alerts(scan_id);
CREATE INDEX idx_alerts_severity ON alerts(severity);
