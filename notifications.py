"""
نظام الإشعارات والرسائل القصيرة
Notifications and SMS System
"""

from datetime import datetime
import json


class NotificationSystem:
    """نظام الإشعارات والرسائل"""
    
    def __init__(self):
        """تهيئة نظام الإشعارات"""
        self.sms_provider = SMSProvider()
        self.notifications = []
    
    def send_sms(self, phone_number, message):
        """إرسال رسالة قصيرة"""
        try:
            # في بيئة الإنتاج، استخدم APIs حقيقية مثل Twilio أو AWS SNS
            return self.sms_provider.send(phone_number, message)
        except Exception as e:
            print(f"خطأ في إرسال الرسالة: {e}")
            return False
    
    def send_exercise_reminder(self, user, exercise_name, scheduled_time):
        """إرسال تذكير بموعد التمرين"""
        message = f"""
🏋️  تذكير تمرين

لديك تمرين: {exercise_name}
⏰ الموعد: {scheduled_time}

تأكد من حضورك وجهز نفسك للتمرين!

📱 سجل البيانات الصحية بعد التمرين
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'exercise_reminder',
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })
    
    def send_health_alert(self, user, alert_type, alert_message, recommendations):
        """إرسال تنبيه صحي"""
        message = f"""
⚠️  تنبيه صحي

النوع: {alert_type}
الرسالة: {alert_message}

تعليمات عاجلة:
{recommendations}

❌ إذا استمرت الأعراض، استشر طبيباً فوراً
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'health_alert',
            'alert_type': alert_type,
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })
    
    def send_health_summary(self, user, health_summary_data):
        """إرسال ملخص الحالة الصحية اليومية"""
        message = f"""
📊 ملخص الحالة الصحية

📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}

💓 معدل النبض: {health_summary_data.get('heart_rate', 'لم يسجل')} نبضة/دقيقة
🏃 المسافة: {health_summary_data.get('exercises_today', 0)} تمرين اليوم
😴 النوم: {health_summary_data.get('sleep_hours', 'لم يسجل')} ساعات
📈 النتيجة: {health_summary_data.get('health_score', 'فقيد')} / 100

💪 استمر بالانتظام والالتزام!
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'daily_summary',
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })
    
    def send_weekly_report(self, user, weekly_data):
        """إرسال تقرير أسبوعي"""
        message = f"""
📋 التقرير الأسبوعي

🗓️ الأسبوع: {weekly_data.get('week_range')}

📊 الإحصائيات:
• عدد التمارين: {weekly_data.get('total_exercises', 0)}
• إجمالي الوقت: {weekly_data.get('total_duration', 0)} دقيقة
• السعرات المحروقة: {weekly_data.get('total_calories', 0)} سعرة
• متوسط النبض: {weekly_data.get('avg_heart_rate', 'لم يسجل')}
• الوزن التقريبي: {weekly_data.get('avg_weight', 'لم يسجل')} كغم

🎯 الهدف: {weekly_data.get('progress_status', 'مستمر')}

💡 النصيحة: {weekly_data.get('tip', 'استمر بالعمل الجيد!')}
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'weekly_report',
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })
    
    def send_ai_recommendation(self, user, recommendation):
        """إرسال توصية من الذكاء الاصطناعي"""
        message = f"""
🤖 توصية من الذكاء الاصطناعي

الموضوع: {recommendation.get('title')}

الوصف:
{recommendation.get('description')}

التوصية الموصى بها:
{recommendation.get('recommendation')}

درجة الثقة: {recommendation.get('confidence', 0) * 100:.0f}%

{'⚠️ تنبيه: استشر طبيباً متخصصاً' if recommendation.get('requires_doctor') else '✅ متابعة البرنامج'}
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'ai_recommendation',
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })
    
    def send_milestone_notification(self, user, milestone_data):
        """إرسال إخطار عند تحقيق إنجاز"""
        message = f"""
🎉 تهانينا! تم تحقيق إنجاز

🏆 الإنجاز: {milestone_data.get('milestone_name')}

