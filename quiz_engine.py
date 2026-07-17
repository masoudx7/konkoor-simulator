# Quiz Engine and Scoring

import random
from questions import get_questions, get_subjects

class Quiz:
    def __init__(self, subject, num_questions=5):
        """
        Start a new quiz
        
        Args:
            subject: Subject name
            num_questions: Number of questions
        """
        self.subject = subject
        self.num_questions = num_questions
        self.questions = []
        self.user_answers = []
        self.current_question_index = 0
        self.score = 0
        
        self._prepare_questions()
    
    def _prepare_questions(self):
        """Select random questions for the subject"""
        all_questions = get_questions(self.subject)
        
        if len(all_questions) == 0:
            raise ValueError(f"Subject {self.subject} does not exist")
        
        # Select random questions
        num = min(self.num_questions, len(all_questions))
        self.questions = random.sample(all_questions, num)
    
    def get_current_question(self):
        """Return current question"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def submit_answer(self, choice):
        """Submit user answer"""
        current_question = self.get_current_question()
        
        if current_question is None:
            return False
        
        self.user_answers.append({
            'number': self.current_question_index + 1,
            'question': current_question['question'],
            'user_choice': choice,
            'correct_choice': current_question['correct_answer'],
            'is_correct': choice == current_question['correct_answer']
        })
        
        if choice == current_question['correct_answer']:
            self.score += 1
        
        self.current_question_index += 1
        return True
    
    def is_completed(self):
        """Check if quiz is completed"""
        return self.current_question_index >= len(self.questions)
    
    def calculate_percentage(self):
        """Calculate percentage score"""
        if len(self.questions) == 0:
            return 0
        return (self.score / len(self.questions)) * 100
    
    def get_report(self):
        """Get detailed result report"""
        report = {
            'subject': self.subject,
            'total_questions': len(self.questions),
            'score': self.score,
            'percentage': self.calculate_percentage(),
            'answers': self.user_answers
        }
        return report
    
    def get_grade(self):
        """Determine letter grade based on percentage"""
        percentage = self.calculate_percentage()
        
        if percentage >= 90:
            return 'ممتاز ⭐⭐⭐⭐⭐'
        elif percentage >= 80:
            return 'خیلی خوب ⭐⭐⭐⭐'
        elif percentage >= 70:
            return 'خوب ⭐⭐⭐'
        elif percentage >= 60:
            return 'متوسط ⭐⭐'
        elif percentage >= 50:
            return 'قابل قبول ⭐'
        else:
            return 'ضعیف'

class QuizManager:
    def __init__(self):
        """Manage all quizzes"""
        self.current_quiz = None
        self.history = []
    
    def start_new_quiz(self, subject, num_questions=5):
        """Start a new quiz"""
        try:
            self.current_quiz = Quiz(subject, num_questions)
            return True
        except ValueError:
            return False
    
    def save_result(self):
        """Save quiz result to history"""
        if self.current_quiz:
            report = self.current_quiz.get_report()
            self.history.append(report)
    
    def get_current_quiz(self):
        """Get current quiz"""
        return self.current_quiz
    
    def get_history(self):
        """Get history of all quizzes"""
        return self.history
