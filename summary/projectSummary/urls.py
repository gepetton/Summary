from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploads/', views.upload_file, name='upload_file'),
    path('uploads/list/', views.list_files, name='list_files'),
    path('gets/file/content/<str:filename>/', views.get_file_content, name='get_file_content'),
    path('updates/file/content/<str:filename>', views.update_file_content, name='update_file_content'),
]