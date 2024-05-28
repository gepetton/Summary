from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from urllib.parse import unquote
from gptConvert import summarize_and_generate
from ocrConrtoller import ocr_image
from sttController import transcribe_audio
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

@require_http_methods(['GET'])
def get_file_content(request, filename):
    decoded_filename = unquote(filename)  # URL 디코딩
    file_path = os.path.join(settings.MEDIA_ROOT, decoded_filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain')
    return JsonResponse({'error': '파일을 찾을 수 없습니다.'}, status=404)


@require_http_methods(['PUT'])
def update_file_content(request, filename):

    decoded_filename = unquote(filename)  # URL 디코딩
    file_path = os.path.join(settings.MEDIA_ROOT, decoded_filename)
    if os.path.exists(file_path):
        edited_content = request.body.decode('utf-8')  # 요청 본문에서 수정된 내용 가져오기
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(edited_content)  # 수정된 내용으로 파일 덮어쓰기
        return JsonResponse({'success': True, 'message': '파일 내용이 업데이트되었습니다.'})
    return JsonResponse({'success': False, 'error': '파일을 찾을 수 없습니다.'}, status=404)

@csrf_exempt
def gpt_conversion(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            result = summarize_and_generate(prompt)
            return JsonResponse({'response': result})
        else:
            return HttpResponseBadRequest('프롬프트가 없습니다.')
    return HttpResponseBadRequest('잘못된 요청입니다.')

@csrf_exempt
def ocr_conversion(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            file_path = default_storage.save(f'uploads/{file.name}', file)

            # OCR 변환
            full_file_path = default_storage.path(file_path)
            result = ocr_image(full_file_path)

            return JsonResponse({'text': result})
        else:
            return HttpResponseBadRequest('파일이 없습니다.')
    return HttpResponseBadRequest('잘못된 요청입니다.')

@csrf_exempt
def stt_conversion(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            file_path = default_storage.save(f'uploads/{file.name}', file)

            # STT 변환
            full_file_path = default_storage.path(file_path)
            result = transcribe_audio(full_file_path)

            return JsonResponse({'transcript': result})
        else:
            return HttpResponseBadRequest('파일이 없습니다.')
    return HttpResponseBadRequest('잘못된 요청입니다.')