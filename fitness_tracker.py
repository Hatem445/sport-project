"""
تطبيق متابعة التمارين الرياضية
Fitness Exercise Tracking Application
"""

import json
import os
from datetime import datetime
from pathlib import Path


class Exercise:
    """فئة تمثل تمرين رياضي واحد"""
    def __init__(self, name, duration, calories, exercise_type, date=None):
        self.name = name
        self.duration = duration  # بالدقائق
        self.calories = calories  # السعرات الحرارية المحروقة
        self.exercise_type = exercise_type  # نوع التمرين
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """تحويل التمرين إلى قاموس"""
        return {
            'name': self.name,
            'duration': self.duration,
            'calories': self.calories,
            'exercise_type': self.exercise_type,
            'date': self.date
        }
    
    @staticmethod
    def from_dict(data):
        """إنشء تمرين من قاموس"""
        return Exercise(
            data['name'],
            data['duration'],
            data['calories'],
            data['exercise_type'],
            data['date']
        )
    
    def __str__(self):
        return f"[{self.date}] {self.name} ({self.exercise_type}) - {self.duration} دقيقة - {self.calories} سعرة حرارية"


class FitnessTracker:
    """فئة رئيسية لإدارة متابعة التمارين الرياضية"""
    
    def __init__(self, data_file='fitness_data.json'):
        self.data_file = data_file
        self.exercises = []
        self.load_data()
    
    def load_data(self):
        """تحميل البيانات من الملف"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.exercises = [Exercise.from_dict(e) for e in data]
                print(f"✓ تم تحميل {len(self.exercises)} تمرين من الملف")
            except Exception as e:
                print(f"خطأ في تحميل البيانات: {e}")
    
    def save_data(self):
        """حفظ البيانات في الملف"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = [e.to_dict() for e in self.exercises]
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✓ تم حفظ البيانات بنجاح")
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")
    
    def add_exercise(self, name, duration, calories, exercise_type):
        """إضافة تمرين جديد"""
        exercise = Exercise(name, duration, calories, exercise_type)
        self.exercises.append(exercise)
        self.save_data()
        print(f"✓ تم إضافة التمرين: {name}")
        return exercise
    
    def view_all_exercises(self):
        """عرض جميع التمارين"""
        if not self.exercises:
            print("\n❌ لا توجد تمارين مسجلة حتى الآن\n")
            return
        
        print("\n" + "="*70)
        print("📋 قائمة جميع التمارين")
        print("="*70)
        for i, exercise in enumerate(self.exercises, 1):
            print(f"{i}. {exercise}")
        print("="*70 + "\n")
    
    def get_statistics(self):
        """حساب الإحصائيات"""
        if not self.exercises:
            print("\n❌ لا توجد بيانات للحساب\n")
            return
        
        total_duration = sum(e.duration for e in self.exercises)
        total_calories = sum(e.calories for e in self.exercises)
        avg_duration = total_duration / len(self.exercises)
        avg_calories = total_calories / len(self.exercises)
        
        # تجميع حسب نوع التمرين
        exercise_types = {}
        for exercise in self.exercises:
            if exercise.exercise_type not in exercise_types:
                exercise_types[exercise.exercise_type] = {'count': 0, 'duration': 0, 'calories': 0}
            exercise_types[exercise.exercise_type]['count'] += 1
            exercise_types[exercise.exercise_type]['duration'] += exercise.duration
            exercise_types[exercise.exercise_type]['calories'] += exercise.calories
        
        print("\n" + "="*70)
        print("📊 الإحصائيات العامة")
        print("="*70)
        print(f"عدد التمارين الإجمالي: {len(self.exercises)}")
        print(f"إجمالي الوقت المستغرق: {total_duration} دقيقة ({total_duration//60} ساعة و {total_duration%60} دقيقة)")
        print(f"إجمالي السعرات المحروقة: {total_calories} سعرة حرارية")
        print(f"متوسط مدة التمرين: {avg_duration:.1f} دقيقة")
        print(f"متوسط السعرات المحروقة: {avg_calories:.1f} سعرة حرارية")
        
        print("\n" + "-"*70)
        print("📈 الإحصائيات حسب نوع التمرين:")
        print("-"*70)
        for exercise_type, stats in exercise_types.items():
            print(f"\n{exercise_type}:")
            print(f"  • عدد التمارين: {stats['count']}")
            print(f"  • إجمالي الوقت: {stats['duration']} دقيقة")
            print(f"  • إجمالي السعرات: {stats['calories']} سعرة حرارية")
        print("="*70 + "\n")
    
    def search_by_type(self, exercise_type):
        """البحث عن تمارين حسب النوع"""
        results = [e for e in self.exercises if e.exercise_type.lower() == exercise_type.lower()]
        
        if not results:
            print(f"\n❌ لا توجد تمارين من نوع '{exercise_type}'\n")
            return
        
        print(f"\n📋 تمارين من نوع '{exercise_type}':")
        print("="*70)
        for i, exercise in enumerate(results, 1):
            print(f"{i}. {exercise}")
        print("="*70 + "\n")
    
    def search_by_date(self, date_str):
        """البحث عن تمارين حسب التاريخ"""
        results = [e for e in self.exercises if e.date.startswith(date_str)]
        
        if not results:
            print(f"\n❌ لا توجد تمارين في التاريخ '{date_str}'\n")
            return
        
        print(f"\n📋 تمارين في التاريخ '{date_str}':")
        print("="*70)
        for i, exercise in enumerate(results, 1):
            print(f"{i}. {exercise}")
        print("="*70 + "\n")
    
    def delete_exercise(self, index):
        """حذف تمرين"""
        if 0 <= index < len(self.exercises):
            deleted = self.exercises.pop(index)
            self.save_data()
            print(f"✓ تم حذف التمرين: {deleted.name}")
        else:
            print("❌ رقم التمرين غير صحيح")
    
    def get_daily_summary(self, date_str):
        """ملخص يومي"""
        exercises = [e for e in self.exercises if e.date.startswith(date_str)]
        
        if not exercises:
            print(f"\n❌ لا توجد تمارين في {date_str}\n")
            return
        
        total_duration = sum(e.duration for e in exercises)
        total_calories = sum(e.calories for e in exercises)
        
        print(f"\n📅 الملخص اليومي لتاريخ {date_str}")
        print("="*70)
        print(f"عدد التمارين: {len(exercises)}")
        print(f"إجمالي الوقت: {total_duration} دقيقة")
        print(f"السعرات المحروقة: {total_calories} سعرة حرارية")
        print("="*70 + "\n")


