# 10. 미니 프로젝트

## 목표

Python 기초 문법을 한 번에 묶어서 작은 콘솔 실습을 완성해 봅니다.  
QGIS Python Console에서 일부를 실행하고, 최종 코드는 `.py` 파일로 정리해도 좋습니다.

## 추천 주제 A. 레이어 요약 정보 정리기

### 구현 목표

- 레이어 이름 목록을 준비한다.
- 각 레이어의 피처 수를 딕셔너리로 정리한다.
- 조건에 따라 메시지를 다르게 출력한다.
- 결과를 텍스트 파일이나 CSV로 저장한다.

### 적용 문법

- 자료형
- 제어문
- 함수
- 자료구조
- 파일 입출력
- 예외 처리

### 예시 구조

```python
layer_summary = {
    "roads": 120,
    "buildings": 48,
    "parcels": 350,
}

def show_summary(summary):
    for layer_name, feature_count in summary.items():
        print(f"{layer_name}: {feature_count}")

show_summary(layer_summary)
```

## 추천 주제 B. 업무 할 일 목록 정리기

### 구현 목표

- 할 일 목록을 리스트로 관리한다.
- 완료 여부를 조건문으로 출력한다.
- 결과를 파일로 저장한다.

## 발표 포인트

- 어떤 자료구조를 왜 선택했는지
- 반복문과 함수를 어떻게 나눴는지
- 저장 파일 형식을 왜 그렇게 정했는지

## PyQGIS로 확장하기

이 프로젝트를 PyQGIS로 확장하면 다음과 같은 형태가 됩니다.

- 현재 프로젝트의 레이어 목록 요약하기
- 특정 레이어의 피처 개수 저장하기
- 결과를 CSV로 내보내기

