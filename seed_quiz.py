from django.core.management.base import BaseCommand
from quiz.models import Question
import random

class Command(BaseCommand):
    help = 'Seed the database with initial quiz questions and subjects'

    def generate_questions(self, subject, count):
        questions = []
        for i in range(1, count + 1):
            questions.append({
                'subject': subject,
                'question': f'{subject} Question {i}: What is the answer?',
                'option1': 'Option 1',
                'option2': 'Option 2',
                'option3': 'Option 3',
                'option4': 'Option 4',
                'correct_option': random.randint(1, 4),
            })
        return questions

    def handle(self, *args, **kwargs):
        subjects = ['Python', 'DSA', 'DBMS']
        all_questions = []
        for subject in subjects:
            all_questions.extend(self.generate_questions(subject, 50))

        for q in all_questions:
            Question.objects.create(
                subject=q['subject'],
                question=q['question'],
                option1=q['option1'],
                option2=q['option2'],
                option3=q['option3'],
                option4=q['option4'],
                correct_option=q['correct_option'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded approx 50 questions per subject'))
