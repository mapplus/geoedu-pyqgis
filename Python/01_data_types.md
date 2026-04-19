# 01. 자료형

## 학습 목표

- Python에서 자주 사용하는 기본 자료형을 구분할 수 있다.
- 형변환이 왜 필요한지 이해할 수 있다.
- QGIS Python Console에서 값을 확인하는 습관을 익힌다.

## 핵심 자료형

- `int`: 정수
- `float`: 실수
- `str`: 문자열
- `bool`: 참/거짓
- `None`: 아직 값이 없음을 나타내는 특수 값

```python
count = 3
length = 12.5
layer_name = "roads"
is_valid = True
selected_layer = None

print(type(count))
print(type(length))
print(type(layer_name))
print(type(is_valid))
print(type(selected_layer))
```

## 숫자와 연산

```python
print(10 + 3)
print(10 - 3)
print(10 * 3)
print(10 / 3)
print(10 // 3)
print(10 % 3)
print(2 ** 4)
```

## 문자열

```python
layer_name = "Parcels"

print(layer_name[0])
print(layer_name[:3])
print(len(layer_name))
print(layer_name.lower())
print(layer_name.upper())
print(layer_name.replace("Parcel", "Building"))
```

## bool과 비교

```python
feature_count = 15

print(feature_count > 10)
print(feature_count == 15)
print(feature_count != 0)
```

## 형변환

QGIS 콘솔에서는 `input()`보다 이미 주어진 값을 바꿔 보는 방식이 더 자연스럽습니다.

```python
text_count = "25"
count = int(text_count)

text_ratio = "0.75"
ratio = float(text_ratio)

print(count + 5)
print(ratio * 100)
```

## 꼭 짚고 갈 것

- `type()`으로 현재 자료형을 확인할 수 있다.
- 숫자처럼 보여도 따옴표가 있으면 문자열이다.
- `None`은 오류가 아니라 "아직 값이 없음"을 의미할 수 있다.

## 같이 해보기

1. 반지름 값을 변수에 넣고 원 넓이를 계산해 봅니다.
2. `"100"`을 정수로 바꾼 뒤 50을 더해 봅니다.
3. 레이어 이름 문자열을 대문자로 바꿔 봅니다.

## PyQGIS 연결

- 좌표값은 숫자 자료형으로 다룹니다.
- 레이어 이름과 필드 이름은 문자열로 다룹니다.
- 객체가 아직 없을 때 `None`을 자주 만나게 됩니다.

