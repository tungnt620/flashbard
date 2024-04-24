from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

from django.utils import timezone


class FlashcardSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Flashcard(models.Model):
    question = models.TextField(max_length=200)
    answer = models.TextField(default="", max_length=5000)
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    last_reviewed = models.DateField(null=True)
    next_review = models.DateField(null=True)
    ease_factor = models.FloatField(default=2.5)
    repetition = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question

    def update_review(self, success: bool, quality: int) -> None:
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Review for flashcard: {self.flashcard.question}'


class ReviewSession(models.Model):
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Review)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Review session for flashcard set: {self.flashcard_set.title}'
