from django.urls import path

from . import views

app_name = "flashcard"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:fcs_id>/", views.fcs_detail, name="fcs_detail"),
    path("fc/<int:fc_id>/", views.FlashcardDetailView.as_view(), name="fc_detail"),
]
