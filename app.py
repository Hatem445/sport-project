"""
موقع متابعة التمارين الرياضية مع الذكاء الاصطناعي
Fitness Tracking Website with AI
"""

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from ai_recommendations import FitnessAIModel
from health_monitor import HealthMonitor
from notifications import NotificationSystem

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات
db = SQLAlchemy(app)

# تهيئة نماذج الذكاء الاصطناعي
ai_model = FitnessAIModel()
health_monitor = HealthMonitor()
notification_system = NotificationSystem()


# ==================== نماذج قاعدة البيانات ====================

class User(db.Model):
    """نموذج المستخدم"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # البيانات الصحية الشخصية
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)  # كغم
    height = db.Column(db.Float)  # سم
    gender = db.Column(db.String(10))
    medical_conditions = db.Column(db.Text)  # حالات طبية
    allergies = db.Column(db.Text)  # الحساسيات
    medications = db.Column(db.Text)  # الأدوية
    
    # تاريخ الحساب
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # notifications
    notifications_enabled = db.Column(db.Boolean, default=True)
    ai_enabled = db.Column(db.Boolean, default=True)
    
    exercises = db.relationship('Exercise', backref='user', lazy=True, cascade='all, delete-orphan')
    health_data = db.relationship('HealthData', backref='user', lazy=True, cascade='all, delete-orphan')
    ai_recommendations = db.relationship('AIRecommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """تعيين كلمة المرور المشفرة"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def get_bmi(self):
        """حساب مؤشر كتلة الجسم"""
        if self.weight and self.height:
            height_m = self.height / 100
            return self.weight / (height_m ** 2)
        return None


class Exercise(db.Model):
    """نموذج التمرين"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    name = db.Column(db.String(120), nullable=False)
    exercise_type = db.Column(db.String(50))  # جري، سباحة، إلخ
    duration = db.Column(db.Integer)  # بالدقائق
    intensity = db.Column(db.Integer)  # من 1-10
    calories = db.Column(db.Float)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    muscle_groups = db.Column(db.Text)  # مجموعات العضلات المستهدفة (JSON)


class HealthData(db.Model):
    """نموذج البيانات الصحية"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # القياسات الصحية
    weight = db.Column(db.Float)  # الوزن الحالي
    heart_rate = db.Column(db.Integer)  # نبضات القلب
    blood_pressure = db.Column(db.String(20))  # ضغط الدم
    body_fat = db.Column(db.Float)  # نسبة الدهون
    muscle_mass = db.Column(db.Float)  # كتلة العضل
    sleep_hours = db.Column(db.Float)  # ساعات النوم
    stress_level = db.Column(db.Integer)  # مستوى الإجهاد (1-10)
    energy_level = db.Column(db.Integer)  # مستوى الطاقة (1-10)
    
    # الملاحظات
    injuries = db.Column(db.Text)  # الإصابات
    pain_points = db.Column(db.Text)  # نقاط الألم
    general_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AIRecommendation(db.Model):
    """نموذج التوصيات من الذكاء الاصطناعي"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    category = db.Column(db.String(50))  # تطوير العضلات، الإصابات، النصائح، إلخ
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    confidence = db.Column(db.Float)  # درجة الثقة من 0-1
    
    # الاستشارات الطبية
    medical_reference = db.Column(db.Text)  # مراجع طبية معتمدة
    requires_doctor = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, archived


class ScheduledExercise(db.Model):
    """نموذج التمارين المجدولة"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    exercise_name = db.Column(db.String(120))
    scheduled_date = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)


