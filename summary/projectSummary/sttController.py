# sttController.py
import os
import io
from google.cloud import speech
import secret

# Google Cloud 인증 키 파일 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = secret.gcloud_credentials_path

def transcribe_audio(file_path, language='ko-KR'):
    """Google Cloud Speech-to-Text API를 사용하여 오디오 파일을 텍스트로 변환"""
    client = speech.SpeechClient()

    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return ' '.join(transcripts)