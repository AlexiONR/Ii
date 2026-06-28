from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# إعدادات قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/cybersecurity_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================== نماذج قاعدة البيانات ========================

class Scan(db.Model):
    """نموذج الفحص"""
    __tablename__ = 'scans'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_type = db.Column(db.String(50), nullable=False)  # url, file, link
    target = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, scanning, completed, failed
    risk_level = db.Column(db.String(20), default='unknown')  # safe, low, medium, high, critical
    threat_detected = db.Column(db.Boolean, default=False)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scan_type': self.scan_type,
            'target': self.target,
            'status': self.status,
            'risk_level': self.risk_level,
            'threat_detected': self.threat_detected,
            'details': self.details,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ThreatDatabase(db.Model):
    """قاعدة بيانات التهديدات"""
    __tablename__ = 'threat_database'
    
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(100), nullable=False)  # malware, phishing, etc
    signature = db.Column(db.String(500), unique=True, nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # low, medium, high, critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'threat_type': self.threat_type,
            'signature': self.signature,
            'description': self.description,
            'severity': self.severity,
            'created_at': self.created_at.isoformat()
        }

class Alert(db.Model):
    """نموذج الإنذارات"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'alert_type': self.alert_type,
            'message': self.message,
            'severity': self.severity,
            'read': self.read,
            'created_at': self.created_at.isoformat()
        }

# ======================== المسارات (Routes) ========================

@app.route('/api/health', methods=['GET'])
def health():
    """فحص صحة الخادم"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Cybersecurity Scanner'
    }), 200

@app.route('/api/scans', methods=['GET'])
def get_scans():
    """الحصول على جميع الفحوصات"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    scans = Scan.query.order_by(Scan.created_at.desc()).paginate(
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'success': True,
        'data': [scan.to_dict() for scan in scans.items],
        'total': scans.total,
        'pages': scans.pages,
        'current_page': page
    }), 200

@app.route('/api/scans/<int:scan_id>', methods=['GET'])
def get_scan(scan_id):
    """الحصول على فحص محدد"""
    scan = Scan.query.get(scan_id)
    
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify({
        'success': True,
        'data': scan.to_dict()
    }), 200

@app.route('/api/scans', methods=['POST'])
def create_scan():
    """إنشاء فحص جديد"""
    data = request.get_json()
    
    if not data or 'scan_type' not in data or 'target' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    scan = Scan(
        scan_type=data['scan_type'],
        target=data['target'],
        status='pending'
    )
    
    db.session.add(scan)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': scan.to_dict(),
        'message': 'Scan created successfully'
    }), 201

@app.route('/api/scans/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    """تحديث حالة الفحص"""
    scan = Scan.query.get(scan_id)
    
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    data = request.get_json()
    
    if 'status' in data:
        scan.status = data['status']
    if 'risk_level' in data:
        scan.risk_level = data['risk_level']
    if 'threat_detected' in data:
        scan.threat_detected = data['threat_detected']
    if 'details' in data:
        scan.details = data['details']
    
    scan.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': scan.to_dict(),
        'message': 'Scan updated successfully'
    }), 200

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """الحصول على قاعدة بيانات التهديدات"""
    threats = ThreatDatabase.query.all()
    
    return jsonify({
        'success': True,
        'data': [threat.to_dict() for threat in threats],
        'total': len(threats)
    }), 200

@app.route('/api/threats', methods=['POST'])
def add_threat():
    """إضافة تهديد جديد"""
    data = request.get_json()
    
    if not data or 'threat_type' not in data or 'signature' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    threat = ThreatDatabase(
        threat_type=data['threat_type'],
        signature=data['signature'],
        description=data.get('description'),
        severity=data.get('severity', 'medium')
    )
    
    db.session.add(threat)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': threat.to_dict(),
        'message': 'Threat added successfully'
    }), 201

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """الحصول على الإنذارات"""
    unread_only = request.args.get('unread', False, type=bool)
    
    query = Alert.query
    if unread_only:
        query = query.filter_by(read=False)
    
    alerts = query.order_by(Alert.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [alert.to_dict() for alert in alerts],
        'total': len(alerts)
    }), 200

@app.route('/api/alerts/<int:alert_id>/read', methods=['PUT'])
def mark_alert_read(alert_id):
    """تحديد الإنذار كمقروء"""
    alert = Alert.query.get(alert_id)
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    alert.read = True
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': alert.to_dict(),
        'message': 'Alert marked as read'
    }), 200

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """إحصائيات لوحة التحكم"""
    total_scans = Scan.query.count()
    completed_scans = Scan.query.filter_by(status='completed').count()
    threats_detected = Scan.query.filter_by(threat_detected=True).count()
    critical_threats = Scan.query.filter_by(risk_level='critical').count()
    
    return jsonify({
        'success': True,
        'data': {
            'total_scans': total_scans,
            'completed_scans': completed_scans,
            'threats_detected': threats_detected,
            'critical_threats': critical_threats,
            'timestamp': datetime.utcnow().isoformat()
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """معالج الأخطاء 404"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج الأخطاء 500"""
    return jsonify({'error': 'Internal server error'}), 500

# ======================== تشغيل التطبيق ========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', True)
    )