# ==================== Routes - الصفحات الرئيسية ====================

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    if 'user_id' not in session:
        return render_template('landing.html')
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """تسجيل مستخدم جديد"""
    if request.method == 'POST':
        data = request.get_json()
        
        # التحقق من البيانات
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'البريد الإلكتروني موجود بالفعل'}), 400
        
        # إنشاء مستخدم جديد
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data.get('phone'),
            age=data.get('age'),
            weight=data.get('weight'),
            height=data.get('height'),
            gender=data.get('gender')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'تم التسجيل بنجاح'}), 201
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """دخول المستخدم"""
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            session['user_id'] = user.id
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True}), 200
        
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """تسجيل خروج المستخدم"""
    session.clear()
    return jsonify({'success': True})


# ==================== API Routes - الواجهات البرمجية ====================

@app.route('/api/user/profile')
def get_user_profile():
    """الحصول على ملف المستخدم"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'المستخدم غير موجود'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'age': user.age,
        'weight': user.weight,
        'height': user.height,
        'bmi': user.get_bmi(),
        'gender': user.gender,
        'phone': user.phone
    })


@app.route('/api/user/profile', methods=['PUT'])
def update_user_profile():
    """تحديث ملف المستخدم"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user = User.query.get(session['user_id'])
    data = request.get_json()
    
    user.age = data.get('age', user.age)
    user.weight = data.get('weight', user.weight)
    user.height = data.get('height', user.height)
    user.gender = data.get('gender', user.gender)
    user.medical_conditions = data.get('medical_conditions', user.medical_conditions)
    user.allergies = data.get('allergies', user.allergies)
    user.medications = data.get('medications', user.medications)
    user.phone = data.get('phone', user.phone)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'تم تحديث الملف بنجاح'})


@app.route('/api/exercises', methods=['GET', 'POST'])
def exercises():
    """إضافة وعرض التمارين"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.get_json()
        
        exercise = Exercise(
            user_id=user_id,
            name=data.get('name'),
            exercise_type=data.get('exercise_type'),
            duration=data.get('duration'),
            intensity=data.get('intensity'),
            calories=data.get('calories'),
            notes=data.get('notes'),
            muscle_groups=json.dumps(data.get('muscle_groups', []))
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        # تحديث نموذج AI
        ai_model.update_with_exercise(user_id, exercise)
        
        return jsonify({'success': True, 'message': 'تم إضافة التمرين بنجاح', 'exercise_id': exercise.id}), 201
    
    # GET - عرض التمارين
    exercises = Exercise.query.filter_by(user_id=user_id).all()
    return jsonify({
        'exercises': [{
            'id': e.id,
            'name': e.name,
            'type': e.exercise_type,
            'duration': e.duration,
            'intensity': e.intensity,
            'calories': e.calories,
            'date': e.created_at.isoformat(),
            'notes': e.notes
        } for e in exercises]
    })


@app.route('/api/health-data', methods=['GET', 'POST'])
def health_data():
    """إضافة وعرض البيانات الصحية"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.get_json()
        
        health = HealthData(
            user_id=user_id,
            weight=data.get('weight'),
            heart_rate=data.get('heart_rate'),
            blood_pressure=data.get('blood_pressure'),
            body_fat=data.get('body_fat'),
            muscle_mass=data.get('muscle_mass'),
            sleep_hours=data.get('sleep_hours'),
            stress_level=data.get('stress_level'),
            energy_level=data.get('energy_level'),
            injuries=data.get('injuries'),
            pain_points=data.get('pain_points'),
            general_notes=data.get('general_notes')
        )
        
        db.session.add(health)
        db.session.commit()
        
        # تحليل الحالة الصحية بـ AI
        health_monitor.analyze(user_id, health)
        
        return jsonify({'success': True, 'message': 'تم تسجيل البيانات الصحية'}), 201
    
    # GET - عرض البيانات
    health_records = HealthData.query.filter_by(user_id=user_id).order_by(HealthData.created_at.desc()).limit(30)
    
    return jsonify({
        'health_data': [{
            'id': h.id,
            'weight': h.weight,
            'heart_rate': h.heart_rate,
            'blood_pressure': h.blood_pressure,
            'body_fat': h.body_fat,
            'muscle_mass': h.muscle_mass,
            'sleep_hours': h.sleep_hours,
            'stress_level': h.stress_level,
            'energy_level': h.energy_level,
            'date': h.created_at.isoformat()
        } for h in health_records]
    })


