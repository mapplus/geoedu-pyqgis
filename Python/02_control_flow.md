# 02. 제어 흐름 도구

## 학습 목표

- 조건에 따라 다른 코드를 실행할 수 있다.
- 반복문을 사용해 같은 작업을 여러 번 수행할 수 있다.
- PyQGIS에서 레이어와 피처를 순회할 준비를 한다.

## if

```python
feature_count = 8

if feature_count == 0:
    print("피처가 없습니다.")
elif feature_count < 10:
    print("피처 수가 적습니다.")
else:
    print("피처가 충분합니다.")
```

## 비교와 논리 연산

```python
feature_count = 12
has_selection = True

print(feature_count > 10 and has_selection)
print(feature_count == 0 or not has_selection)
```

## for

```python
layer_names = ["roads", "buildings", "parcels"]

for layer_name in layer_names:
    print(layer_name)
```

## range

```python
for number in range(1, 6):
    print(number)
```

## while

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

## break와 continue

```python
for number in range(1, 11):
    if number == 3:
        continue
    if number == 8:
        break
    print(number)
```

## 같이 해보기

1. 점수 변수에 따라 `A`, `B`, `C`를 출력해 봅니다.
2. 리스트 안의 레이어 이름을 하나씩 출력해 봅니다.
3. 1부터 10까지 더하는 누적 합 코드를 작성해 봅니다.

## 꼭 짚고 갈 것

- `=`는 대입, `==`는 비교입니다.
- 반복문에서는 누적 변수 `total`, `count`를 자주 씁니다.
- `while`은 종료 조건을 먼저 확인하는 습관이 중요합니다.

## PyQGIS 연결

반복문은 PyQGIS에서 매우 자주 사용합니다.

- 레이어 목록 순회
- 피처 순회
- 필드 목록 확인
- 조건에 맞는 객체만 처리

