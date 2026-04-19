# 07. 오류와 예외

## 학습 목표

- 에러 메시지를 읽고 원인을 추적하는 습관을 익힌다.
- 프로그램이 중단되지 않도록 예외를 처리할 수 있다.
- PyQGIS 작업에서 자주 만나는 오류 상황에 대비한다.

## 대표적인 오류

- `NameError`: 이름이 정의되지 않음
- `TypeError`: 자료형이 맞지 않음
- `ValueError`: 값의 형식이 맞지 않음
- `FileNotFoundError`: 파일이 없음

## try / except

```python
text_value = "abc"

try:
    value = int(text_value)
    print(value)
except ValueError:
    print("정수로 바꿀 수 없는 값입니다.")
```

## else / finally

```python
try:
    value = int("10")
except ValueError:
    print("변환 실패")
else:
    print("변환 성공:", value)
finally:
    print("처리를 마칩니다.")
```

## 파일 예외 처리

```python
from pathlib import Path

file_path = Path.home() / "missing_file.txt"

try:
    with file_path.open("r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
```

## 꼭 짚고 갈 것

- 에러가 나면 메시지를 읽고 몇 번째 줄인지 먼저 봅니다.
- `except:`만 쓰지 말고 가능한 한 구체적인 예외를 잡습니다.
- 예외 처리는 문제를 숨기는 것이 아니라 상황을 통제하는 방법입니다.

## 같이 해보기

1. 숫자 문자열과 일반 문자열을 각각 `int()`로 바꿔 봅니다.
2. 존재하지 않는 파일을 읽어 보고 예외를 처리해 봅니다.
3. `NameError`를 일부러 만들고 메시지를 확인해 봅니다.

## PyQGIS 연결

- 레이어가 없는 경우
- 필드명이 다른 경우
- 경로가 잘못된 경우
- 선택한 객체가 없는 경우

