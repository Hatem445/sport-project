# Sport Project

مشروع Flask للتجربة والنشر عبر Render.

## تشغيل محلي
1. تثبيت المكتبات:
   pip install -r requirements.txt
2. تشغيل التطبيق:
   flask run

## النشر على Render
- Render بيقرأ requirements.txt و Procfile تلقائيًا.
- أمر التشغيل: gunicorn main:app
