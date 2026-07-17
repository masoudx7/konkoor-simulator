#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اپلیکیشن شبیه‌ساز کنکور سراسری
برنامه اصلی با رابط کاربری گرافیکی
"""

import tkinter as tk
from tkinter import messagebox, ttk
import time
from quiz_engine import مدیریت_کوییز
from questions import گرفتن_درس‌ها

class صفحه_اصلی:
    def __init__(self, root):
        self.root = root
        self.root.title("شبیه‌ساز کنکور سراسری")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        # تعیین فونت RTL
        self.فونت_عنوان = ("Arial", 20, "bold")
        self.فونت_عادی = ("Arial", 12)
        self.فونت_کوچک = ("Arial", 10)
        
        self.مدیریت_کوییز = مدیریت_کوییز()
        self.درس_انتخابی = None
        
        self._ایجاد_صفحه_اصلی()
    
    def _ایجاد_صفحه_اصلی(self):
        """ایجاد صفحه اصلی"""
        # پاک کردن صفحه
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # قسمت بالایی - عنوان
        فریم_عنوان = tk.Frame(self.root, bg="#1e3a8a", height=100)
        فریم_عنوان.pack(fill=tk.X)
        
        لیبل_عنوان = tk.Label(
            فریم_عنوان,
            text="🎓 شبیه‌ساز کنکور سراسری",
            font=self.فونت_عنوان,
            bg="#1e3a8a",
            fg="white"
        )
        لیبل_عنوان.pack(pady=20)
        
        # قسمت اصلی
        فریم_محتوا = tk.Frame(self.root, bg="#f0f0f0")
        فریم_محتوا.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # پیام خوش‌آمدگویی
        پیام = tk.Label(
            فریم_محتوا,
            text="خوش‌آمدید به شبیه‌ساز کنکور سراسری!\nیک درس را انتخاب کنید:",
            font=self.فونت_عادی,
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        پیام.pack(pady=20)
        
        # لیست درس‌ها
        درس‌ها = گرفتن_درس‌ها()
        
        for درس in درس‌ها:
            دکمه = tk.Button(
                فریم_محتوا,
                text=f"📚 {درس}",
                font=self.فونت_عادی,
                bg="#3b82f6",
                fg="white",
                padx=20,
                pady=10,
                width=30,
                command=lambda d=درس: self._شروع_کوییز(d)
            )
            دکمه.pack(pady=8)
        
        # قسمت پایین - تاریخچه
        دکمه_تاریخچه = tk.Button(
            فریم_محتوا,
            text="📊 مشاهده تاریخچه",
            font=self.فونت_کوچک,
            bg="#10b981",
            fg="white",
            command=self._نمایش_تاریخچه
        )
        دکمه_تاریخچه.pack(pady=10)
    
    def _شروع_کوییز(self, درس):
        """شروع کوییز برای درس انتخاب شده"""
        self.درس_انتخابی = درس
        
        # پنجره انتخاب تعداد سوالات
        پنجره_تنظیمات = tk.Toplevel(self.root)
        پنجره_تنظیمات.title("تنظیمات کوییز")
        پنجره_تنظیمات.geometry("300x200")
        
        tk.Label(
            پنجره_تنظیمات,
            text=f"درس: {درس}",
            font=self.فونت_عادی
        ).pack(pady=10)
        
        tk.Label(
            پنجره_تنظیمات,
            text="تعداد سوالات:",
            font=self.فونت_عادی
        ).pack(pady=5)
        
        تعداد = ttk.Spinbox(
            پنجره_تنظیمات,
            from_=1,
            to=10,
            width=10,
            font=self.فونت_عادی
        )
        تعداد.set(5)
        تعداد.pack(pady=5)
        
        def شروع():
            try:
                تعداد_سوال = int(تعداد.get())
                if self.مدیریت_کوییز.شروع_کوییز_جدید(درس, تعداد_سوال):
                    پنجره_تنظیمات.destroy()
                    self._نمایش_صفحه_کوییز()
                else:
                    messagebox.showerror("خطا", "خطای نامشخص!")
            except ValueError:
                messagebox.showerror("خطا", "لطفاً عدد صحیح وارد کنید!")
        
        دکمه_شروع = tk.Button(
            پنجره_تنظیمات,
            text="شروع کوییز",
            font=self.فونت_عادی,
            bg="#3b82f6",
            fg="white",
            command=شروع
        )
        دکمه_شروع.pack(pady=20)
    
    def _نمایش_صفحه_کوییز(self):
        """نمایش صفحه کوییز"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        کوییز_فعلی = self.مدیریت_کوییز.گرفتن_کوییز_فعلی()
        
        if not کوییز_فعلی:
            messagebox.showerror("خطا", "خطا در بارگذاری کوییز")
            return
        
        # قسمت بالایی - اطلاعات
        فریم_اطلاعات = tk.Frame(self.root, bg="#1e3a8a")
        فریم_اطلاعات.pack(fill=tk.X)
        
        اطلاعات_متن = f"درس: {کوییز_فعلی.درس} | سوال {کوییز_فعلی.شماره_سوال_فعلی + 1} از {len(کوییز_فعلی.سوالات)}"
        
        لیبل_اطلاعات = tk.Label(
            فریم_اطلاعات,
            text=اطلاعات_متن,
            font=self.فونت_عادی,
            bg="#1e3a8a",
            fg="white"
        )
        لیبل_اطلاعات.pack(pady=10)
        
        # قسمت اصلی - سوال و گزینه‌ها
        فریم_محتوا = tk.Frame(self.root, bg="#f0f0f0")
        فریم_محتوا.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        سوال_فعلی = کوییز_فعلی.گرفتن_سوال_فعلی()
        
        if not سوال_فعلی:
            self._نمایش_نتایج()
            return
        
        # نمایش سوال
        لیبل_سوال = tk.Label(
            فریم_محتوا,
            text=سوال_فعلی['سوال'],
            font=self.فونت_عادی,
            bg="#f0f0f0",
            wraplength=600,
            justify=tk.CENTER
        )
        لیبل_سوال.pack(pady=20)
        
        # متغیر برای ذخیره انتخاب
        انتخاب = tk.IntVar()
        
        # نمایش گزینه‌ها
        for i, گزینه in enumerate(سوال_فعلی['گزینه‌ها']):
            رادیو = tk.Radiobutton(
                فریم_محتوا,
                text=گزینه,
                variable=انتخاب,
                value=i,
                font=self.فونت_عادی,
                bg="#f0f0f0"
            )
            رادیو.pack(pady=8, anchor=tk.E)
        
        # دکمه بعدی
        def انتقال_به_بعدی():
            کوییز_فعلی.ثبت_پاسخ(انتخاب.get())
            
            if کوییز_فعلی.آیا_کوییز_تمام_شده():
                self._نمایش_نتایج()
            else:
                self._نمایش_صفحه_کوییز()
        
        دکمه_بعدی = tk.Button(
            فریم_محتوا,
            text="→ بعدی",
            font=self.فونت_عادی,
            bg="#10b981",
            fg="white",
            padx=20,
            pady=10,
            command=انتقال_به_بعدی
        )
        دکمه_بعدی.pack(pady=20)
    
    def _نمایش_نتایج(self):
        """نمایش صفحه نتایج"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        کوییز_فعلی = self.مدیریت_کوییز.گرفتن_کوییز_فعلی()
        گزارش = کوییز_فعلی.گرفتن_گزارش()
        
        # قسمت بالایی
        فریم_بالایی = tk.Frame(self.root, bg="#1e3a8a")
        فریم_بالایی.pack(fill=tk.X)
        
        لیبل_عنوان = tk.Label(
            فریم_بالایی,
            text="🏆 نتایج کوییز",
            font=self.فونت_عنوان,
            bg="#1e3a8a",
            fg="white"
        )
        لیبل_عنوان.pack(pady=20)
        
        # قسمت اصلی
        فریم_محتوا = tk.Frame(self.root, bg="#f0f0f0")
        فریم_محتوا.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # اطلاعات نتایج
        نتایج_متن = f"""
