import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from userauths.models import User


fs = FileSystemStorage(location='media/posters', base_url='/media/posters/')


def upload_poster_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return f'{slugify(instance.slug)}_poster{file_extension}'


class DoramaGenre(models.Model):
    genre_name = models.CharField(max_length=100, unique=True, verbose_name='Название жанра')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.genre_name


class DoramaActor(models.Model):
    actor_name = models.CharField(max_length=100, verbose_name='Имя актёра')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.actor_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.actor_name


class DoramaCountry(models.Model):
    country_name = models.CharField(max_length=100, unique=True, verbose_name='Названия страны')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.country_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.country_name


class DoramaStatus(models.Model):
    status_name = models.CharField(max_length=10, unique=True, verbose_name='Статус дорамы')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.status_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
        # return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.status_name


class DoramaTranlate(models.Model):
    translate_name = models.CharField(max_length=10, unique=True, verbose_name='Статус дорамы')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.translate_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    # return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.translate_name


class Dorama(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    description = models.TextField(verbose_name='Описание')
    country = models.ForeignKey(DoramaCountry, max_length=100, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Страна')
    release_year = models.PositiveIntegerField(verbose_name='Год выпуска')
    duration_minutes = models.CharField(max_length=100, verbose_name='Продолжительность в минутах')
    duration_episodes = models.PositiveIntegerField(verbose_name='Продолжительность в сериях')
    genres = models.ManyToManyField(DoramaGenre, blank=True, null=True, verbose_name='Жанры')
    actors = models.ManyToManyField(DoramaActor, blank=True, null=True, verbose_name='Актёры')
    translations = models.ForeignKey(DoramaTranlate, on_delete=models.CASCADE, blank=True, verbose_name='Переводы', null=True)
    status = models.ForeignKey(DoramaStatus, on_delete=models.CASCADE, verbose_name='Статус аниме', null=True, blank=True)
    poster = models.ImageField(upload_to=upload_poster_path, storage=fs, verbose_name='Постер аниме', blank=True,
                               null=True, default='default_dorama_poster.jpg')

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dorama_info:dorama-info', args=[str(self.slug)])

    def __str__(self):
        return self.name
