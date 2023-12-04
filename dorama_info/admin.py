from django.contrib import admin
from dorama_info import models


class DoramaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('id', 'slug', 'name', 'country', 'release_year', 'translations', 'status')
    list_filter = ('country', 'release_year', 'genres', 'translations', 'status')
    search_fields = ('name', 'slug')
    filter_horizontal = ('genres', 'actors')


admin.site.register(models.Dorama, DoramaAdmin)


class DoramaCountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['country_name']}
    list_display = ('id', 'slug', 'country_name')
    search_fields = ('slug', 'country_name')


admin.site.register(models.DoramaCountry, DoramaCountryAdmin)


class DoramaGenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['genre_name']}
    list_display = ('id', 'slug', 'genre_name')
    search_fields = ('slug', 'genre_name')


admin.site.register(models.DoramaGenre, DoramaGenreAdmin)


class DoramaActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['actor_name']}
    list_display = ('id', 'slug', 'actor_name')
    search_fields = ('slug', 'actor_name')


admin.site.register(models.DoramaActor, DoramaActorAdmin)


class DoramaStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['status_name']}
    list_display = ('id', 'slug', 'status_name')
    search_fields = ('slug', 'status_name')


admin.site.register(models.DoramaStatus, DoramaStatusAdmin)


class DoramaTranlateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['translate_name']}
    list_display = ('id', 'slug', 'translate_name')
    search_fields = ('slug', 'translate_name')


admin.site.register(models.DoramaTranlate, DoramaTranlateAdmin)


models.Dorama._meta.verbose_name_plural = 'Дорамы'
models.DoramaCountry._meta.verbose_name_plural = 'Страны'
models.DoramaGenre._meta.verbose_name_plural = 'Жанры'
models.DoramaStatus._meta.verbose_name_plural = 'Статус'
models.DoramaTranlate._meta.verbose_name_plural = 'Переводы'
models.DoramaActor._meta.verbose_name_plural = 'Актёры'
