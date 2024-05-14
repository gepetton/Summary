import openai
import secret

# OpenAI API 키 설정 (개인 키를 사용해야 합니다)
openai.api_key = secret.gpt_Api_key

def summarize_and_generate(input_text):
    # GPT-3.5 Turbo Instruct 모델 선택
    model = "gpt-3.5-turbo-instruct"

    try:
        # OpenAI Completion 요청 보내기
        response = openai.Completion.create(
            engine=model,
            prompt=input_text+"내용을 정리해서 문단으로 나눠서 요약하고 추가 정보도 주석으로 달아줘. 총 내용은 500자 이내로 부탁해",
            max_tokens=1000  # 생성할 최대 토큰 수 설정 (요약 및 추가 내용에 사용될 최대 토큰 수)
        )

        if response and len(response.choices) > 0:
            # 생성된 응답 추출
            answer = response.choices[0].text.strip()
            return answer
        else:
            return "응답을 생성할 수 없습니다."

    except Exception as e:
        print("오류 발생:", e)
        return "오류 발생"


# 테스트를 위한 입력 텍스트
input_text =  input()

# 입력 텍스트 요약 및 추가 내용 생성 함수 호출
result = summarize_and_generate(input_text)
print("요약 및 추가 내용:", result)