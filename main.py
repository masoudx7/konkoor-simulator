#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Konkoor Simulator Application
Main program with graphical user interface
"""

import tkinter as tk
from tkinter import messagebox, ttk
import time
from quiz_engine import QuizManager
from questions import get_subjects

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("شبیه‌ساز کنکور سراسری")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        # Set fonts
        self.font_title = ("Arial", 20, "bold")
        self.font_normal = ("Arial", 12)
        self.font_small = ("Arial", 10)
        
        self.quiz_manager = QuizManager()
        self.selected_subject = None
        
        self._create_main_page()
    
    def _create_main_page(self):
        """Create main page"""
        # Clear page
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top section - title
        top_frame = tk.Frame(self.root, bg="#1e3a8a", height=100)
        top_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            top_frame,
            text="🎓 شبیه‌ساز کنکور سراسری",
            font=self.font_title,
            bg="#1e3a8a",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content section
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome message
        message = tk.Label(
            main_frame,
            text="خوش‌آمدید به شبیه‌ساز کنکور سراسری!\nیک درس را انتخاب کنید:",
            font=self.font_normal,
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        message.pack(pady=20)
        
        # Subject list
        subjects = get_subjects()
        
        for subject in subjects:
            btn = tk.Button(
                main_frame,
                text=f"📚 {subject}",
                font=self.font_normal,
                bg="#3b82f6",
                fg="white",
                padx=20,
                pady=10,
                width=30,
                command=lambda s=subject: self._start_quiz(s)
            )
            btn.pack(pady=8)
        
        # Bottom section - history
        history_btn = tk.Button(
            main_frame,
            text="📊 مشاهده تاریخچه",
            font=self.font_small,
            bg="#10b981",
            fg="white",
            command=self._show_history
        )
        history_btn.pack(pady=10)
    
    def _start_quiz(self, subject):
        """Start quiz for selected subject"""
        self.selected_subject = subject
        
        # Settings window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("تنظیمات کوییز")
        settings_window.geometry("300x200")
        
        tk.Label(
            settings_window,
            text=f"درس: {subject}",
            font=self.font_normal
        ).pack(pady=10)
        
        tk.Label(
            settings_window,
            text="تعداد سوالات:",
            font=self.font_normal
        ).pack(pady=5)
        
        num_questions = ttk.Spinbox(
            settings_window,
            from_=1,
            to=10,
            width=10,
            font=self.font_normal
        )
        num_questions.set(5)
        num_questions.pack(pady=5)
        
        def start():
            try:
                num = int(num_questions.get())
                if self.quiz_manager.start_new_quiz(subject, num):
                    settings_window.destroy()
                    self._show_quiz_page()
                else:
                    messagebox.showerror("خطا", "خطای نامشخص!")
            except ValueError:
                messagebox.showerror("خطا", "لطفاً عدد صحیح وارد کنید!")
        
        start_btn = tk.Button(
            settings_window,
            text="شروع کوییز",
            font=self.font_normal,
            bg="#3b82f6",
            fg="white",
            command=start
        )
        start_btn.pack(pady=20)
    
    def _show_quiz_page(self):
        """Show quiz page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        current_quiz = self.quiz_manager.get_current_quiz()
        
        if not current_quiz:
            messagebox.showerror("خطا", "خطا در بارگذاری کوییز")
            return
        
        # Top section - information
        info_frame = tk.Frame(self.root, bg="#1e3a8a")
        info_frame.pack(fill=tk.X)
        
        info_text = f"درس: {current_quiz.subject} | سوال {current_quiz.current_question_index + 1} از {len(current_quiz.questions)}"
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=self.font_normal,
            bg="#1e3a8a",
            fg="white"
        )
        info_label.pack(pady=10)
        
        # Main section - question and options
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        current_question = current_quiz.get_current_question()
        
        if not current_question:
            self._show_results()
            return
        
        # Display question
        question_label = tk.Label(
            main_frame,
            text=current_question['question'],
            font=self.font_normal,
            bg="#f0f0f0",
            wraplength=600,
            justify=tk.CENTER
        )
        question_label.pack(pady=20)
        
        # Variable to store selection
        choice = tk.IntVar()
        
        # Display options
        for i, option in enumerate(current_question['options']):
            radio = tk.Radiobutton(
                main_frame,
                text=option,
                variable=choice,
                value=i,
                font=self.font_normal,
                bg="#f0f0f0"
            )
            radio.pack(pady=8, anchor=tk.E)
        
        # Next button
        def next_question():
            current_quiz.submit_answer(choice.get())
            
            if current_quiz.is_completed():
                self._show_results()
            else:
                self._show_quiz_page()
        
        next_btn = tk.Button(
            main_frame,
            text="→ بعدی",
            font=self.font_normal,
            bg="#10b981",
            fg="white",
            padx=20,
            pady=10,
            command=next_question
        )
        next_btn.pack(pady=20)
    
    def _show_results(self):
        """Show results page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        current_quiz = self.quiz_manager.get_current_quiz()
        report = current_quiz.get_report()
        
        # Top section
        top_frame = tk.Frame(self.root, bg="#1e3a8a")
        top_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            top_frame,
            text="🏆 نتایج کوییز",
            font=self.font_title,
            bg="#1e3a8a",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main section
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Results information
        results_text = f"""
