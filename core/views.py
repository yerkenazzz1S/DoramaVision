import csv
import os

from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from dorama_info import models


def index(requests):
    return render(requests, 'core/index.html')


def load_data(requests):
    csv_filepath_genre = os.path.join(settings.BASE_DIR, 'genres.csv')
    # Загрузка жанров
    with open(csv_filepath_genre, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Проверяем, существует ли объект с таким слагом
            existing_genre = models.DoramaGenre.objects.filter(slug=row['genre_slug']).first()

            if existing_genre:
                # Если существует, используем его
                genre = existing_genre
            else:
                # В противном случае, создаем новый объект
                genre, created = models.DoramaGenre.objects.get_or_create(
                    genre_name=row['genre_name'],
                    slug=row['genre_slug']
                )

    csv_filepath_actors = os.path.join(settings.BASE_DIR, 'actors.csv')

    with open(csv_filepath_actors, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            actor, created = models.DoramaActor.objects.get_or_create(
                actor_name=row['actor_name'],
                slug=row['actor_slug']
            )

    csv_filepath_translate = os.path.join(settings.BASE_DIR, 'translate.csv')

    with open(csv_filepath_translate, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            translate, created = models.DoramaTranlate.objects.get_or_create(
                translate_name=row['translate'],
                slug=row['translate_slug']
            )

    status_list = [
        ['released', 'Вышел'],
        ['ongoing', 'Выходит']
    ]

    for status_data in status_list:
        status, created = models.DoramaStatus.objects.get_or_create(
            status_name=status_data[1],
            slug=status_data[0]
        )

    country_list = [
        ['Япония', 'iaponiia'],
        ['Таиланд', 'tailand'],
        ['Южная Корея', 'iuzhnaia-koreia'],
        ['Китай', 'kitai'],
        ['Тайвань', 'taivan']
    ]

    for country_data in country_list:
        country, created = models.DoramaCountry.objects.get_or_create(
            country_name=country_data[0],
            slug=country_data[1]
        )

    csv_filepath = os.path.join(settings.BASE_DIR, 'dorama_info.csv')
    with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Создаем объект Anime
            dorama = models.Dorama()

            # Заполняем обязательные поля
            dorama.name = row['name']
            dorama.slug = row['slug']
            dorama.release_year = int(row['release_year'])
            dorama.description = row['desc']
            dorama.duration_minutes = row['duration_minutes']
            dorama.duration_episodes = row['duration_episodes']

            posters_dir = str(settings.BASE_DIR).replace("\\", "/").lstrip("/")
            relative_path = row['poster_dorama_src'].replace("\\", "/").lstrip("/")
            poster_path = str(os.path.join(posters_dir, relative_path)).replace("\\", "/")
            if os.path.exists(poster_path):
                with open(poster_path, 'rb') as poster_file:
                    dorama.poster.save(row['poster_dorama_src'], File(poster_file), save=False)
            # dorama.save()

                    # Обработка и добавление статуса
            translate, _ = models.DoramaTranlate.objects.get_or_create(translate_name=row['translate'])
            dorama.translate = translate

            # Обработка и добавление статуса
            status, _ = models.DoramaStatus.objects.get_or_create(status_name=row['status'])
            dorama.status = status

            # Обработка и добавление страны
            country, _ = models.DoramaCountry.objects.get_or_create(country_name=row['country'])
            dorama.country = country

            # Сохраняем объект Dorama перед добавлением связей многие ко многим
            dorama.save()

            # Обработка и добавление актеров
            actors = row['actors'].split(',')
            for actor_name in actors:
                actor, _ = models.DoramaActor.objects.get_or_create(actor_name=actor_name.strip())
                dorama.actors.add(actor)

            # Обработка и добавление жанров
            genres = row['genre'].split(',')
            for genre_name in genres:
                genre, _ = models.DoramaGenre.objects.get_or_create(genre_name=genre_name.strip())
                dorama.genres.add(genre)

            # Сохраняем объект Dorama после добавления связей многие ко многим
            dorama.save()

    return HttpResponse("Данные успешно загружены в модели.")