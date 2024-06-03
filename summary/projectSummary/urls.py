from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploads/', views.upload_file, name='upload_file'),
    path('uploads/list/', views.list_files, name='list_files'),
    path('gets/file/content/<str:filename>/', views.get_file_content, name='get_file_content'),
    path('updates/file/content/<str:filename>', views.update_file_content, name='update_file_content'),
    path('gpt/conversion/', views.gpt_conversion, name='gpt_conversion'),
    path('ocr/conversion/', views.ocr_conversion, name='ocr_conversion'),
    path('stt/conversion/', views.stt_conversion, name='stt_conversion'),
    path('sub1/', views.sub1_page, name='sub1_page'), # 일반 노트 페이지 이동 path
]