def main_menu():
    """القائمة الرئيسية"""
    tracker = FitnessTracker()
    
    while True:
        print("\n" + "="*70)
        print("🏋️  تطبيق متابعة التمارين الرياضية")
        print("="*70)
        print("1. ➕ إضافة تمرين جديد")
        print("2. 📋 عرض جميع التمارين")
        print("3. 📊 عرض الإحصائيات")
        print("4. 🔍 البحث حسب نوع التمرين")
        print("5. 📅 البحث حسب التاريخ")
        print("6. 🗑️  حذف تمرين")
        print("7. 📆 الملخص اليومي")
        print("8. ❌ خروج")
        print("="*70)
        
        choice = input("اختر من القائمة (1-8): ").strip()
        
        if choice == '1':
            print("\n" + "-"*70)
            print("أنواع التمارين: مشي - جري - سباحة - رفع أثقال - اليوجا - دراجة - تمارين منزلية - أخرى")
            print("-"*70)
            
            name = input("اسم التمرين: ").strip()
            if not name:
                print("❌ يجب إدخال اسم التمرين")
                continue
            
            try:
                duration = int(input("مدة التمرين بالدقائق: "))
                calories = int(input("السعرات المحروقة (تقريبي): "))
                exercise_type = input("نوع التمرين: ").strip()
                
                if duration <= 0 or calories < 0:
                    print("❌ يجب إدخال قيم صحيحة")
                    continue
                
                tracker.add_exercise(name, duration, calories, exercise_type)
            except ValueError:
                print("❌ يجب إدخال أرقام صحيحة")
        
        elif choice == '2':
            tracker.view_all_exercises()
        
        elif choice == '3':
            tracker.get_statistics()
        
        elif choice == '4':
            exercise_type = input("أدخل نوع التمرين للبحث عنه: ").strip()
            if exercise_type:
                tracker.search_by_type(exercise_type)
        
        elif choice == '5':
            date_str = input("أدخل التاريخ (YYYY-MM-DD): ").strip()
            if date_str:
                tracker.search_by_date(date_str)
        
        elif choice == '6':
            tracker.view_all_exercises()
            try:
                index = int(input("أدخل رقم التمرين المراد حذفه: ")) - 1
                tracker.delete_exercise(index)
            except ValueError:
                print("❌ يجب إدخال رقم صحيح")
        
        elif choice == '7':
            date_str = input("أدخل التاريخ (YYYY-MM-DD): ").strip()
            if date_str:
                tracker.get_daily_summary(date_str)
        
        elif choice == '8':
            print("\n👋 شكراً لاستخدام تطبيق متابعة التمارين الرياضية!")
            break
        
        else:
            print("❌ اختيار غير صحيح. حاول مرة أخرى")


if __name__ == "__main__":
    main_menu()