درس: {گزارش['درس']}
تعداد سوالات: {گزارش['تعداد_سوالات']}
امتیاز: {گزارش['امتیاز']}/{گزارش['تعداد_سوالات']}
درصد: {گزارش['درصد']:.1f}%
رتبه‌بندی: {کوییز_فعلی.تعیین_گریدز()}
        """
        
        لیبل_نتایج = tk.Label(
            فریم_محتوا,
            text=نتایج_متن,
            font=self.فونت_عادی,
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        لیبل_نتایج.pack(pady=20)
        
        # دکمه مشاهده تفاصیل
        دکمه_تفاصیل = tk.Button(
            فریم_محتوا,
            text="📋 مشاهده تفاصیل",
            font=self.فونت_عادی,
            bg="#3b82f6",
            fg="white",
            command=lambda: self._نمایش_تفاصیل_نتایج(گزارش)
        )
        دکمه_تفاصیل.pack(pady=10)
        
        # دکمه برگشت
        دکمه_برگشت = tk.Button(
            فریم_محتوا,
            text="🏠 برگشت به صفحه اصلی",
            font=self.فونت_عادی,
            bg="#10b981",
            fg="white",
            command=self._بازگشت_به_صفحه_اصلی
        )
        دکمه_برگشت.pack(pady=10)
        
        # ثبت نتیجه در تاریخچه
        self.مدیریت_کوییز.ثبت_نتیجه_نهایی()
    
    def _نمایش_تفاصیل_نتایج(self, گزارش):
        """نمایش تفاصیل پاسخ‌ها"""
        پنجره_تفاصیل = tk.Toplevel(self.root)
        پنجره_تفاصیل.title("تفاصیل نتایج")
        پنجره_تفاصیل.geometry("600x500")
        
        # ایجاد Scrollbar
        canvas = tk.Canvas(پنجره_تفاصیل)
        scrollbar = ttk.Scrollbar(پنجره_تفاصیل, orient="vertical", command=canvas.yview)
        فریم_قابل_اسکرول = tk.Frame(canvas)
        
        فریم_قابل_اسکرول.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=فریم_قابل_اسکرول, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # نمایش هر پاسخ
        for پاسخ in گزارش['پاسخ‌ها']:
            وضعیت = "✅ درست" if پاسخ['درست'] else "❌ اشتباه"
            
            متن_پاسخ = f"""