التفاصيل:
{milestone_data.get('description')}

التاريخ: {datetime.now().strftime('%Y-%m-%d')}

⭐ أنت رائع! استمر بهذا الزخم!
        """.strip()
        
        if user.phone:
            self.send_sms(user.phone, message)
        
        self.notifications.append({
            'user_id': user.id,
            'type': 'milestone',
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        })


class SMSProvider:
    """مزود خدمة الرسائل القصيرة"""
    
    def __init__(self):
        """تهيئة مزود الخدمة"""
        # في الإنتاج، أضف معلومات الاعتماد الحقيقية
        self.api_key = "YOUR_SMS_API_KEY"
        self.provider = "twilio"  # أو nexmo, vonage, إلخ
    
    def send(self, phone_number, message):
        """إرسال رسالة (نسخة محاكاة)"""
        # في الإنتاج، استخدم API حقيقية
        # مثال: 
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=message,
        #     from_="+1234567890",
        #     to=phone_number
        # )
        # return message.sid
        
        # للتطوير والاختبار:
        print(f"\n📱 رسالة SMS محاكاة:")
        print(f"إلى: {phone_number}")
        print(f"المحتوى:\n{message}")
        print(f"الحالة: تم الإرسال (محاكاة)")
        print("=" * 50)
        
        return True
    
    @staticmethod
    def validate_phone_number(phone_number):
        """التحقق من صحة رقم الهاتف"""
        # إزالة المسافات والأحرف الخاصة
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # التحقق من الطول (10-15 أرقام عادة)
        if len(clean_number) < 10 or len(clean_number) > 15:
            return False
        
        return clean_number


class PushNotificationSystem:
    """نظام الإشعارات الفورية (Push Notifications)"""
    
    def __init__(self):
        """تهيئة نظام الإشعارات الفورية"""
        self.notifications = []
    
    def send_push_notification(self, user_id, title, body, data=None):
        """إرسال إشعار فوري"""
        notification = {
            'user_id': user_id,
            'title': title,
            'body': body,
            'data': data or {},
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        self.notifications.append(notification)
        # في الإنتاج، استخدم Firebase Cloud Messaging أو خدمة مماثلة
        return True
    
    def mark_as_read(self, notification_id):
        """تحديد الإشعار كمقروء"""
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['read'] = True
                return True
        return False
    
    def get_user_notifications(self, user_id, unread_only=False):
        """الحصول على إشعارات المستخدم"""
        user_notifications = [n for n in self.notifications if n['user_id'] == user_id]
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n['read']]
        
        return user_notifications


class EmailNotificationSystem:
    """نظام إخطارات البريد الإلكتروني"""
    
    def __init__(self):
        """تهيئة نظام البريد"""
        self.emails = []
    
    def send_email(self, user_email, subject, body, html_body=None):
        """إرسال بريد إلكتروني"""
        email = {
            'to': user_email,
            'subject': subject,
            'body': body,
            'html_body': html_body,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent'
        }
        
        self.emails.append(email)
        # في الإنتاج، استخدم SMTP أو خدمة مثل SendGrid
        return True
    
    def send_detailed_report(self, user_email, user_name, report_data):
        """إرسال تقرير مفصل بالبريد"""
        subject = "تقرير اللياقة والصحة الشهري"
        
        body = f"""
مرحباً {user_name}،

إليك تقريرك الصحي الشهري:

📊 الإحصائيات:
- عدد التمارين: {report_data.get('total_exercises', 0)}
- إجمالي الوقت: {report_data.get('total_duration', 0)} دقيقة
- السعرات المحروقة: {report_data.get('total_calories', 0)}
- متوسط الصحة: {report_data.get('avg_health_score', 0)} / 100

📈 التحسن:
{report_data.get('progress_summary', 'مستمر بالتحسن')}

💡 التوصيات:
{report_data.get('recommendations', 'استمر بالعمل الجيد')}

استمتع برحلتك نحو صحة أفضل!
        """
        
        return self.send_email(user_email, subject, body)
