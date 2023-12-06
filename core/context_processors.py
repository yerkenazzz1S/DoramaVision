from dorama_info import models


def accept(request):
    all_genres = models.DoramaGenre.objects.all()
    all_translates = models.DoramaTranlate.objects.all()
    all_status = models.DoramaStatus.objects.all()
    all_country = models.DoramaCountry.objects.all()
    dorama_the_best = models.Dorama.objects.order_by('-release_year')[:12]
    dorama_released = models.Dorama.objects.filter(status__slug='released')[:8]
    dorama_ongoing = models.Dorama.objects.filter(status__slug='ongoing')[8:17]

    return {
        'all_genres': all_genres,
        'all_translates': all_translates,
        'all_status': all_status,
        'all_country': all_country,
        'dorama_the_best': dorama_the_best,
        'dorama_released': dorama_released,
        'dorama_ongoing': dorama_ongoing
    }
