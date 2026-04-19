# 04. 자료구조

## 학습 목표

- 리스트, 튜플, 딕셔너리, 집합의 차이를 이해한다.
- 상황에 맞는 자료구조를 고를 수 있다.
- PyQGIS에서 속성, 설정값, 목록 데이터를 다룰 준비를 한다.

## 리스트

순서가 있고, 수정할 수 있는 자료구조입니다.

```python
layer_names = ["roads", "buildings", "parcels"]

print(layer_names[0])
layer_names.append("rivers")
print(layer_names)
```

## 튜플

순서가 있지만, 변경하지 않는 값을 묶을 때 적합합니다.

```python
point = (127.12, 37.45)
x, y = point
print(x, y)
```

## 딕셔너리

이름표로 값을 찾을 때 사용합니다.

```python
layer_info = {
    "name": "roads",
    "geometry": "LineString",
    "feature_count": 1520
}

print(layer_info["name"])
print(layer_info["feature_count"])
```

## 집합

중복 제거와 포함 검사에 강합니다.

```python
field_names = {"id", "name", "name", "length"}
print(field_names)
print("name" in field_names)
```

## 반복과 함께 쓰기

```python
layer_info = {
    "roads": 120,
    "buildings": 48,
    "parcels": 350
}

for layer_name, feature_count in layer_info.items():
    print(layer_name, feature_count)
```

## 어떤 때 무엇을 쓰나

- 리스트: 순서대로 처리할 항목이 있을 때
- 튜플: 좌표처럼 한 번 정하면 잘 바뀌지 않는 값
- 딕셔너리: 이름과 값의 짝으로 관리할 때
- 집합: 중복 제거가 필요할 때

## 같이 해보기

1. 레이어 이름 4개를 리스트로 만들고 하나를 추가해 봅니다.
2. 좌표 1개를 튜플로 저장해 봅니다.
3. 사번, 이름, 부서를 딕셔너리로 저장해 봅니다.
4. 중복된 필드명을 집합으로 정리해 봅니다.

## PyQGIS 연결

- 레이어 목록은 리스트처럼 다루게 됩니다.
- 피처 속성은 딕셔너리처럼 이해하면 접근이 쉬워집니다.
- 좌표쌍은 튜플로 생각하면 편합니다.

