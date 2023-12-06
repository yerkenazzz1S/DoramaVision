import csv
import os
import joblib
import numpy as np
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from django.conf import settings
from django.core.files import File
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from dorama_info import models


def get_dorama_slug(requests):
    def get_dorama(query):
        count_vectorizer = joblib.load(os.path.join(settings.BASE_DIR, 'core\\pkl\\count_vectorizer_model.pkl'))
        count_matrix = joblib.load(os.path.join(settings.BASE_DIR, 'core\\pkl\\count_matrix_model.pkl'))

        csv_file_path = os.path.join(settings.BASE_DIR, 'dorama_info.csv')  # Укажите путь к вашему датасету
        df = pd.read_csv(csv_file_path)

        def lemmatize_text(text):
            lemmatizer = WordNetLemmatizer()
            words = nltk.word_tokenize(text)
            return ' '.join([lemmatizer.lemmatize(w) for w in words])

        def jaccard_similarity(query, matrix):
            query_vector = count_vectorizer.transform([query])

            # Преобразуем вектор запроса и матрицу признаков в множества
            query_set = set(query_vector.indices)
            matrix_set = set(matrix.indices)

            # Вычисляем сходство Жаккара
            intersection = len(query_set.intersection(matrix_set))
            union = len(query_set.union(matrix_set))

            return intersection / union if union != 0 else 0

        lemmatized_query = lemmatize_text(query)

        jaccard_similarities = [jaccard_similarity(lemmatized_query, row) for row in count_matrix]

        top_index = np.argmax(jaccard_similarities)
        recommended_slug = df['slug'].iloc[top_index]
        return recommended_slug

    if requests.method == 'POST':
        comment_text = requests.POST.get('comment', '')
        # Обработайте comment_text и получите slug (замените этот код на свою логику)
        slug = get_dorama(comment_text)
        dorama = get_object_or_404(models.Dorama, slug=slug)
        similar_dorama = models.Dorama.objects.filter(genres__in=dorama.genres.all()).exclude(id=dorama.id).distinct()[:8]

        context = {
            'dorama': dorama,
            'similar_dorama': similar_dorama
        }
        return render(requests, 'dorama_info/dorama_info.html', context)
    else:
        return render(requests, 'core/index.html')


def index(requests):
    doramas = models.Dorama.objects.all()
    paginator = Paginator(doramas, 10)

    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(requests, 'core/index.html', context)


def get_genre(requests, dorama_genre_slug):
    genre = get_object_or_404(models.DoramaGenre, slug=dorama_genre_slug)
    dorama_list = genre.dorama_set.all().order_by('-release_year')
    paginator = Paginator(dorama_list, 10)

    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(requests, 'core/index.html', context)


def get_translate(requests, dorama_translate_slug):
    translate = get_object_or_404(models.DoramaTranlate, slug=dorama_translate_slug)
    dorama_list = translate.dorama_set.all().order_by('-release_year')
    paginator = Paginator(dorama_list, 10)

    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(requests, 'core/index.html', context)


def get_country(requests, dorama_country_slug):
    country = get_object_or_404(models.DoramaCountry, slug=dorama_country_slug)
    dorama_list = country.dorama_set.all().order_by('-release_year')
    paginator = Paginator(dorama_list, 10)

    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(requests, 'core/index.html', context)


def get_status(requests, dorama_status_slug):
    status = get_object_or_404(models.DoramaStatus, slug=dorama_status_slug)
    dorama_list = status.dorama_set.all().order_by('-release_year')
    paginator = Paginator(dorama_list, 10)

    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(requests, 'core/index.html', context)


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
            dorama.translations = translate

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