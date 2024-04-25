from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views import generic

from flashcard.models import FlashcardSet, Flashcard


def index(request: WSGIRequest):
    your_fcs_list: QuerySet[FlashcardSet]

    if request.user.is_anonymous:
        your_fcs_list = QuerySet[FlashcardSet]()
    else:
        your_fcs_list = FlashcardSet.objects.filter(created_by=request.user)

    return render(
        request,
        "flashcard/fcs_list.html",
        {
            "your_fcs_list": your_fcs_list,
        },
    )


def fcs_detail(request: WSGIRequest, fcs_id: int):
    fcs: FlashcardSet = get_object_or_404(FlashcardSet, pk=fcs_id)
    list_fc: QuerySet[Flashcard] = Flashcard.objects.filter(flashcard_set=fcs)

    return render(
        request,
        "flashcard/fcs_detail.html",
        {
            "fcs": fcs,
            "list_fc": list_fc,
        },
    )


class FlashcardDetailView(generic.DetailView):
    model = Flashcard
    template_name = "flashcard/fc_detail.html"
    context_object_name = "flashcard"
    pk_url_kwarg = "fc_id"

    def get_queryset(self):
        return Flashcard.objects.filter(created_by=self.request.user)
