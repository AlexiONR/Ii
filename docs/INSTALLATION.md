# دليل التثبيت

## المتطلبات
- Python 3.8 أو أحدث
- Node.js 14 أو أحدث
- PostgreSQL 12 أو أحدث
- pip (مدير حزم Python)
- npm (مدير حزم Node.js)

## خطوات التثبيت

### 1. استنساخ المستودع
```bash
git clone https://github.com/AlexiONR/Ii.git
cd Ii
```

### 2. إعداد قاعدة البيانات

#### إنشاء قاعدة البيانات
```bash
creatdb cybersecurity_db
```

#### استيراد الجدول
```bash
psql cybersecurity_db < database/schema.sql
```

### 3. إعداد الواجهة الخلفية (Backend)

#### إنشاء البيئة الافتراضية
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows
```

#### تثبيت المكتبات
```bash
pip install -r requirements.txt
```

#### إعداد متغيرات البيئة
```bash
cp config/.env.example .env
# ثم عدّل الملف .env بالقيم الصحيحة
```

#### تشغيل الخادم
```bash
python backend/app.py
```

سيكون متاحاً على: `http://localhost:5000`

### 4. إعداد الواجهة الأمامية (Frontend)

#### تثبيت المكتبات
```bash
npm install
```

#### إنشاء ملف البيئة
```bash
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env.local
```

#### تشغيل الواجهة
```bash
npm start
```

ستكون متاحة على: `http://localhost:3000`

## التحقق من التثبيت

### فحص صحة الخادم
```bash
curl http://localhost:5000/api/health
```

### النتيجة المتوقعة
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "service": "Cybersecurity Scanner"
}
```

## استكشاف الأخطاء

### الخطأ: قاعدة البيانات غير موجودة
```bash
creatdb cybersecurity_db
psql cybersecurity_db < database/schema.sql
```

### الخطأ: رقم الميناء مستخدم
```bash
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows
```

ثم غير رقم الميناء في متغيرات البيئة.

## الخطوات التالية
- اقرأ [توثيق API](API.md)
- استكشف [أمثلة الاستخدام](EXAMPLES.md)
- اطّلع على [دليل التطوير](DEVELOPMENT.md)
