# 복통 분류 API

- Flask API 서버
    - Python 3.8.3, Flask 2.2.2
    - GET 방식 호출



- 설치 및 실행
    - `sh install_mecab.sh`
    - `pip install -r requirments.txt`
    - `python app.py`



- API 호출

    - 포트 번호는 app.py 의 가장 마자막에 있는 port 수정하면 됩니다.

    - 현재는 16022 이므로, 다음과 같이 request 보냅니다

    - ```
        localhost:16022/predict?verbose=0&center=국군수도병원&age=24&gender=1&height=176&weight=72&pain_nrs=1&temperature=37&pulse=120&respiration=16&symtom=회덮밥을 먹은 후 복통 호소&is_operation=0&is_pain=0&is_medical_history=0&is_alertness=1&is_digestive=0&is_hemoptysis=0&is_blood_excrement=0
        ```

    - `localhost:16022/predict?` 까지는 고정이고 이후에 원하는 데이터를 각 항목에 삽입합니다. 

        - 현재 예시 url 은 다음과 같은 정보를 표현합니다.
            - verbose: 세부 항목 표시 여부 (0: N / 1: Y)
            - center: 병원 소재지
            - age: 나이
            - gender: 성별 (0: 여, 1: 남)
            - height: 신장 (cm)
            - weight: 체중 (kg)
            - pain_nrs: 고통 점수 (1~10)
            - temperature: 체온
            - pulse: 맥박
            - respiration: 호흡
            - symtom: 주증상
            - is_operation: 과거 수술력
            - is_pain: 통증 유무 (0: N / 1: Y)
            - is_medical_history: 과거 병력 (0: N / 1: Y)
            - is_alertness: 의식 유무 (0: N / 1: Y)
            - is_digestive: 소화기계 이상 (0: N / 1: Y)
            - is_hemoptysis: 각혈 유무 (0: N / 1: Y)
            - is_blood_excrement: 혈변 유무 (0: N / 1: Y)



- 결과 예시
    - postman 을 이용하여 request 하였습니다. 직접 타이핑하면 힘드니 이러한 툴을 사용하시는 것이 편합니다. 
    - Verbose True (기입한 세부 항목 노출 요청)
    - ![](/Users/jonghyun/Workspace/StomachNet/figures/api_request_example_2_verbose_true.png)
    - Verbose  False (예측 결과만 가져오기)
    - ![](/Users/jonghyun/Workspace/StomachNet/figures/api_request_example_1_verbose_false.png)

