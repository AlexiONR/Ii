"""وحدة فحص الأمان"""

import requests
import hashlib
from urllib.parse import urlparse
import re
from datetime import datetime

class SecurityScanner:
    """فئة فحص الأمان المتقدمة"""
    
    def __init__(self):
        self.phishing_keywords = [
            'verify', 'confirm', 'update', 'click here', 'urgent',
            'account', 'password', 'secure', 'validate'
        ]
        self.malicious_extensions = [
            '.exe', '.bat', '.cmd', '.com', '.pif', '.scr',
            '.vbs', '.js', '.jar', '.zip', '.rar'
        ]
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 'short.link'
        ]
    
    def scan_url(self, url):
        """فحص رابط URL"""
        result = {
            'url': url,
            'is_safe': True,
            'threats': [],
            'score': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # التحقق من صيغة الرابط
            parsed = urlparse(url)
            if not parsed.scheme:
                result['threats'].append('Missing URL scheme (http/https)')
                result['score'] += 10
            
            # فحص اسم النطاق المريب
            domain = parsed.netloc.lower()
            if self._is_suspicious_domain(domain):
                result['threats'].append('Suspicious domain detected')
                result['score'] += 30
            
            # فحص محتوى الرابط
            if any(keyword in url.lower() for keyword in self.phishing_keywords):
                result['threats'].append('Phishing keywords detected')
                result['score'] += 25
            
            # فحص طول الرابط
            if len(url) > 100:
                result['threats'].append('Unusually long URL')
                result['score'] += 5
            
            # محاولة الوصول إلى الرابط
            try:
                response = requests.head(url, timeout=5, allow_redirects=False)
                result['status_code'] = response.status_code
                
                # فحص رؤوس الأمان
                if 'X-Frame-Options' not in response.headers:
                    result['threats'].append('Missing X-Frame-Options header')
                    result['score'] += 5
                
                if 'X-Content-Type-Options' not in response.headers:
                    result['threats'].append('Missing X-Content-Type-Options header')
                    result['score'] += 5
            
            except requests.exceptions.RequestException as e:
                result['threats'].append(f'Connection error: {str(e)}')
                result['score'] += 10
        
        except Exception as e:
            result['error'] = str(e)
            result['score'] = 50
        
        # تحديد مستوى الخطر
        result['is_safe'] = result['score'] < 30
        if result['score'] >= 70:
            result['risk_level'] = 'CRITICAL'
        elif result['score'] >= 50:
            result['risk_level'] = 'HIGH'
        elif result['score'] >= 30:
            result['risk_level'] = 'MEDIUM'
        else:
            result['risk_level'] = 'LOW'
        
        return result
    
    def scan_file(self, filename, file_hash=None):
        """فحص الملف"""
        result = {
            'filename': filename,
            'is_safe': True,
            'threats': [],
            'score': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # فحص امتداد الملف
            extension = filename.lower().split('.')[-1]
            if f'.{extension}' in self.malicious_extensions:
                result['threats'].append(f'Potentially dangerous file extension: .{extension}')
                result['score'] += 50
            
            # فحص أسماء الملفات المريبة
            suspicious_names = ['virus', 'malware', 'trojan', 'ransomware', 'spyware']
            if any(name in filename.lower() for name in suspicious_names):
                result['threats'].append('Suspicious filename pattern detected')
                result['score'] += 40
            
            # فحص حجم الملف (إن أمكن)
            # يمكن إضافة فحص YARA هنا
            
        except Exception as e:
            result['error'] = str(e)
        
        # تحديد مستوى الخطر
        result['is_safe'] = result['score'] < 30
        if result['score'] >= 70:
            result['risk_level'] = 'CRITICAL'
        elif result['score'] >= 50:
            result['risk_level'] = 'HIGH'
        elif result['score'] >= 30:
            result['risk_level'] = 'MEDIUM'
        else:
            result['risk_level'] = 'LOW'
        
        return result
    
    def scan_link(self, link):
        """فحص الرابط المختصر"""
        result = {
            'link': link,
            'is_shortened': False,
            'threats': [],
            'score': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            parsed = urlparse(link)
            domain = parsed.netloc.lower()
            
            # فحص الرابط المختصر
            if any(short_domain in domain for short_domain in self.suspicious_domains):
                result['is_shortened'] = True
                result['threats'].append('Shortened URL detected (may hide malicious destination)')
                result['score'] += 30
            
            # محاولة توسيع الرابط
            try:
                response = requests.head(link, timeout=5, allow_redirects=True)
                result['final_url'] = response.url
                result['redirect_chain'] = len(response.history)
                
                if len(response.history) > 3:
                    result['threats'].append('Multiple redirects detected')
                    result['score'] += 20
            
            except Exception as e:
                result['error'] = str(e)
        
        except Exception as e:
            result['error'] = str(e)
        
        # تحديد مستوى الخطر
        result['is_safe'] = result['score'] < 30
        if result['score'] >= 70:
            result['risk_level'] = 'CRITICAL'
        elif result['score'] >= 50:
            result['risk_level'] = 'HIGH'
        elif result['score'] >= 30:
            result['risk_level'] = 'MEDIUM'
        else:
            result['risk_level'] = 'LOW'
        
        return result
    
    def _is_suspicious_domain(self, domain):
        """التحقق من كون النطاق مريب"""
        suspicious_patterns = [
            r'^\d+\.\d+\.\d+\.\d+',  # IP address
            r'bit\.ly', 'tinyurl', 'goo\.gl',  # URL shorteners
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, domain):
                return True
        
        return False
    
    def calculate_risk_score(self, threats_count, severity_levels):
        """حساب درجة المخاطرة"""
        base_score = len(threats_count) * 10
        severity_score = sum([10 if s == 'high' else 5 if s == 'medium' else 2 for s in severity_levels])
        return min(100, base_score + severity_score)
