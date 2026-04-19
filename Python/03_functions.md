# 03. 함수

## 학습 목표

- 반복되는 작업을 함수로 묶을 수 있다.
- `return`으로 결과를 돌려주는 방식을 이해한다.
- PyQGIS 코드에서 재사용 가능한 도구 함수를 만들 준비를 한다.

## 기본 구조

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)
```

## 기본값 인수

```python
def greet(name, prefix="안녕하세요"):
    print(f"{prefix}, {name}")

greet("QGIS")
greet("Python", prefix="반갑습니다")
```

## 여러 값 반환

```python
def calculate(a, b):
    return a + b, a * b

sum_value, mul_value = calculate(2, 4)
print(sum_value)
print(mul_value)
```

## 가변 인수

```python
def add_many(*numbers):
    total = 0
    for number in numbers:
        total += number
    return total

print(add_many(1, 2, 3, 4))
```

## 지역 변수와 전역 변수

```python
message = "전역"

def show_message():
    local_message = "지역"
    print(message)
    print(local_message)

show_message()
```

## print와 return의 차이

- `print()`는 화면에 보여 줍니다.
- `return`은 함수 밖으로 결과를 돌려줍니다.

## 같이 해보기

1. 두 수 중 큰 값을 반환하는 함수를 만들어 봅니다.
2. 문자열을 받아 `"레이어: ..."` 형태로 반환하는 함수를 만들어 봅니다.
3. 숫자 리스트를 받아 평균을 반환하는 함수를 만들어 봅니다.

## PyQGIS 연결

앞으로는 아래 같은 함수를 자주 만들게 됩니다.

- 레이어 존재 여부 확인 함수
- 필드 존재 여부 확인 함수
- 결과 메시지 생성 함수

