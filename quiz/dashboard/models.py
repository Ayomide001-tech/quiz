from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
CORRECT_ANSWER_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')

]

 
class category(models.Model):
    category_name = models.CharField(max_length = 30, default = 'uncategorized')
    time = models.PositiveIntegerField(default=60, help_text="Time in Minutes for this category quiz")

    def __str__(self):
        return self.category_name

class Question (models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='questions')
    
    question = models.TextField()
    option_a = models.CharField(max_length = 255)
    option_b = models.CharField(max_length = 255)
    option_c = models.CharField(max_length = 255)
    option_d = models.CharField(max_length = 255)
    correct_answer = models.CharField(max_length = 1, choices=CORRECT_ANSWER_CHOICES)

    def __str__(self):
        return self.question


@receiver(post_delete, sender=Question)
def delete_empty_category(sender, instance, **kwargs):
    category_id = instance.category_id
    if category_id is None:
        return

    category_obj = category.objects.filter(id=category_id).first()
    if category_obj and not category_obj.questions.exists():
        category_obj.delete()


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    category = models.ForeignKey(
        category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quiz_attempts'
    )
    score = models.PositiveIntegerField(default=0)
    total_question = models.PositiveIntegerField(default=0)
    completed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed']

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_question}"

# def get_absolute_url(self):
#         from django.urls import reverse
#         return reverse('quiz:quiz', args=[str(self.category.id)])