from django.urls import path
from core import views
from core import middleware

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('load_data/', views.load_data, name='load-data'),
    # path('recommendation/', middleware.recommendation_middleware, name='recommendation_middleware'),
path('get_dorama_slug/', views.get_dorama_slug, name='get_dorama_slug'),
    path('dorama_genre/<slug:dorama_genre_slug>/', views.get_genre, name='dorama_genre'),
    path('dorama_translate/<slug:dorama_translate_slug>/', views.get_translate, name='dorama-translate'),
    path('dorama_country/<slug:dorama_country_slug>/', views.get_country, name='dorama-country'),
    path('dorama_status/<slug:dorama_status_slug>/', views.get_status, name='dorama-status'),
]