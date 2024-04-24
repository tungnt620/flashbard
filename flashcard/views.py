from django.shortcuts import get_object_or_404, render

from flashcard.models import FlashcardSet, Flashcard


def index(request):
    your_fcs_list = FlashcardSet.objects.filter(created_by=request.user)

    return render(
        request,
        "flashcard/fcs_list.html",
        {
            "your_fcs_list": your_fcs_list,
        },
    )


def fcs_detail(request, fcs_id: int):
    fcs = get_object_or_404(FlashcardSet, pk=fcs_id)

    return render(
        request,
        "flashcard/fcs_detail.html",
        {
            "fcs": fcs,
        },
    )
