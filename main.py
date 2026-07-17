#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Konkoor Simulator Application
Modern GUI with RTL support
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from quiz_engine import QuizManager
from questions import get_subjects

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("شبیه‌ساز کنکور سراسری")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f172a")
        
        # Modern fonts
        self.font_title = ("Segoe UI", 28, "bold")
        self.font_subtitle = ("Segoe UI", 14)
        self.font_normal = ("Segoe UI", 11)
        self.font_small = ("Segoe UI", 9)
        
        # Color scheme
        self.colors = {
            "bg_dark": "#0f172a",
            "bg_light": "#1e293b",
            "bg_card": "#1a2332",
            "primary": "#3b82f6",
            "primary_hover": "#2563eb",
            "success": "#10b981",
            "success_hover": "#059669",
            "danger": "#ef4444",
            "text_primary": "#f1f5f9",
            "text_secondary": "#cbd5e1",
            "accent": "#06b6d4"
        }
        
        # Configure style
        self._configure_style()
        
        self.quiz_manager = QuizManager()
        self.selected_subject = None
        
        self._create_main_page()
    
    def _configure_style(self):
        """Configure modern style"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            'TButton',
            font=self.font_normal,
            padding=10,
            background=self.colors["primary"],
            foreground=self.colors["text_primary"],
            borderwidth=0,
            focuscolor='none'
        )
        
        style.map(
            'TButton',
            background=[('active', self.colors["primary_hover"])],
            foreground=[('active', self.colors["text_primary"])]
        )
    
    def _create_main_page(self):
        """Create modern main page"""
        # Clear page
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with gradient-like background
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=self.colors["bg_light"], height=120)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with emoji
        title_label = tk.Label(
            header_frame,
            text="🎓 شبیه‌ساز کنکور سراسری",
            font=self.font_title,
            bg=self.colors["bg_light"],
            fg=self.colors["text_primary"],
            justify=tk.CENTER
        )
        title_label.pack(pady=20, expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="آماده‌سازی برای کنکور سراسری",
            font=self.font_subtitle,
            bg=self.colors["bg_light"],
            fg=self.colors["accent"],
            justify=tk.CENTER
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors["bg_dark"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Subjects title
        subjects_title = tk.Label(
            content_frame,
            text="درس‌های موجود:",
            font=self.font_subtitle,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_primary"],
            justify=tk.RIGHT
        )
        subjects_title.pack(anchor=tk.E, pady=(0, 20))
        
        # Subjects container
        subjects_container = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        subjects_container.pack(fill=tk.BOTH, expand=True)
        
        subjects = get_subjects()
        
        # Create subject buttons in grid
        for i, subject in enumerate(subjects):
            btn_frame = tk.Frame(subjects_container, bg=self.colors["bg_dark"])
            btn_frame.pack(fill=tk.X, pady=8)
            
            btn = tk.Button(
                btn_frame,
                text=f"📚 {subject}",
                font=self.font_normal,
                bg=self.colors["primary"],
                fg=self.colors["text_primary"],
                activebackground=self.colors["primary_hover"],
                activeforeground=self.colors["text_primary"],
                padx=20,
                pady=12,
                width=50,
                border=0,
                cursor="hand2",
                command=lambda s=subject: self._start_quiz(s)
            )
            btn.pack(fill=tk.X)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["primary_hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["primary"]))
        
        # Bottom section
        bottom_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        bottom_frame.pack(fill=tk.X, pady=(30, 0))
        
        history_btn = tk.Button(
            bottom_frame,
            text="📊 مشاهده تاریخچه",
            font=self.font_normal,
            bg=self.colors["success"],
            fg=self.colors["text_primary"],
            activebackground=self.colors["success_hover"],
            activeforeground=self.colors["text_primary"],
            padx=20,
            pady=10,
            border=0,
            cursor="hand2",
            command=self._show_history
        )
        history_btn.pack(side=tk.LEFT)
        
        history_btn.bind("<Enter>", lambda e, b=history_btn: b.config(bg=self.colors["success_hover"]))
        history_btn.bind("<Leave>", lambda e, b=history_btn: b.config(bg=self.colors["success"]))
    
    def _start_quiz(self, subject):
        """Start quiz for selected subject"""
        self.selected_subject = subject
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("تنظیمات کوییز")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.colors["bg_dark"])
        settings_window.resizable(False, False)
        
        # Center window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Container
        container = tk.Frame(settings_window, bg=self.colors["bg_light"])
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Title
        title = tk.Label(
            container,
            text="تنظیمات کوییز",
            font=self.font_subtitle,
            bg=self.colors["bg_light"],
            fg=self.colors["text_primary"]
        )
        title.pack(pady=20)
        
        # Subject display
        subject_label = tk.Label(
            container,
            text=f"درس: {subject}",
            font=self.font_normal,
            bg=self.colors["bg_light"],
            fg=self.colors["accent"]
        )
        subject_label.pack(pady=10)
        
        # Number of questions
        num_label = tk.Label(
            container,
            text="تعداد سوالات (۱-۱۰):",
            font=self.font_normal,
            bg=self.colors["bg_light"],
            fg=self.colors["text_primary"]
        )
        num_label.pack(pady=(20, 10))
        
        num_frame = tk.Frame(container, bg=self.colors["bg_light"])
        num_frame.pack(pady=10)
        
        num_questions = ttk.Spinbox(
            num_frame,
            from_=1,
            to=10,
            width=10,
            font=self.font_normal
        )
        num_questions.set(5)
        num_questions.pack()
        
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
        
        # Start button
        start_btn = tk.Button(
            container,
            text="شروع کوییز",
            font=self.font_normal,
            bg=self.colors["primary"],
            fg=self.colors["text_primary"],
            activebackground=self.colors["primary_hover"],
            activeforeground=self.colors["text_primary"],
            padx=30,
            pady=10,
            border=0,
            cursor="hand2",
            command=start
        )
        start_btn.pack(pady=30)
        
        start_btn.bind("<Enter>", lambda e, b=start_btn: b.config(bg=self.colors["primary_hover"]))
        start_btn.bind("<Leave>", lambda e, b=start_btn: b.config(bg=self.colors["primary"]))
    
    def _show_quiz_page(self):
        """Show modern quiz page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        current_quiz = self.quiz_manager.get_current_quiz()
        
        if not current_quiz:
            messagebox.showerror("خطا", "خطا در بارگذاری کوییز")
            return
        
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        progress_frame = tk.Frame(main_container, bg=self.colors["bg_light"], height=70)
        progress_frame.pack(fill=tk.X)
        progress_frame.pack_propagate(False)
        
        progress_percent = ((current_quiz.current_question_index) / len(current_quiz.questions)) * 100
        
        progress_text = f"سوال {current_quiz.current_question_index + 1} از {len(current_quiz.questions)} | {progress_percent:.0f}%"
        progress_label = tk.Label(
            progress_frame,
            text=progress_text,
            font=self.font_subtitle,
            bg=self.colors["bg_light"],
            fg=self.colors["accent"]
        )
        progress_label.pack(pady=10)
        
        # Progress bar visual
        progress_canvas = tk.Canvas(
            progress_frame,
            bg=self.colors["bg_light"],
            highlightthickness=0,
            height=6
        )
        progress_canvas.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        bar_width = (progress_percent / 100) * 860
        progress_canvas.create_rectangle(0, 0, bar_width, 6, fill=self.colors["accent"], outline="")
        progress_canvas.create_rectangle(bar_width, 0, 860, 6, fill=self.colors["bg_dark"], outline="")
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors["bg_dark"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        current_question = current_quiz.get_current_question()
        
        if not current_question:
            self._show_results()
            return
        
        # Question
        question_label = tk.Label(
            content_frame,
            text=current_question['question'],
            font=self.font_normal,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_primary"],
            wraplength=700,
            justify=tk.RIGHT
        )
        question_label.pack(pady=(0, 40), anchor=tk.NE)
        
        # Options frame
        options_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        choice = tk.IntVar()
        
        for i, option in enumerate(current_question['options']):
            option_frame = tk.Frame(
                options_frame,
                bg=self.colors["bg_card"],
                highlightbackground=self.colors["primary"],
                highlightthickness=2
            )
            option_frame.pack(fill=tk.X, pady=12)
            
            radio = tk.Radiobutton(
                option_frame,
                text=option,
                variable=choice,
                value=i,
                font=self.font_normal,
                bg=self.colors["bg_card"],
                fg=self.colors["text_primary"],
                activebackground=self.colors["primary"],
                activeforeground=self.colors["text_primary"],
                selectcolor=self.colors["primary"],
                highlightthickness=0,
                justify=tk.RIGHT,
                anchor=tk.E
            )
            radio.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Bottom buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        button_frame.pack(fill=tk.X, pady=(40, 0))
        
        def next_question():
            current_quiz.submit_answer(choice.get())
            
            if current_quiz.is_completed():
                self._show_results()
            else:
                self._show_quiz_page()
        
        next_btn = tk.Button(
            button_frame,
            text="بعدی ←",
            font=self.font_normal,
            bg=self.colors["success"],
            fg=self.colors["text_primary"],
            activebackground=self.colors["success_hover"],
            activeforeground=self.colors["text_primary"],
            padx=30,
            pady=12,
            border=0,
            cursor="hand2",
            command=next_question
        )
        next_btn.pack(side=tk.LEFT)
        
        next_btn.bind("<Enter>", lambda e, b=next_btn: b.config(bg=self.colors["success_hover"]))
        next_btn.bind("<Leave>", lambda e, b=next_btn: b.config(bg=self.colors["success"]))
    
    def _show_results(self):
        """Show modern results page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        current_quiz = self.quiz_manager.get_current_quiz()
        report = current_quiz.get_report()
        
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.colors["bg_light"], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🏆 نتایج کوییز",
            font=self.font_title,
            bg=self.colors["bg_light"],
            fg=self.colors["accent"]
        )
        title_label.pack(pady=20, expand=True)
        
        # Content
        content_frame = tk.Frame(main_container, bg=self.colors["bg_dark"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Results card
        results_card = tk.Frame(
            content_frame,
            bg=self.colors["bg_card"],
            relief=tk.FLAT,
            bd=0
        )
        results_card.pack(fill=tk.X, pady=20)
        
        # Score display
        score_text = f"امتیاز: {report['score']}/{report['total_questions']}"
        score_label = tk.Label(
            results_card,
            text=score_text,
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["accent"]
        )
        score_label.pack(pady=20)
        
        # Percentage display
        percentage_text = f"درصد: {report['percentage']:.1f}%"
        percentage_label = tk.Label(
            results_card,
            text=percentage_text,
            font=self.font_subtitle,
            bg=self.colors["bg_card"],
            fg=self.colors["text_primary"]
        )
        percentage_label.pack(pady=10)
        
        # Grade display
        grade_label = tk.Label(
            results_card,
            text=f"رتبه‌بندی: {current_quiz.get_grade()}",
            font=self.font_subtitle,
            bg=self.colors["bg_card"],
            fg=self.colors["success"]
        )
        grade_label.pack(pady=(10, 20))
        
        # Subject info
        subject_label = tk.Label(
            results_card,
            text=f"درس: {report['subject']}",
            font=self.font_normal,
            bg=self.colors["bg_card"],
            fg=self.colors["text_secondary"]
        )
        subject_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        buttons_frame.pack(fill=tk.X, pady=(40, 0))
        
        # Details button
        details_btn = tk.Button(
            buttons_frame,
            text="📋 مشاهده تفاصیل",
            font=self.font_normal,
            bg=self.colors["primary"],
            fg=self.colors["text_primary"],
            activebackground=self.colors["primary_hover"],
            activeforeground=self.colors["text_primary"],
            padx=20,
            pady=10,
            border=0,
            cursor="hand2",
            command=lambda: self._show_details(report)
        )
        details_btn.pack(side=tk.LEFT, padx=5)
        
        details_btn.bind("<Enter>", lambda e, b=details_btn: b.config(bg=self.colors["primary_hover"]))
        details_btn.bind("<Leave>", lambda e, b=details_btn: b.config(bg=self.colors["primary"]))
        
        # Back button
        back_btn = tk.Button(
            buttons_frame,
            text="🏠 برگشت به صفحه اصلی",
            font=self.font_normal,
            bg=self.colors["success"],
            fg=self.colors["text_primary"],
            activebackground=self.colors["success_hover"],
            activeforeground=self.colors["text_primary"],
            padx=20,
            pady=10,
            border=0,
            cursor="hand2",
            command=self._back_to_main
        )
        back_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn.bind("<Enter>", lambda e, b=back_btn: b.config(bg=self.colors["success_hover"]))
        back_btn.bind("<Leave>", lambda e, b=back_btn: b.config(bg=self.colors["success"]))
        
        self.quiz_manager.save_result()
    
    def _show_details(self, report):
        """Show answer details in modern style"""
        details_window = tk.Toplevel(self.root)
        details_window.title("تفاصیل نتایج")
        details_window.geometry("700x600")
        details_window.configure(bg=self.colors["bg_dark"])
        
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Header
        header = tk.Frame(details_window, bg=self.colors["bg_light"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="تفاصیل پاسخ‌ها",
            font=self.font_subtitle,
            bg=self.colors["bg_light"],
            fg=self.colors["text_primary"]
        )
        header_label.pack(pady=15)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(
            details_window,
            bg=self.colors["bg_dark"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Answers
        for answer in report['answers']:
            answer_frame = tk.Frame(
                scrollable_frame,
                bg=self.colors["bg_card"],
                relief=tk.FLAT,
                bd=0
            )
            answer_frame.pack(fill=tk.X, padx=15, pady=10)
            
            status = "✅ درست" if answer['is_correct'] else "❌ اشتباه"
            status_color = self.colors["success"] if answer['is_correct'] else self.colors["danger"]
            
            # Question number and status
            header_line = tk.Label(
                answer_frame,
                text=f"سوال {answer['number']}: {status}",
                font=self.font_normal,
                bg=self.colors["bg_card"],
                fg=status_color,
                justify=tk.RIGHT
            )
            header_line.pack(anchor=tk.E, padx=15, pady=(15, 10))
            
            # Question text
            question_line = tk.Label(
                answer_frame,
                text=answer['question'],
                font=self.font_small,
                bg=self.colors["bg_card"],
                fg=self.colors["text_secondary"],
                wraplength=600,
                justify=tk.RIGHT
            )
            question_line.pack(anchor=tk.E, padx=15, pady=5)
            
            # User answer
            user_answer_line = tk.Label(
                answer_frame,
                text=f"پاسخ شما: گزینه {answer['user_choice'] + 1}",
                font=self.font_small,
                bg=self.colors["bg_card"],
                fg=self.colors["text_primary"],
                justify=tk.RIGHT
            )
            user_answer_line.pack(anchor=tk.E, padx=15, pady=3)
            
            # Correct answer
            correct_answer_line = tk.Label(
                answer_frame,
                text=f"پاسخ صحیح: گزینه {answer['correct_choice'] + 1}",
                font=self.font_small,
                bg=self.colors["bg_card"],
                fg=self.colors["success"],
                justify=tk.RIGHT
            )
            correct_answer_line.pack(anchor=tk.E, padx=15, pady=(3, 15))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _show_history(self):
        """Show quiz history in modern style"""
        history = self.quiz_manager.get_history()
        
        if not history:
            messagebox.showinfo("تاریخچه", "تاریخچه خالی است!\nاول یک کوییز شروع کنید.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("تاریخچه کوییزها")
        history_window.geometry("600x500")
        history_window.configure(bg=self.colors["bg_dark"])
        
        history_window.transient(self.root)
        history_window.grab_set()
        
        # Header
        header = tk.Frame(history_window, bg=self.colors["bg_light"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="تاریخچه کوییزها",
            font=self.font_subtitle,
            bg=self.colors["bg_light"],
            fg=self.colors["text_primary"]
        )
        header_label.pack(pady=15)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(
            history_window,
            bg=self.colors["bg_dark"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # History items
        for i, result in enumerate(history, 1):
            item_frame = tk.Frame(
                scrollable_frame,
                bg=self.colors["bg_card"],
                relief=tk.FLAT,
                bd=0
            )
            item_frame.pack(fill=tk.X, padx=15, pady=10)
            
            # Quiz number and subject
            header_line = tk.Label(
                item_frame,
                text=f"کوییز {i}: {result['subject']}",
                font=self.font_normal,
                bg=self.colors["bg_card"],
                fg=self.colors["accent"],
                justify=tk.RIGHT
            )
            header_line.pack(anchor=tk.E, padx=15, pady=(15, 10))
            
            # Score
            score_line = tk.Label(
                item_frame,
                text=f"امتیاز: {result['score']}/{result['total_questions']}",
                font=self.font_small,
                bg=self.colors["bg_card"],
                fg=self.colors["text_primary"],
                justify=tk.RIGHT
            )
            score_line.pack(anchor=tk.E, padx=15, pady=3)
            
            # Percentage
            percentage_line = tk.Label(
                item_frame,
                text=f"درصد: {result['percentage']:.1f}%",
                font=self.font_small,
                bg=self.colors["bg_card"],
                fg=self.colors["success"],
                justify=tk.RIGHT
            )
            percentage_line.pack(anchor=tk.E, padx=15, pady=(3, 15))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _back_to_main(self):
        """Back to main page"""
        self._create_main_page()

def main():
    """Main function"""
    root = tk.Tk()
    root.configure(bg="#0f172a")
    
    app = ModernApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
