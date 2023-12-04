from django.urls import path
from dorama_info import views

app_name = 'dorama_info'

urlpatterns = [
    path('<slug:dorama_name_slug>/', views.dorama_info, name='dorama-info'),
]
