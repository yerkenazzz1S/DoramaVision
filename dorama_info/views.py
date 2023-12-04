from django.shortcuts import render, get_object_or_404
from . import models


def dorama_info(requests, dorama_name_slug):
    dorama = get_object_or_404(models.Dorama, slug=dorama_name_slug)
    similar_dorama = models.Dorama.objects.filter(genres__in=dorama.genres.all()).exclude(id=dorama.id).distinct()[:8]

    context = {
        'dorama': dorama,
        'similar_dorama': similar_dorama
    }
    return render(requests, 'dorama_info/dorama_info.html', context)