سوال {پاسخ['شماره']}: {وضعیت}
{پاسخ['سوال']}

گزینه انتخاب شده: {پاسخ['پاسخ_انتخاب_شده'] + 1}
پاسخ صحیح: {پاسخ['پاسخ_صحیح'] + 1}
            """
            
            لیبل = tk.Label(
                فریم_قابل_اسکرول,
                text=متن_پاسخ,
                font=self.فونت_کوچک,
                bg="#f0f0f0",
                justify=tk.RIGHT,
                padx=10,
                pady=10
            )
            لیبل.pack(fill=tk.X, padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _نمایش_تاریخچه(self):
        """نمایش تاریخچه کوییزها"""
        تاریخچه = self.مدیریت_کوییز.گرفتن_تاریخچه()
        
        if not تاریخچه:
            messagebox.showinfo("تاریخچه", "تاریخچه خالی است!\nاول یک کوییز شروع کنید.")
            return
        
        پنجره_تاریخچه = tk.Toplevel(self.root)
        پنجره_تاریخچه.title("تاریخچه کوییزها")
        پنجره_تاریخچه.geometry("500x400")
        
        # ایجاد Scrollbar
        canvas = tk.Canvas(پنجره_تاریخچه)
        scrollbar = ttk.Scrollbar(پنجره_تاریخچه, orient="vertical", command=canvas.yview)
        فریم_قابل_اسکرول = tk.Frame(canvas)
        
        فریم_قابل_اسکرول.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=فریم_قابل_اسکرول, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # نمایش هر کوییز
        for i, نتیجه in enumerate(تاریخچه, 1):
            متن = f"""
کوییز {i}:
درس: {نتیجه['درس']}
امتیاز: {نتیجه['امتیاز']}/{نتیجه['تعداد_سوالات']}
درصد: {نتیجه['درصد']:.1f}%
            """
            
            لیبل = tk.Label(
                فریم_قابل_اسکرول,
                text=متن,
                font=self.فونت_کوچک,
                bg="#f0f0f0",
                justify=tk.RIGHT
            )
            لیبل.pack(fill=tk.X, padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _بازگشت_به_صفحه_اصلی(self):
        """بازگشت به صفحه اصلی"""
        self._ایجاد_صفحه_اصلی()

def main():
    """تابع اصلی برنامه"""
    root = tk.Tk()
    
    # تنظیم RTL
    root.tk.call('tk', 'scaling', 2.0)
    
    # تنظیم رنگ‌های پیش‌فرض
    root.configure(bg="#f0f0f0")
    
    app = صفحه_اصلی(root)
    root.mainloop()

if __name__ == "__main__":
    main()
