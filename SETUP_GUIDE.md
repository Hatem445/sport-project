# 🚀 دليل البدء السريع - FitLife AI

## تثبيت وتشغيل الموقع

### الخطوة 1: تثبيت Python والمكتبات

```bash
# التأكد من وجود Python 3.8+
python --version

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt
```

### الخطوة 2: تنظيف قاعدة البيانات (اختياري)

```bash
# احذف ملف قاعدة البيانات القديمة إن وجد
del fitness_ai.db

# أو استخدم الأمر التالي على Linux/Mac:
# rm fitness_ai.db
```

### الخطوة 3: تشغيل الخادم

```bash
# من مجلد المشروع
python app.py

# سيظهر:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### الخطوة 4: فتح الموقع

افتح متصفحك واذهب إلى:
```
http://localhost:5000
```

---

## 🔐 إعدادات الأمان (للإنتاج)

قبل نشر الموقع على الإنترنت:

1. **غير مفتاح السري**
```python
# في app.py
app.config['SECRET_KEY'] = 'YOUR_SECURE_KEY_HERE'
```

2. **استخدم HTTPS**
```bash
# استخدم Let's Encrypt أو خدمة مماثلة
```

3. **أضف متغيرات البيئة**
```bash
# أنشئ ملف .env
FLASK_ENV=production
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
SMS_API_KEY=your_sms_api_key
```

---

## 📱 إعداد خدمة الرسائل SMS

### اختيار مزود الخدمة

#### خيار 1: Twilio (موصى به)
```python
# في notifications.py
from twilio.rest import Client

client = Client(account_sid, auth_token)
```

#### خيار 2: AWS SNS
```python
import boto3
sns_client = boto3.client('sns')
```

#### خيار 3: محاكاة (للاختبار)
```python
# حالياً تم تفعيل نسخة محاكاة للتطوير
```

### تفعيل الرسائل الحقيقية
```python
# غير في notifications.py:
def send(self, phone_number, message):
    # استخدم API حقيقية بدلاً من المحاكاة
    client.messages.create(
        body=message,
        from_="+1234567890",
        to=phone_number
    )
```

---

## 🗄️ قاعدة البيانات

### عرض قاعدة البيانات

```bash
# استخدم SQLite Browser أو:
pip install sqlite-web
sqlite_web fitness_ai.db
```

### عمل نسخة احتياطية

```bash
# Windows
copy fitness_ai.db fitness_ai_backup.db

# Linux/Mac
cp fitness_ai.db fitness_ai_backup.db
```

### استعادة النسخة

```bash
# استبدل الملف القديم بالنسخة الاحتياطية
copy fitness_ai_backup.db fitness_ai.db
```

---

## 🖥️ أوامر مفيدة

### تشغيل الخادم في وضع الإنتاج

```bash
# استخدم gunicorn بدلاً من Flask
pip install gunicorn
gunicorn app:app
```

### تشغيل مع Nginx (Linux)

```bash
# تثبيت Nginx
sudo apt-get install nginx

# إنشاء ملف إعدادات
# /etc/nginx/sites-available/fitlife

# تشغيل
sudo systemctl start nginx
```

### جدولة المهام (Cron Jobs)

```bash
# تنظيف النوتيفيكاشنات القديمة (كل يوم)
0 2 * * * python /path/to/cleanup.py

# إرسال التقارير الأسبوعية
0 9 * * 1 python /path/to/send_reports.py
```

---

## 🐛 استكشاف الأخطاء

### مشكلة: الصفحة البيضاء

**الحل:**
```bash
# تحقق من سجلات الأخطاء
python app.py  # سيعرض الأخطاء مباشرة

# تمكين وضع التصحيح المتقدم
python -u app.py
```

### مشكلة: لا تعمل الرسائل SMS

**الحل:**
```python
# تحقق من رقم الهاتف
phone = "+966501234567"  # صيغة صحيحة

# تحقق من بيانات الاعتماد
print(SMS_API_KEY)
```

### مشكلة: بطء التحميل

**الحل:**
```python
# أضف تخزين مؤقت
pip install redis
# ثم استخدم Flask-Caching
```

---

## 📊 الإحصائيات والمراقبة

### مراقبة الأداء

```python
# أضف تسجيل الأخطاء
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
```

### إحصائيات الاستخدام

```sql
-- عدد المستخدمين النشطين
SELECT COUNT(*) FROM user WHERE last_login > date('now', '-7 days');

-- إجمالي التمارين
SELECT COUNT(*) FROM exercise;

-- متوسط السعرات المحروقة
SELECT AVG(calories) FROM exercise;
```

---

## 🎯 قائمة للتحقق من الجاهزية

### قبل الذهاب للإنتاج

- [ ] اختبار جميع الميزات الأساسية
- [ ] التحقق من أمان كلمات المرور
- [ ] اختبار نظام الإشعارات
- [ ] عمل نسخة احتياطية من قاعدة البيانات
- [ ] تعيين اسم نطاق (Domain)
- [ ] تثبيت شهادة SSL/HTTPS
- [ ] إعداد CDN للملفات الثابتة
- [ ] إعداد البريد الإلكتروني للإشعارات
- [ ] اختبار الأداء والحمل
- [ ] توثيق API كاملة

---

## 📞 الدعم الفني

### الأخطاء الشائعة

| الخطأ | السبب | الحل |
|-------|--------|------|
| `ModuleNotFoundError` | مكتبة غير مثبتة | `pip install -r requirements.txt` |
| `Address already in use` | المنفذ مشغول | غير المنفذ أو أغلق العملية |
| `Database locked` | قاعدة بيانات مقفلة | أعد تشغيل التطبيق |
| `SMS not sending` | بيانات اعتماد خاطئة | تحقق من API key |

---

## 🔄 التحديثات والصيانة

### تحديث البرنامج

```bash
# احذر النسخة الحالية
git stash

# اسحب التحديثات الجديدة
git pull origin main

# أعد تثبيت المكتبات
pip install -r requirements.txt --upgrade

# أعد الخادم
python app.py
```

### جدول الصيانة المقترح

- **يومي**: مراقبة الأداء والأخطاء
- **أسبوعي**: عمل نسخة احتياطية
- **شهري**: تحديث المكتبات والأمان
- **سنوي**: مراجعة شاملة وتحسينات

---

## 💡 نصائح للتطوير

### استخدم أداة التطوير الحديثة

```bash
# Chrome DevTools
# اضغط F12 في المتصفح

# تفعيل وضع التطوير في Flask
FLASK_ENV=development python app.py
```

### اختبر الميزات الجديدة

```bash
# استخدم Postman لاختبار API
# https://www.postman.com/

# أو استخدم curl
curl -X GET http://localhost:5000/api/user/profile
```

### تتبع الأخطاء

```python
# أضف docstrings
def add_exercise():
    """
    إضافة تمرين جديد
    
    Request:
        - name: اسم التمرين
        - duration: المدة
    
    Response:
        - success: boolean
    """
    pass
```

---

## 🎓 موارد تعليمية

### مراجع مفيدة
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [REST API Best Practices](https://restfulapi.net/)
- [JavaScript ES6+](https://developer.mozilla.org/en-US/docs/Web/JavaScript/)

---

**هل تحتاج مساعدة إضافية؟ تذكر - الخطأ يعلمنا!** 🚀

استمتع بتطوير الموقع! 💚
