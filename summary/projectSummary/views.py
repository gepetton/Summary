from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from urllib.parse import unquote
from .models import ConversionResult
from .gptConvert import summarize_and_generate
from .ocrConrtoller import ocr_image
from .sttController import transcribe_audio
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
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # 파일 저장
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))

        try:
            # 저장된 파일 경로 재확인
            absolute_file_path = os.path.join(settings.MEDIA_ROOT, saved_path)

            with open(absolute_file_path, 'r') as file:
                file_content = file.read()

            # 변환 작업 수행
            transformed_content = summarize_and_generate(file_content)

            # 변환된 내용을 기존 파일에 덮어쓰기
            with open(absolute_file_path, 'w') as file:
                file.write(transformed_content)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': '파일 변환 및 업데이트 성공', 'content': transformed_content})

    return JsonResponse({'error': 'Invalid request method or no file uploaded'}, status=400)

@csrf_exempt
def ocr_conversion(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # 파일 저장
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        absolute_saved_path = os.path.join(settings.MEDIA_ROOT, saved_path)
        try:
            # OCR 처리
            extracted_text = ocr_image(absolute_saved_path)
            # 추출한 텍스트 요약
            result_text = summarize_and_generate(extracted_text)
            # 기존 이미지 파일 삭제
            if os.path.exists(absolute_saved_path):
                os.remove(absolute_saved_path)

            # 추출된 텍스트를 같은 이름의 파일로 저장
            text_file_path = os.path.join(settings.MEDIA_ROOT, f"{os.path.splitext(uploaded_file.name)[0]}.txt")
            with open(text_file_path, 'w') as text_file:
                text_file.write(result_text)

            return JsonResponse({'message': 'OCR 처리 성공', 'file_path': text_file_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def stt_conversion(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # 파일 저장
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        absolute_saved_path = os.path.join(settings.MEDIA_ROOT, saved_path)

        try:
            # STT 변환 수행
            extracted_text = transcribe_audio(absolute_saved_path)
            result = summarize_and_generate(extracted_text)
            # 기존 오디오 파일 삭제
            if os.path.exists(absolute_saved_path):
                os.remove(absolute_saved_path)

            # 변환된 텍스트를 같은 이름의 파일로 저장
            text_file_path = os.path.join(settings.MEDIA_ROOT, f"{os.path.splitext(uploaded_file.name)[0]}.txt")
            with open(text_file_path, 'w') as text_file:
                text_file.write(result)

            return JsonResponse({'message': 'STT 처리 성공', 'file_path': text_file_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method or no file uploaded'}, status=400)


# @csrf_exempt
# def stt_conversion(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         if file:
#             file_path = default_storage.save(f'uploads/{file.name}', file)
#
#             # STT 변환
#             full_file_path = default_storage.path(file_path)
#             result = transcribe_audio(full_file_path)
#
#             return JsonResponse({'transcript': result})
#         else:
#             return HttpResponseBadRequest('파일이 없습니다.')
#     return HttpResponseBadRequest('잘못된 요청입니다.')