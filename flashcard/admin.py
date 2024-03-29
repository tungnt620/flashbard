from django.contrib import admin

from .models import Flashcard, FlashcardSet, Review

admin.site.register(Flashcard)
admin.site.register(FlashcardSet)
admin.site.register(Review)
