"""
أمثلة على استخدام تطبيق متابعة التمارين الرياضية
Examples on how to use the Fitness Tracker Application
"""

from fitness_tracker import FitnessTracker, Exercise


def example_basic_usage():
    """مثال بسيط لاستخدام التطبيق"""
    print("\n" + "="*70)
    print("🔹 مثال 1: الاستخدام الأساسي")
    print("="*70)
    
    # إنشاء متتبع التمارين
    tracker = FitnessTracker('example_data.json')
    
    # إضافة عدة تمارين
    print("\n✓ إضافة التمارين...")
    tracker.add_exercise("الجري الصباحي", 30, 300, "جري")
    tracker.add_exercise("السباحة", 45, 400, "سباحة")
    tracker.add_exercise("رفع الأثقال", 60, 350, "رفع أثقال")
    
    # عرض التمارين
    print("\n✓ التمارين المسجلة:")
    tracker.view_all_exercises()


def example_statistics():
    """مثال على الحصول على الإحصائيات"""
    print("\n" + "="*70)
    print("🔹 مثال 2: عرض الإحصائيات")
    print("="*70)
    
    tracker = FitnessTracker('example_data.json')
    tracker.get_statistics()


def example_search():
    """مثال على البحث والتصفية"""
    print("\n" + "="*70)
    print("🔹 مثال 3: البحث والتصفية")
    print("="*70)
    
    tracker = FitnessTracker('example_data.json')
    
    # البحث حسب نوع التمرين
    print("\n🔍 البحث عن تمارين الجري:")
    tracker.search_by_type("جري")
    
    # البحث حسب التاريخ
    print("🔍 البحث عن التمارين في تاريخ محدد:")
    tracker.search_by_date("2024-03-12")


def example_daily_summary():
    """مثال على الملخص اليومي"""
    print("\n" + "="*70)
    print("🔹 مثال 4: الملخص اليومي")
    print("="*70)
    
    tracker = FitnessTracker('example_data.json')
    
    # عرض ملخص يومي
    print("\n📅 ملخص اليوم:")
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    tracker.get_daily_summary(today)


def example_advanced_operations():
    """مثال على العمليات المتقدمة"""
    print("\n" + "="*70)
    print("🔹 مثال 5: العمليات المتقدمة")
    print("="*70)
    
    tracker = FitnessTracker('example_data.json')
    
    # إضافة تمرين بتاريخ محدد
    print("\n✓ إضافة تمرين بتاريخ محدد...")
    from datetime import datetime, timedelta
    
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    exercise = Exercise("اليوجا", 20, 100, "اليوجا", past_date)
    tracker.exercises.append(exercise)
    tracker.save_data()
    print(f"✓ تم إضافة: {exercise}")
    
    # حساب إجمالي السعرات المحروقة
    print("\n✓ حساب الإحصائيات المخصصة...")
    total_calories = sum(e.calories for e in tracker.exercises)
    total_duration = sum(e.duration for e in tracker.exercises)
    print(f"إجمالي السعرات المحروقة: {total_calories} سعرة حرارية")
    print(f"إجمالي الوقت المستغرق: {total_duration} دقيقة")
    
    # تصفية التمارين حسب شروط معينة
    print("\n✓ تمارين تزيد مدتها عن 30 دقيقة:")
    long_exercises = [e for e in tracker.exercises if e.duration > 30]
    for exercise in long_exercises:
        print(f"  • {exercise}")
    
    # تمارين تحرق أكثر من 300 سعرة
    print("\n✓ تمارين تحرق أكثر من 300 سعرة حرارية:")
    high_calorie_exercises = [e for e in tracker.exercises if e.calories > 300]
    for exercise in high_calorie_exercises:
        print(f"  • {exercise}")


def example_file_operations():
    """مثال على عمليات الملفات"""
    print("\n" + "="*70)
    print("🔹 مثال 6: عمليات الملفات")
    print("="*70)
    
    import json
    import os
    
    # إنشاء متتبع وإضافة بيانات
    tracker = FitnessTracker('backup_data.json')
    tracker.add_exercise("تمرين اختبار", 25, 200, "تمارين منزلية")
    
    # قراءة الملف
    print("\n✓ محتوى ملف البيانات:")
    if os.path.exists('backup_data.json'):
        with open('backup_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(json.dumps(data, ensure_ascii=False, indent=2))
    
    # نسخ احتياطية
    print("\n✓ إنشاء نسخة احتياطية...")
    import shutil
    if os.path.exists('backup_data.json'):
        shutil.copy('backup_data.json', 'backup_data_backup.json')
        print("✓ تم إنشاء نسخة احتياطية: backup_data_backup.json")


def example_workout_plan():
    """مثال على خطة تدريب أسبوعية"""
    print("\n" + "="*70)
    print("🔹 مثال 7: خطة تدريب أسبوعية")
    print("="*70)
    
    tracker = FitnessTracker('weekly_plan.json')
    
    # خطة تدريب نموذجية
    workout_plan = {
        "الأحد": [("جري", 30, 300), ("تمارين منزلية", 20, 150)],
        "الاثنين": [("سباحة", 45, 400)],
        "الثلاثاء": [("رفع أثقال", 60, 350)],
        "الأربعاء": [("جري", 30, 300)],
        "الخميس": [("اليوجا", 30, 100), ("دراجة", 40, 300)],
        "الجمعة": [("تمارين منزلية", 45, 250)],
        "السبت": [("سباحة", 60, 450)],
    }
    
    print("\n✓ خطة التدريب الأسبوعية:")
    print("="*70)
    
    from datetime import datetime, timedelta
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    
    for day_offset, (day_name, exercises) in enumerate(workout_plan.items()):
        date = start_of_week + timedelta(days=day_offset)
        print(f"\n📅 {day_name} ({date.strftime('%Y-%m-%d')})")
        
        for exercise_name, duration, calories in exercises:
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
            exercise = Exercise(exercise_name, duration, calories, "مختلط", date_str)
            tracker.exercises.append(exercise)
            print(f"  ✓ {exercise_name} - {duration} دقيقة - {calories} سعرة")
    
    tracker.save_data()
    
    # الإحصائيات الأسبوعية
    print("\n" + "="*70)
    print("📊 الإحصائيات الأسبوعية:")
    print("="*70)
    total_duration = sum(e.duration for e in tracker.exercises)
    total_calories = sum(e.calories for e in tracker.exercises)
    print(f"إجمالي الوقت: {total_duration} دقيقة ({total_duration//60} ساعة و {total_duration%60} دقيقة)")
    print(f"إجمالي السعرات: {total_calories} سعرة حرارية")
    print(f"متوسط السعرات اليومي: {total_calories//7} سعرة حرارية")


def main():
    """تشغيل جميع الأمثلة"""
    print("\n" + "🏋️  أمثلة على استخدام تطبيق متابعة التمارين الرياضية".center(70))
    print("="*70)
    
    try:
        example_basic_usage()
        example_statistics()
        example_search()
        example_daily_summary()
        example_advanced_operations()
        example_file_operations()
        example_workout_plan()
        
        print("\n" + "="*70)
        print("✅ انتهت جميع الأمثلة بنجاح!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}\n")


if __name__ == "__main__":
    main()
