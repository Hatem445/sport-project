"""
نظام مراقبة الصحة
Health Monitoring System
"""

from datetime import datetime, timedelta
import json


class HealthMonitor:
    """نظام لمراقبة الصحة واكتشاف التشوهات"""
    
    def __init__(self):
        """تهيئة نظام المراقبة"""
        self.alerts = []
        self.normal_ranges = {
            'heart_rate': {
                'min': 60,
                'max': 100,
                'alert_ranges': {
                    'low': (40, 60),
                    'high': (100, 140),
                    'critical_low': (0, 40),
                    'critical_high': (140, 200)
                }
            },
            'blood_pressure': {
                'systolic': {'normal': (90, 120), 'elevated': (120, 140), 'high': (140, 180)},
                'diastolic': {'normal': (60, 80), 'elevated': (80, 90), 'high': (90, 120)},
                'alert_systolic': 180,
                'alert_diastolic': 120
            },
            'body_fat_male': {
                'essential': (2, 5),
                'athletic': (6, 13),
                'fitness': (14, 17),
                'average': (18, 24),
                'obese': (25, 100)
            },
            'body_fat_female': {
                'essential': (10, 13),
                'athletic': (14, 20),
                'fitness': (21, 24),
                'average': (25, 31),
                'obese': (32, 100)
            },
            'sleep_hours': {
                'optimal': (7, 9),
                'warning_low': (5, 7),
                'warning_high': (9, 12),
                'critical': (0, 5)
            },
            'stress_level': {
                'low': (1, 3),
                'moderate': (4, 6),
                'high': (7, 10)
            }
        }
    
    def analyze(self, user_id, health_data):
        """تحليل بيانات صحية"""
        alerts = []
        warnings = []
        
        # فحص معدل ضربات القلب
        if health_data.heart_rate:
            heart_status = self._check_heart_rate(health_data.heart_rate)
            if heart_status['type'] == 'alert':
                alerts.append(heart_status)
            elif heart_status['type'] == 'warning':
                warnings.append(heart_status)
        
        # فحص ضغط الدم
        if health_data.blood_pressure:
            bp_status = self._check_blood_pressure(health_data.blood_pressure)
            if bp_status['type'] == 'alert':
                alerts.append(bp_status)
            elif bp_status['type'] == 'warning':
                warnings.append(bp_status)
        
        # فحص نسبة الدهون
        if health_data.body_fat:
            fat_status = self._check_body_fat(health_data.body_fat)
            if fat_status['type'] == 'alert':
                alerts.append(fat_status)
            elif fat_status['type'] == 'warning':
                warnings.append(fat_status)
        
        # فحص النوم
        if health_data.sleep_hours:
            sleep_status = self._check_sleep(health_data.sleep_hours)
            if sleep_status['type'] == 'alert':
                alerts.append(sleep_status)
            elif sleep_status['type'] == 'warning':
                warnings.append(sleep_status)
        
        # فحص الإجهاد
        if health_data.stress_level:
            stress_status = self._check_stress(health_data.stress_level)
            if stress_status['type'] == 'warning':
                warnings.append(stress_status)
        
        # فحص الإصابات
        if health_data.pain_points:
            injury_status = self._check_injuries(health_data.pain_points, health_data.injuries)
            if injury_status['type'] == 'alert':
                alerts.append(injury_status)
            elif injury_status['type'] == 'warning':
                warnings.append(injury_status)
        
        return {
            'user_id': user_id,
            'analysis_date': datetime.now().isoformat(),
            'alerts': alerts,
            'warnings': warnings,
            'overall_status': 'critical' if alerts else ('warning' if warnings else 'good')
        }
    
    def _check_heart_rate(self, heart_rate):
        """فحص معدل ضربات القلب"""
        ranges = self.normal_ranges['heart_rate']
        
        if ranges['alert_ranges']['critical_low'][0] <= heart_rate <= ranges['alert_ranges']['critical_low'][1]:
            return {
                'type': 'alert',
                'metric': 'heart_rate',
                'value': heart_rate,
                'severity': 'critical',
                'message': f'معدل ضربات القلب حرج جداً: {heart_rate} نبضة/دقيقة',
                'action': 'اطلب المساعدة الطبية فوراً'
            }
        
        if ranges['alert_ranges']['critical_high'][0] <= heart_rate <= ranges['alert_ranges']['critical_high'][1]:
            return {
                'type': 'alert',
                'metric': 'heart_rate',
                'value': heart_rate,
                'severity': 'critical',
                'message': f'معدل ضربات القلب مرتفع جداً: {heart_rate} نبضة/دقيقة',
                'action': 'توقف عن التمرين واستشر طبيباً فوراً'
            }
        
        if ranges['alert_ranges']['low'][0] <= heart_rate <= ranges['alert_ranges']['low'][1]:
            return {
                'type': 'warning',
                'metric': 'heart_rate',
                'value': heart_rate,
                'severity': 'mild',
                'message': f'معدل ضربات القلب منخفض: {heart_rate} نبضة/دقيقة',
                'action': 'راقب حالتك وزيادة النشاط تدريجياً'
            }
        
        if ranges['alert_ranges']['high'][0] <= heart_rate <= ranges['alert_ranges']['high'][1]:
            return {
                'type': 'warning',
                'metric': 'heart_rate',
                'value': heart_rate,
                'severity': 'mild',
                'message': f'معدل ضربات القلب مرتفع: {heart_rate} نبضة/دقيقة',
                'action': 'قلل من شدة التمرين واستريح'
            }
        
        return {
            'type': 'normal',
            'metric': 'heart_rate',
            'value': heart_rate,
            'message': f'معدل ضربات القلب طبيعي: {heart_rate} نبضة/دقيقة'
        }
    
    def _check_blood_pressure(self, blood_pressure_str):
        """فحص ضغط الدم"""
        try:
            sys, dias = map(int, blood_pressure_str.split('/'))
        except:
            return {'type': 'normal', 'message': 'لم يتم قراءة ضغط الدم بشكل صحيح'}
        
        # فحص الحالات الحرجة
        if sys >= self.normal_ranges['blood_pressure']['alert_systolic'] or \
           dias >= self.normal_ranges['blood_pressure']['alert_diastolic']:
            return {
                'type': 'alert',
                'metric': 'blood_pressure',
                'value': blood_pressure_str,
                'severity': 'critical',
                'message': f'ضغط الدم حرج: {blood_pressure_str}',
                'action': 'استشر طبيباً فوراً'
            }
        
        # فحص الارتفاع العالي
        if sys >= self.normal_ranges['blood_pressure']['systolic']['high'][0]:
            return {
                'type': 'warning',
                'metric': 'blood_pressure',
                'value': blood_pressure_str,
                'severity': 'moderate',
                'message': f'ضغط الدم مرتفع: {blood_pressure_str}',
                'action': 'قلل الملح والإجهاد، استشر طبيباً'
            }
        
        # فحص الارتفاع المعتدل
        if sys >= self.normal_ranges['blood_pressure']['systolic']['elevated'][0]:
            return {
                'type': 'warning',
                'metric': 'blood_pressure',
                'value': blood_pressure_str,
                'severity': 'mild',
                'message': f'ضغط الدم مرتفع قليلاً: {blood_pressure_str}',
                'action': 'راقب ضغطك بانتظام'
            }
        
        return {
            'type': 'normal',
            'metric': 'blood_pressure',
            'value': blood_pressure_str,
            'message': f'ضغط الدم طبيعي: {blood_pressure_str}'
        }
    
    def _check_body_fat(self, body_fat, gender='male'):
        """فحص نسبة الدهون"""
        ranges = self.normal_ranges['body_fat_male'] if gender == 'male' else self.normal_ranges['body_fat_female']
        
        for category, (min_val, max_val) in ranges.items():
            if min_val <= body_fat <= max_val:
                if category == 'obese':
                    return {
                        'type': 'alert',
                        'metric': 'body_fat',
                        'value': body_fat,
                        'severity': 'high',
                        'category': category,
                        'message': f'نسبة الدهون عالية جداً: {body_fat}%',
                        'action': 'استشر أخصائي تغذية وكثف التمارين'
                    }
                elif category == 'average':
                    return {
                        'type': 'warning',
                        'metric': 'body_fat',
                        'value': body_fat,
                        'category': category,
                        'message': f'نسبة الدهون متوسطة: {body_fat}%',
                        'action': 'يمكنك تحسينها بالتمارين المنتظمة'
                    }
                else:
                    return {
                        'type': 'normal',
                        'metric': 'body_fat',
                        'value': body_fat,
                        'category': category,
                        'message': f'نسبة الدهون ممتازة: {body_fat}% ({category})'
                    }
        
        return {
            'type': 'normal',
            'metric': 'body_fat',
            'value': body_fat
        }
    
    def _check_sleep(self, sleep_hours):
        """فحص ساعات النوم"""
        ranges = self.normal_ranges['sleep_hours']
        
        if sleep_hours >= ranges['optimal'][0] and sleep_hours <= ranges['optimal'][1]:
            return {
                'type': 'normal',
                'metric': 'sleep',
                'value': sleep_hours,
                'message': f'ساعات نومك ممتازة: {sleep_hours} ساعات'
            }
        
        if sleep_hours >= ranges['critical'][0] and sleep_hours <= ranges['critical'][1]:
            return {
                'type': 'alert',
                'metric': 'sleep',
                'value': sleep_hours,
                'severity': 'critical',
                'message': f'تنام أقل من 5 ساعات: {sleep_hours} ساعات',
                'action': 'زد ساعات نومك - هذا حرج للصحة'
            }
        
        if sleep_hours >= ranges['warning_low'][0] and sleep_hours < ranges['optimal'][0]:
            return {
                'type': 'warning',
                'metric': 'sleep',
                'value': sleep_hours,
                'message': f'ساعات النوم أقل من اللازم: {sleep_hours} ساعات',
                'action': 'حاول النوم 7-9 ساعات يومياً للتعافي الصحيح'
            }
        
        if sleep_hours > ranges['optimal'][1]:
            return {
                'type': 'warning',
                'metric': 'sleep',
                'value': sleep_hours,
                'message': f'ساعات النوم أكثر من اللازم: {sleep_hours} ساعات',
                'action': 'النوم الزائد قد يشير لتعب أو اكتئاب - استشر طبيباً'
            }
    
    def _check_stress(self, stress_level):
        """فحص مستوى الإجهاد"""
        if stress_level <= 3:
            return {
                'type': 'normal',
                'metric': 'stress',
                'value': stress_level,
                'message': 'مستوى الإجهاد منخفض - حالة جيدة'
            }
        elif stress_level <= 6:
            return {
                'type': 'warning',
                'metric': 'stress',
                'value': stress_level,
                'message': 'مستوى الإجهاد معتدل',
                'action': 'جرب تمارين الاسترخاء واليوجا'
            }
        else:
            return {
                'type': 'warning',
                'metric': 'stress',
                'value': stress_level,
                'message': 'مستوى الإجهاد مرتفع جداً',
                'action': 'خذ وقتاً للراحة وجرب تقنيات التأمل'
            }
    
    def _check_injuries(self, pain_points_str, injuries_str):
        """فحص الإصابات والألم"""
        try:
            pain_points = json.loads(pain_points_str) if isinstance(pain_points_str, str) else pain_points_str
            injuries = json.loads(injuries_str) if isinstance(injuries_str, str) else injuries_str
        except:
            return {'type': 'normal', 'message': 'لا توجد إصابات مسجلة'}
        
        # فحص نقاط الألم الشديدة
        severe_pain_areas = [area for area, severity in (pain_points or {}).items() if severity > 7]
        
        if severe_pain_areas:
            return {
                'type': 'alert',
                'metric': 'injury',
                'severity': 'high',
                'areas': severe_pain_areas,
                'message': f'ألم شديد في: {", ".join(severe_pain_areas)}',
                'action': 'توقف عن التمارين واستشر متخصصاً'
            }
        
        moderate_pain_areas = [area for area, severity in (pain_points or {}).items() if severity > 4]
        
        if moderate_pain_areas:
            return {
                'type': 'warning',
                'metric': 'injury',
                'severity': 'moderate',
                'areas': moderate_pain_areas,
                'message': f'ألم معتدل في: {", ".join(moderate_pain_areas)}',
                'action': 'قلل الشدة وراقب الحالة'
            }
        
        if injuries:
            return {
                'type': 'warning',
                'metric': 'injury',
                'injuries': injuries,
                'message': f'إصابات مسجلة: {injuries}',
                'action': 'اتبع نصائح إعادة التأهيل'
            }
        
        return {
            'type': 'normal',
            'metric': 'injury',
            'message': 'لا توجد إصابات أو آلام'
        }
    
    def get_health_score(self, health_data):
        """حساب درجة الصحة العامة من 0-100"""
        score = 100
        factors = {}
        
        # عوامل تأثر على الدرجة
        if health_data.heart_rate:
            if health_data.heart_rate > 120:
                score -= 15
                factors['heart_rate'] = -15
            elif health_data.heart_rate < 50:
                score -= 10
                factors['heart_rate'] = -10
        
        if health_data.sleep_hours:
            if health_data.sleep_hours < 5:
                score -= 20
                factors['sleep'] = -20
            elif health_data.sleep_hours < 7:
                score -= 10
                factors['sleep'] = -10
            elif health_data.sleep_hours > 10:
                score -= 5
                factors['sleep'] = -5
        
        if health_data.stress_level:
            score -= (health_data.stress_level * 2)
            factors['stress'] = -(health_data.stress_level * 2)
        
        if health_data.body_fat:
            if health_data.body_fat > 30:
                score -= 15
                factors['body_fat'] = -15
            elif health_data.body_fat > 25:
                score -= 8
                factors['body_fat'] = -8
        
        return max(0, min(100, score)), factors
