"""
نموذج الذكاء الاصطناعي للتوصيات والتحليلات
AI Model for Recommendations and Analysis
"""

import numpy as np
from datetime import datetime, timedelta
import json


class FitnessAIModel:
    """نموذج AI لتحليل اللياقة والصحة"""
    
    def __init__(self):
        """تهيئة النموذج"""
        self.min_max_stats = {
            'duration': (15, 120),
            'intensity': (1, 10),
            'calories': (50, 500)
        }
        
        # قاعدة المعرفة الطبية
        self.medical_database = self._load_medical_database()
    
    def _load_medical_database(self):
        """تحميل قاعدة البيانات الطبية المعتمدة"""
        return {
            'muscle_development': {
                'exercises': {
                    'بناء الذراعين': ['رفع الأثقال', 'تمارين الضغط'],
                    'بناء الصدر': ['تمارين الضغط', 'رفع الأثقال'],
                    'بناء الساقين': ['تمارين السكوات', 'المشي السريع'],
                    'بناء الظهر': ['رفع الأثقال', 'السباحة']
                },
                'parameters': {
                    'recommended_intensity': 7,
                    'min_duration': 30,
                    'frequency_per_week': 3
                }
            },
            'injury_treatment': {
                'lower_back_pain': {
                    'avoid': ['رفع أثقال ثقيلة', 'التواءات حادة'],
                    'recommended': ['السباحة', 'اليوجا', 'المشي برفق'],
                    'medical_reference': 'American Academy of Orthopaedic Surgeons',
                    'recovery_time': '4-8 weeks'
                },
                'knee_pain': {
                    'avoid': ['الجري على أسطح صلبة', 'تمارين الوثب'],
                    'recommended': ['السباحة', 'العلاج الطبيعي'],
                    'medical_reference': 'Mayo Clinic',
                    'recovery_time': '2-6 weeks'
                },
                'shoulder_pain': {
                    'avoid': ['تمارين الضغط الثقيلة', 'رفع الأثقال فوق الرأس'],
                    'recommended': ['تمارين التمدد', 'السباحة لينة'],
                    'medical_reference': 'Orthopaedic Research Society',
                    'recovery_time': '3-8 weeks'
                }
            },
            'health_conditions': {
                'hypertension': {
                    'recommended_intensity': 5,
                    'max_duration': 60,
                    'avoid': ['تمارين صعودية شديدة'],
                    'recommended': ['المشي السريع', 'السباحة', 'الدراجة'],
                    'medical_reference': 'American Heart Association'
                },
                'diabetes': {
                    'recommended_intensity': 6,
                    'min_frequency': 3,
                    'monitor': ['blood_sugar', 'heart_rate'],
                    'recommended': ['المشي، الجري المعتدل، السباحة'],
                    'medical_reference': 'American Diabetes Association'
                },
                'obesity': {
                    'focus': 'weight_loss',
                    'recommended_intensity': 6,
                    'min_frequency': 5,
                    'calorie_deficit': 500,
                    'medical_reference': 'WHO'
                }
            },
            'nerve_health': {
                'recommended_exercises': ['اليوجا', 'تمارين التوازن', 'تمارين المرونة'],
                'avoid': ['تمارين شديدة جداً'],
                'medical_reference': 'International Stroke Society',
                'key_metrics': ['balance', 'coordination', 'flexibility']
            }
        }
    
    def update_with_exercise(self, user_id, exercise):
        """تحديث البيانات عند إضافة تمرين جديد"""
        # سيتم حفظ البيانات في قاعدة البيانات
        pass
    
    def calculate_bmi_category(self, user):
        """تصنيف مؤشر كتلة الجسم"""
        bmi = user.get_bmi()
        if not bmi:
            return None
        
        if bmi < 18.5:
            return 'نقص الوزن'
        elif bmi < 25:
            return 'وزن طبيعي'
        elif bmi < 30:
            return 'زيادة الوزن'
        else:
            return 'السمنة'
    
    def detect_injury_patterns(self, health_records):
        """كشف أنماط الإصابات من السجلات الصحية"""
        injuries = []
        
        for record in health_records:
            if record.pain_points:
                pain_areas = json.loads(record.pain_points) if isinstance(record.pain_points, str) else record.pain_points
                for area, severity in pain_areas.items():
                    if severity > 5:  # ألم شديد
                        injuries.append({
                            'area': area,
                            'severity': severity,
                            'date': record.created_at,
                            'treatment': self._get_injury_treatment(area)
                        })
        
        return injuries
    
    def _get_injury_treatment(self, injury_type):
        """الحصول على علاج الإصابة من قاعدة البيانات الطبية"""
        injury_lower = injury_type.lower()
        
        if 'ظهر' in injury_lower or 'back' in injury_lower:
            return self.medical_database['injury_treatment'].get('lower_back_pain')
        elif 'ركبة' in injury_lower or 'knee' in injury_lower:
            return self.medical_database['injury_treatment'].get('knee_pain')
        elif 'كتف' in injury_lower or 'shoulder' in injury_lower:
            return self.medical_database['injury_treatment'].get('shoulder_pain')
        
        return None
    
    def analyze_health_metrics(self, user, health_record):
        """تحليل المقاييس الصحية"""
        recommendations = []
        
        # تحليل معدل ضربات القلب
        if health_record.heart_rate:
            if health_record.heart_rate > 100:
                recommendations.append({
                    'metric': 'heart_rate',
                    'status': 'تحذير',
                    'message': f'معدل ضربات القلب مرتفع: {health_record.heart_rate}',
                    'recommendation': 'قلل كثافة التمارين وراقب ضغط الدم'
                })
            elif health_record.heart_rate < 60:
                recommendations.append({
                    'metric': 'heart_rate',
                    'status': 'معلومة',
                    'message': f'معدل ضربات القلب منخفض: {health_record.heart_rate}',
                    'recommendation': 'حالة جيدة - تابع التمارين المنتظمة'
                })
        
        # تحليل نسبة الدهون
        if health_record.body_fat:
            if user.gender == 'male' and health_record.body_fat > 25:
                recommendations.append({
                    'metric': 'body_fat',
                    'status': 'تنبيه',
                    'message': f'نسبة الدهون مرتفعة: {health_record.body_fat}%',
                    'recommendation': 'زد من شدة التمارين وراقب التغذية'
                })
            elif user.gender == 'female' and health_record.body_fat > 32:
                recommendations.append({
                    'metric': 'body_fat',
                    'status': 'تنبيه',
                    'message': f'نسبة الدهون مرتفعة: {health_record.body_fat}%',
                    'recommendation': 'زد من شدة التمارين وراقب التغذية'
                })
        
        # تحليل النوم
        if health_record.sleep_hours:
            if health_record.sleep_hours < 7:
                recommendations.append({
                    'metric': 'sleep',
                    'status': 'تحذير',
                    'message': f'ساعات النوم قليلة: {health_record.sleep_hours} ساعات',
                    'recommendation': 'حاول الحصول على 7-9 ساعات نوم يومياً للتعافي'
                })
        
        # تحليل مستوى الإجهاد
        if health_record.stress_level and health_record.stress_level > 7:
            recommendations.append({
                'metric': 'stress',
                'status': 'تحذير',
                'message': f'مستوى الإجهاد مرتفع: {health_record.stress_level}/10',
                'recommendation': 'جرب اليوجا أو التأمل. قلل كثافة التمارين إذا لزم الأمر'
            })
        
        return recommendations
    
    def recommend_exercises_for_muscle_development(self, user, current_exercises):
        """التوصية بتمارين لتطوير العضلات"""
        recommendations = []
        
        # تحليل المناطق المستهدفة
        muscle_groups = {}
        for exercise in current_exercises:
            groups = json.loads(exercise.muscle_groups) if isinstance(exercise.muscle_groups, str) else exercise.muscle_groups or []
            for group in groups:
                muscle_groups[group] = muscle_groups.get(group, 0) + 1
        
        # التوصية بتمارين للمناطق الضعيفة
        all_groups = ['الصدر', 'الظهر', 'الذراعين', 'الساقين', 'الأساسيات']
        for group in all_groups:
            if group not in muscle_groups or muscle_groups[group] < 2:
                recommendations.append({
                    'category': 'muscle_development',
                    'title': f'تطوير مجموعة عضلات {group}',
                    'description': f'لاحظنا أنك لم تركز على {group} بشكل كافٍ',
                    'recommendation': self._get_muscle_group_exercises(group),
                    'confidence': 0.85,
                    'medical_reference': 'American College of Sports Medicine'
                })
        
        return recommendations
    
    def _get_muscle_group_exercises(self, muscle_group):
        """الحصول على تمارين لمجموعة عضلية معينة"""
        exercises_map = {
            'الصدر': [
                '• تمارين الضغط الكلاسيكية - 3 مجموعات × 10-15 تكرار',
                '• اضغط الدمبل - 3 مجموعات × 8-12 تكرار',
                '• انجراف الكابلات - 3 مجموعات × 10-12 تكرار'
            ],
            'الظهر': [
                '• سحب الذقن - 3 مجموعات × 8-12 تكرار',
                '• تمارين الجسر - 3 مجموعات × 10-15 تكرار',
                '• السباحة - 30-45 دقيقة',
                '• صفوف الدمبل - 3 مجموعات × 8-12 تكرار'
            ],
            'الذراعين': [
                '• تجعيد الدمبل - 3 مجموعات × 10-12 تكرار',
                '• ثني الذراع - 3 مجموعات × 8-12 تكرار',
                '• تمارين الضغط - 3 مجموعات × 10-15 تكرار'
            ],
            'الساقين': [
                '• السكوات - 3 مجموعات × 12-15 تكرار',
                '• الاندفاعات - 3 مجموعات × 10 لكل ساق',
                '• رفع الكعب - 3 مجموعات × 15-20 تكرار',
                '• الجري أو المشي السريع - 30-45 دقيقة'
            ],
            'الأساسيات': [
                '• تمارين البلانك - 3 مجموعات × 30-60 ثانية',
                '• تجعيد الانحناء - 3 مجموعات × 15-20 تكرار',
                '• دراجة البطن - 3 مجموعات × 20 تكرار',
                '• تطبيق جانبي - 3 مجموعات × 15-20 تكرار'
            ]
        }
        
        return '\n'.join(exercises_map.get(muscle_group, ['تمارين عامة متنوعة']))
    
    def detect_and_diagnose_injuries(self, user, health_records):
        """كشف وتشخيص الإصابات"""
        diagnoses = []
        
        injuries = self.detect_injury_patterns(health_records)
        
        for injury in injuries:
            if injury['treatment']:
                diagnoses.append({
                    'category': 'injury_diagnosis',
                    'title': f'تشخيص: {injury["area"]}',
                    'description': f'تم كشف ألم في منطقة {injury["area"]} بدرجة {injury["severity"]}/10',
                    'recommendation': self._format_injury_treatment(injury['treatment']),
                    'confidence': 0.8,
                    'medical_reference': injury['treatment'].get('medical_reference'),
                    'requires_doctor': True
                })
        
        return diagnoses
    
    def _format_injury_treatment(self, treatment):
        """تنسيق بيانات الإصابة"""
        if not treatment:
            return ''
        
        text = f"""
        🚫 تجنب:
        {', '.join(treatment.get('avoid', []))}
        
        ✅ موصى به:
        {', '.join(treatment.get('recommended', []))}
        
        ⏱️ وقت التعافي المتوقع: {treatment.get('recovery_time', 'استشر طبيباً')}
        
        📚 مرجع طبي معتمد: {treatment.get('medical_reference')}
        
        ⚠️ تنبيه: يرجى استشارة متخصص صحي قبل العودة للتمرين الكامل
        """
        return text
    
    def generate_comprehensive_analysis(self, user, exercises, health_records):
        """تحليل شامل للمستخدم"""
        analysis = {
            'user_id': user.id,
            'analysis_date': datetime.now().isoformat(),
            'health_status': {
                'bmi': user.get_bmi(),
                'bmi_category': self.calculate_bmi_category(user),
                'exercise_frequency': len(exercises),
                'last_health_check': health_records[-1].created_at.isoformat() if health_records else None
            },
            'recommendations': []
        }
        
        # تحليل المقاييس الصحية
        if health_records:
            latest_health = health_records[-1]
            metrics_recommendations = self.analyze_health_metrics(user, latest_health)
            analysis['recommendations'].extend(metrics_recommendations)
        
        # توصيات تطوير العضلات
        muscle_recommendations = self.recommend_exercises_for_muscle_development(user, exercises)
        analysis['recommendations'].extend(muscle_recommendations)
        
        # كشف الإصابات
        if health_records:
            injury_recommendations = self.detect_and_diagnose_injuries(user, health_records)
            analysis['recommendations'].extend(injury_recommendations)
        
        # نصائح عامة
        general_tips = self._generate_general_tips(user, exercises, health_records)
        analysis['recommendations'].extend(general_tips)
        
        return analysis
    
    def _generate_general_tips(self, user, exercises, health_records):
        """توليد نصائح عامة"""
        tips = []
        
        # التحقق من الانتظام
        if len(exercises) < 3:
            tips.append({
                'category': 'general_advice',
                'title': 'زد من تكرار التمرين',
                'description': 'لاحظنا أن عدد التمارين قليل',
                'recommendation': '''
                🎯 التوصيات:
                • مارس تمارين معتدلة 3-5 أيام في الأسبوع
                • ابدأ بـ 20-30 دقيقة يومياً
                • زد المدة والشدة تدريجياً
                • أعطِ عضلاتك يوماً للراحة بين التمارين الشديدة
                ''',
                'confidence': 0.9,
                'medical_reference': 'American Heart Association Guidelines'
            })
        
        # نصائح حول الماء والتغذية
        tips.append({
            'category': 'health_tips',
            'title': 'نصائح التغذية والترطيب',
            'description': 'نصائح مهمة للحفاظ على الصحة',
            'recommendation': '''
            💧 الترطيب:
            • اشرب 2-3 لترات من الماء يومياً
            • اشرب ماء إضافياً أثناء التمرين
            
            🥗 التغذية:
            • تناول بروتين الدجاج والسمك والبيض
            • أضف الخضروات والفواكه الطازجة
            • تجنب الأطعمة المصنعة والسكاكر البسيطة
            
            🍽️ عدد الوجبات:
            • تناول 3-4 وجبات متوازنة
            • لا تتخطى وجبة الإفطار
            ''',
            'confidence': 0.95,
            'medical_reference': 'WHO Nutrition Guidelines'
        })
        
        return tips


# إنشاء نموذج عام
fitness_ai = FitnessAIModel()
