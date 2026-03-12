"""
نسخة متقدمة: واجهة رسومية لتطبيق متابعة التمارين الرياضية
Advanced Version: GUI for Fitness Tracking Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from fitness_tracker import FitnessTracker, Exercise


class FitnessTrackerGUI:
    """واجهة رسومية لتطبيق متابعة التمارين"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️  تطبيق متابعة التمارين الرياضية")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # تحديد الخط العربي
        self.root.tk.call('tk', 'scaling', 2.0)
        
        self.tracker = FitnessTracker()
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        
        # القائمة العلوية
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="استيراد بيانات", command=self.import_data)
        file_menu.add_command(label="تصدير بيانات", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.root.quit)
        
        # علامات التبويب
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # تبويب إضافة تمرين
        self.add_exercise_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_exercise_frame, text="إضافة تمرين")
        self.setup_add_exercise_tab()
        
        # تبويب عرض التمارين
        self.view_exercises_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_exercises_frame, text="التمارين")
        self.setup_view_exercises_tab()
        
        # تبويب الإحصائيات
        self.statistics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.statistics_frame, text="الإحصائيات")
        self.setup_statistics_tab()
        
        # تبويب البحث
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="بحث")
        self.setup_search_tab()
    
    def setup_add_exercise_tab(self):
        """تبويب إضافة تمرين جديد"""
        
        frame = ttk.LabelFrame(self.add_exercise_frame, text="إضافة تمرين جديد", padding=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # اسم التمرين
        ttk.Label(frame, text="اسم التمرين:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.exercise_name = ttk.Entry(frame, width=30)
        self.exercise_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # المدة
        ttk.Label(frame, text="المدة (دقيقة):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.exercise_duration = ttk.Spinbox(frame, from_=1, to=300, width=10)
        self.exercise_duration.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # السعرات
        ttk.Label(frame, text="السعرات المحروقة:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.exercise_calories = ttk.Spinbox(frame, from_=0, to=2000, width=10)
        self.exercise_calories.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # نوع التمرين
        ttk.Label(frame, text="نوع التمرين:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.exercise_type = ttk.Combobox(frame, width=27, values=[
            "مشي", "جري", "سباحة", "رفع أثقال", "اليوجا", "دراجة", "تمارين منزلية", "أخرى"
        ])
        self.exercise_type.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # زر الإضافة
        ttk.Button(frame, text="إضافة التمرين", command=self.add_exercise).grid(
            row=4, column=0, columnspan=2, pady=20
        )
        
        frame.columnconfigure(1, weight=1)
    
    def setup_view_exercises_tab(self):
        """تبويب عرض التمارين"""
        
        # شريط الأدوات
        toolbar = ttk.Frame(self.view_exercises_frame)
        toolbar.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(toolbar, text="تحديث", command=self.refresh_exercises_list).pack(side="left", padx=5)
        ttk.Button(toolbar, text="حذف المحدد", command=self.delete_selected_exercise).pack(side="left", padx=5)
        
        # جدول التمارين
        columns = ("التاريخ", "اسم التمرين", "النوع", "المدة", "السعرات")
        self.exercises_tree = ttk.Treeview(self.view_exercises_frame, columns=columns, height=15)
        self.exercises_tree.column("#0", width=0, stretch=tk.NO)
        self.exercises_tree.column("التاريخ", anchor="center", width=150)
        self.exercises_tree.column("اسم التمرين", anchor="center", width=120)
        self.exercises_tree.column("النوع", anchor="center", width=100)
        self.exercises_tree.column("المدة", anchor="center", width=80)
        self.exercises_tree.column("السعرات", anchor="center", width=80)
        
        self.exercises_tree.heading("#0", text="", anchor="w")
        self.exercises_tree.heading("التاريخ", text="التاريخ", anchor="center")
        self.exercises_tree.heading("اسم التمرين", text="اسم التمرين", anchor="center")
        self.exercises_tree.heading("النوع", text="النوع", anchor="center")
        self.exercises_tree.heading("المدة", text="المدة", anchor="center")
        self.exercises_tree.heading("السعرات", text="السعرات", anchor="center")
        
        self.exercises_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(self.view_exercises_frame, orient="vertical", command=self.exercises_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.exercises_tree.configure(yscroll=scrollbar.set)
        
        self.refresh_exercises_list()
    
    def setup_statistics_tab(self):
        """تبويب الإحصائيات"""
        
        self.stats_text = tk.Text(self.statistics_frame, height=30, width=80, bg="white", fg="black")
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(self.statistics_frame, text="تحديث الإحصائيات", command=self.update_statistics).pack(pady=10)
        
        self.update_statistics()
    
    def setup_search_tab(self):
        """تبويب البحث"""
        
        search_frame = ttk.LabelFrame(self.search_frame, text="خيارات البحث", padding=20)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        # البحث حسب النوع
        ttk.Label(search_frame, text="البحث حسب النوع:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.search_type_var = ttk.Entry(search_frame, width=30)
        self.search_type_var.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(search_frame, text="بحث", command=self.search_by_type).grid(row=0, column=2, padx=5)
        
        # البحث حسب التاريخ
        ttk.Label(search_frame, text="البحث حسب التاريخ:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.search_date_var = ttk.Entry(search_frame, width=30)
        self.search_date_var.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(search_frame, text="(YYYY-MM-DD)").grid(row=1, column=2, sticky="w", padx=5)
        ttk.Button(search_frame, text="بحث", command=self.search_by_date).grid(row=1, column=3, padx=5)
        
        search_frame.columnconfigure(1, weight=1)
        
        # نتائج البحث
        columns = ("التاريخ", "اسم التمرين", "النوع", "المدة", "السعرات")
        self.search_tree = ttk.Treeview(self.search_frame, columns=columns, height=15)
        self.search_tree.column("#0", width=0, stretch=tk.NO)
        self.search_tree.column("التاريخ", anchor="center", width=150)
        self.search_tree.column("اسم التمرين", anchor="center", width=120)
        self.search_tree.column("النوع", anchor="center", width=100)
        self.search_tree.column("المدة", anchor="center", width=80)
        self.search_tree.column("السعرات", anchor="center", width=80)
        
        for col_name in columns:
            self.search_tree.heading(col_name, text=col_name, anchor="center")
        
        self.search_tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def add_exercise(self):
        """إضافة تمرين جديد من الواجهة"""
        
        name = self.exercise_name.get().strip()
        if not name:
            messagebox.showerror("خطأ", "يجب إدخال اسم التمرين")
            return
        
        try:
            duration = int(self.exercise_duration.get())
            calories = int(self.exercise_calories.get())
        except ValueError:
            messagebox.showerror("خطأ", "يجب إدخال أرقام صحيحة للمدة والسعرات")
            return
        
        exercise_type = self.exercise_type.get().strip()
        if not exercise_type:
            messagebox.showerror("خطأ", "يجب اختيار نوع التمرين")
            return
        
        self.tracker.add_exercise(name, duration, calories, exercise_type)
        
        self.exercise_name.delete(0, tk.END)
        self.exercise_duration.delete(0, tk.END)
        self.exercise_calories.delete(0, tk.END)
        self.exercise_type.delete(0, tk.END)
        
        messagebox.showinfo("نجاح", f"تم إضافة التمرين: {name}")
        self.refresh_exercises_list()
    
    def refresh_exercises_list(self):
        """تحديث قائمة التمارين"""
        for item in self.exercises_tree.get_children():
            self.exercises_tree.delete(item)
        
        for i, exercise in enumerate(self.tracker.exercises):
            self.exercises_tree.insert("", "end", iid=i, values=(
                exercise.date,
                exercise.name,
                exercise.exercise_type,
                f"{exercise.duration} دقيقة",
                f"{exercise.calories} سعرة"
            ))
    
    def delete_selected_exercise(self):
        """حذف التمرين المحدد"""
        selected = self.exercises_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر تمرين لحذفه")
            return
        
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذا التمرين؟"):
            for item in selected:
                index = int(item)
                self.tracker.delete_exercise(index)
            self.refresh_exercises_list()
    
    def update_statistics(self):
        """تحديث الإحصائيات"""
        self.stats_text.delete(1.0, tk.END)
        
        if not self.tracker.exercises:
            self.stats_text.insert(tk.END, "❌ لا توجد بيانات للعرض\n")
            return
        
        total_duration = sum(e.duration for e in self.tracker.exercises)
        total_calories = sum(e.calories for e in self.tracker.exercises)
        avg_duration = total_duration / len(self.tracker.exercises)
        avg_calories = total_calories / len(self.tracker.exercises)
        
        stats_text = f"""
════════════════════════════════════════════════════════════════
📊 الإحصائيات العامة
════════════════════════════════════════════════════════════════
عدد التمارين الإجمالي: {len(self.tracker.exercises)}
إجمالي الوقت المستغرق: {total_duration} دقيقة ({total_duration//60} ساعة و {total_duration%60} دقيقة)
إجمالي السعرات المحروقة: {total_calories} سعرة حرارية
متوسط مدة التمرين: {avg_duration:.1f} دقيقة
متوسط السعرات المحروقة: {avg_calories:.1f} سعرة حرارية

────────────────────────────────────────────────────────────────
📈 الإحصائيات حسب نوع التمرين
────────────────────────────────────────────────────────────────
"""
        
        exercise_types = {}
        for exercise in self.tracker.exercises:
            if exercise.exercise_type not in exercise_types:
                exercise_types[exercise.exercise_type] = {'count': 0, 'duration': 0, 'calories': 0}
            exercise_types[exercise.exercise_type]['count'] += 1
            exercise_types[exercise.exercise_type]['duration'] += exercise.duration
            exercise_types[exercise.exercise_type]['calories'] += exercise.calories
        
        for exercise_type, stats in exercise_types.items():
            stats_text += f"""
{exercise_type}:
  • عدد التمارين: {stats['count']}
  • إجمالي الوقت: {stats['duration']} دقيقة
  • إجمالي السعرات: {stats['calories']} سعرة حرارية
"""
        
        self.stats_text.insert(tk.END, stats_text)
        self.stats_text.config(state="disabled")
    
    def search_by_type(self):
        """البحث حسب نوع التمرين"""
        search_text = self.search_type_var.get().strip()
        if not search_text:
            messagebox.showwarning("تحذير", "أدخل نوع التمرين للبحث عنه")
            return
        
        self._display_search_results(
            [e for e in self.tracker.exercises if e.exercise_type.lower() == search_text.lower()]
        )
    
    def search_by_date(self):
        """البحث حسب التاريخ"""
        search_date = self.search_date_var.get().strip()
        if not search_date:
            messagebox.showwarning("تحذير", "أدخل التاريخ للبحث")
            return
        
        self._display_search_results(
            [e for e in self.tracker.exercises if e.date.startswith(search_date)]
        )
    
    def _display_search_results(self, results):
        """عرض نتائج البحث"""
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        if not results:
            messagebox.showinfo("النتائج", "لم يتم العثور على نتائج")
            return
        
        for i, exercise in enumerate(results):
            self.search_tree.insert("", "end", iid=i, values=(
                exercise.date,
                exercise.name,
                exercise.exercise_type,
                f"{exercise.duration} دقيقة",
                f"{exercise.calories} سعرة"
            ))
    
    def export_data(self):
        """تصدير البيانات إلى ملف"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"fitness_data_{datetime.now().strftime('%Y%m%d')}.json"
        )
        if file_path:
            try:
                self.tracker.data_file = file_path
                self.tracker.save_data()
                messagebox.showinfo("نجاح", f"تم تصدير البيانات إلى:\n{file_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في التصدير:\n{e}")
    
    def import_data(self):
        """استيراد البيانات من ملف"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tracker.exercises = [Exercise.from_dict(e) for e in data]
                    self.tracker.save_data()
                messagebox.showinfo("نجاح", "تم استيراد البيانات بنجاح")
                self.refresh_exercises_list()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في الاستيراد:\n{e}")


def main():
    """تشغيل التطبيق"""
    root = tk.Tk()
    app = FitnessTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
