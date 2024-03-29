from django.db import models
from datetime import timedelta

from django.utils import timezone


class FlashcardSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(default="", max_length=5000)
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    last_reviewed = models.DateField(null=True)
    next_review = models.DateField(null=True)
    ease_factor = models.FloatField(default=2.5)
    repetition = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def update_review(self, success, quality):
        if success:
            self.repetition += 1
        else:
            self.repetition = 0

        self.ease_factor = max(1.3, self.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

        self.last_reviewed = timezone.now()
        self.next_review = self.last_reviewed + timedelta(days=self.repetition * self.ease_factor)


class Review(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    success = models.BooleanField()
    quality = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for flashcard: {self.flashcard.question}'