@app.route('/api/ai/recommendations')
def get_recommendations():
    """الحصول على التوصيات من الذكاء الاصطناعي"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    
    # الحصول على التوصيات المحفوظة
    recommendations = AIRecommendation.query.filter_by(
        user_id=user_id,
        status='active'
    ).order_by(AIRecommendation.created_at.desc()).all()
    
    return jsonify({
        'recommendations': [{
            'id': r.id,
            'category': r.category,
            'title': r.title,
            'description': r.description,
            'recommendation': r.recommendation,
            'confidence': r.confidence,
            'medical_reference': r.medical_reference,
            'requires_doctor': r.requires_doctor,
            'date': r.created_at.isoformat()
        } for r in recommendations]
    })


@app.route('/api/ai/analyze', methods=['POST'])
def analyze_with_ai():
    """تحليل شامل باستخدام الذكاء الاصطناعي"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # جمع البيانات
    exercises = Exercise.query.filter_by(user_id=user_id).all()
    health_records = HealthData.query.filter_by(user_id=user_id).all()
    
    # تحليل AI
    analysis = ai_model.generate_comprehensive_analysis(
        user,
        exercises,
        health_records
    )
    
    # حفظ التوصيات
    for recommendation in analysis['recommendations']:
        rec = AIRecommendation(
            user_id=user_id,
            category=recommendation['category'],
            title=recommendation['title'],
            description=recommendation['description'],
            recommendation=recommendation['recommendation'],
            confidence=recommendation['confidence'],
            medical_reference=recommendation.get('medical_reference'),
            requires_doctor=recommendation.get('requires_doctor', False)
        )
        db.session.add(rec)
    
    db.session.commit()
    
    return jsonify(analysis)


@app.route('/api/schedule/exercise', methods=['POST'])
def schedule_exercise():
    """جدولة تمرين مع إرسال إشعار"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    data = request.get_json()
    
    scheduled_exercise = ScheduledExercise(
        user_id=user_id,
        exercise_name=data.get('exercise_name'),
        scheduled_date=datetime.fromisoformat(data.get('scheduled_date'))
    )
    
    db.session.add(scheduled_exercise)
    db.session.commit()
    
    # إرسال إشعار
    if user.phone and user.notifications_enabled:
        notification_system.send_sms(
            user.phone,
            f"تذكير: لديك تمرين '{data.get('exercise_name')}' في {data.get('scheduled_date')}"
        )
    
    return jsonify({'success': True, 'message': 'تم جدولة التمرين'})


@app.route('/api/stats/summary')
def get_stats_summary():
    """ملخص الإحصائيات"""
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول'}), 401
    
    user_id = session['user_id']
    
    # إحصائيات التمارين
    exercises = Exercise.query.filter_by(user_id=user_id).all()
    total_exercises = len(exercises)
    total_calories = sum(e.calories or 0 for e in exercises)
    total_duration = sum(e.duration or 0 for e in exercises)
    
    # آخر البيانات الصحية
    latest_health = HealthData.query.filter_by(user_id=user_id).order_by(
        HealthData.created_at.desc()
    ).first()
    
    return jsonify({
        'total_exercises': total_exercises,
        'total_calories': total_calories,
        'total_duration': total_duration,
        'latest_health': {
            'weight': latest_health.weight if latest_health else None,
            'heart_rate': latest_health.heart_rate if latest_health else None,
            'body_fat': latest_health.body_fat if latest_health else None
        } if latest_health else {}
    })


# ==================== معالجة الأخطاء ====================

@app.errorhandler(404)
def not_found(error):
    """صفحة غير موجودة"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """خطأ في الخادم"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
