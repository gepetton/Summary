import requests
import uuid
import time
import json
import secret

api_url = secret.ocr_Api_url
secret_key = secret.ocr_Api_key
image_file = './test.jpg'

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
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

for i in response.json()['images'][0]['fields']:
    text = i['inferText']
    print(text)
