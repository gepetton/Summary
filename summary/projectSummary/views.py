from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # 파일을 저장할 경로 지정
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        # 파일 저장
        path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        return JsonResponse({'message': '파일이 업로드되었습니다.'})
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

def list_files(request):
    file_list = []
    for filename in os.listdir(settings.MEDIA_ROOT):
        # 숨김파일 표시 안되게끔
        if filename == '.DS_Store':
            continue
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.isfile(file_path):
            file_list.append({
                'name': filename,
                'size': os.path.getsize(file_path),
            })
    return JsonResponse(file_list, safe=False)