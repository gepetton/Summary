from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploads/', views.upload_file, name='upload_file'),
]