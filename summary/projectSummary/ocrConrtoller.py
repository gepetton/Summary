# ocrController.py
import requests
import uuid
import time
import json
import secret

api_url = secret.ocr_Api_url
secret_key = secret.ocr_Api_key

def ocr_image(image_file):
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', open(image_file, 'rb'))
    ]
    headers = {
        'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        try:
            results = [field['inferText'] for field in response.json()['images'][0]['fields']]
            return " ".join(results)
        except KeyError:
            return "응답에서 텍스트를 추출할 수 없습니다."
    else:
        return f"OCR 요청 실패: {response.status_code}"