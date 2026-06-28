# منصة الأمن السيبراني الدفاعي - توثيق API

## نظرة عامة
هذه الوثائق توضح جميع نقاط نهاية API المتاحة في المنصة.

## عنوان الخادم
```
http://localhost:5000/api
```

## المصادقة
حالياً، جميع النقاط مفتوحة. في المستقبل، سيتم إضافة مصادقة JWT.

## نقاط النهاية (Endpoints)

### 1. الفحوصات (Scans)

#### الحصول على جميع الفحوصات
```
GET /api/scans?page=1&per_page=10
```

**الاستجابة:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "scan_type": "url",
      "target": "https://example.com",
      "status": "completed",
      "risk_level": "LOW",
      "threat_detected": false,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 100,
  "pages": 10,
  "current_page": 1
}
```

#### إنشاء فحص جديد
```
POST /api/scans
Content-Type: application/json

{
  "scan_type": "url",
  "target": "https://example.com"
}
```

#### الحصول على فحص محدد
```
GET /api/scans/{id}
```

#### تحديث فحص
```
PUT /api/scans/{id}
Content-Type: application/json

{
  "status": "completed",
  "risk_level": "HIGH",
  "threat_detected": true
}
```

### 2. قاعدة بيانات التهديدات (Threats)

#### الحصول على جميع التهديدات
```
GET /api/threats
```

#### إضافة تهديد جديد
```
POST /api/threats
Content-Type: application/json

{
  "threat_type": "malware",
  "signature": "malware_signature_hash",
  "description": "وصف التهديد",
  "severity": "high"
}
```

### 3. الإنذارات (Alerts)

#### الحصول على الإنذارات
```
GET /api/alerts?unread=true
```

#### تحديد الإنذار كمقروء
```
PUT /api/alerts/{id}/read
```

### 4. لوحة التحكم (Dashboard)

#### الحصول على الإحصائيات
```
GET /api/dashboard/stats
```

**الاستجابة:**
```json
{
  "success": true,
  "data": {
    "total_scans": 150,
    "completed_scans": 145,
    "threats_detected": 23,
    "critical_threats": 3,
    "timestamp": "2024-01-01T00:00:00"
  }
}
```

## أكواد الحالة (Status Codes)

- `200` - نجاح
- `201` - تم الإنشاء
- `400` - طلب خاطئ
- `404` - غير موجود
- `500` - خطأ في الخادم

## مستويات الخطر (Risk Levels)

- `SAFE` - آمن تماماً
- `LOW` - منخفض
- `MEDIUM` - متوسط
- `HIGH` - مرتفع
- `CRITICAL` - حرج

## أنواع الفحوصات (Scan Types)

- `url` - فحص الروابط
- `file` - فحص الملفات
- `link` - فحص الروابط المختصرة