درس: {report['subject']}
تعداد سوالات: {report['total_questions']}
امتیاز: {report['score']}/{report['total_questions']}
درصد: {report['percentage']:.1f}%
رتبه‌بندی: {current_quiz.get_grade()}
        """
        
        results_label = tk.Label(
            main_frame,
            text=results_text,
            font=self.font_normal,
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        results_label.pack(pady=20)
        
        # Details button
        details_btn = tk.Button(
            main_frame,
            text="📋 مشاهده تفاصیل",
            font=self.font_normal,
            bg="#3b82f6",
            fg="white",
            command=lambda: self._show_details(report)
        )
        details_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(
            main_frame,
            text="🏠 برگشت به صفحه اصلی",
            font=self.font_normal,
            bg="#10b981",
            fg="white",
            command=self._back_to_main
        )
        back_btn.pack(pady=10)
        
        # Save result to history
        self.quiz_manager.save_result()
    
    def _show_details(self, report):
        """Show answer details"""
        details_window = tk.Toplevel(self.root)
        details_window.title("تفاصیل نتایج")
        details_window.geometry("600x500")
        
        # Create Scrollbar
        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display each answer
        for answer in report['answers']:
            status = "✅ درست" if answer['is_correct'] else "❌ اشتباه"
            
            answer_text = f"""
سوال {answer['number']}: {status}
{answer['question']}

گزینه انتخاب شده: {answer['user_choice'] + 1}
پاسخ صحیح: {answer['correct_choice'] + 1}
            """
            
            label = tk.Label(
                scrollable_frame,
                text=answer_text,
                font=self.font_small,
                bg="#f0f0f0",
                justify=tk.RIGHT,
                padx=10,
                pady=10
            )
            label.pack(fill=tk.X, padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _show_history(self):
        """Show quiz history"""
        history = self.quiz_manager.get_history()
        
        if not history:
            messagebox.showinfo("تاریخچه", "تاریخچه خالی است!\nاول یک کوییز شروع کنید.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("تاریخچه کوییزها")
        history_window.geometry("500x400")
        
        # Create Scrollbar
        canvas = tk.Canvas(history_window)
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display each quiz
        for i, result in enumerate(history, 1):
            text = f"""
کوییز {i}:
درس: {result['subject']}
امتیاز: {result['score']}/{result['total_questions']}
درصد: {result['percentage']:.1f}%
            """
            
            label = tk.Label(
                scrollable_frame,
                text=text,
                font=self.font_small,
                bg="#f0f0f0",
                justify=tk.RIGHT
            )
            label.pack(fill=tk.X, padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _back_to_main(self):
        """Back to main page"""
        self._create_main_page()

def main():
    """Main function"""
    root = tk.Tk()
    
    # Set default colors
    root.configure(bg="#f0f0f0")
    
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
