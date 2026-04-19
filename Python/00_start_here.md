# 00. 시작하기

## 같이 먼저 해볼 것

이미지 순서는 `자료형`부터 시작하지만, 시작 전에 아래 3가지는 먼저 같이 실행해 보겠습니다.

- 변수에 값을 저장하고 다시 출력해 보기
- Python Console에서 한 줄씩 실행하는 흐름 익히기
- 들여쓰기가 문법이라는 점 확인하기

```python
message = "Hello, QGIS Python Console"
team_name = "GeoEdu"

print(message)
print(f"{team_name} 실습을 시작합니다.")
```

## QGIS Python Console에서 익힐 것

- 코드를 한 줄씩 실행할 수 있다.
- 선택한 여러 줄도 함께 실행할 수 있다.
- 실행 결과를 바로 확인하면서 수정할 수 있다.
- 짧은 코드는 콘솔에서 실험하고, 정리된 코드는 `.py` 파일로 저장할 수 있다.

## 첫 확인 포인트

- `=`는 값을 저장할 때 사용한다.
- `print()`는 결과를 출력할 때 사용한다.
- 문자열은 따옴표로 감싼다.
- 들여쓰기를 틀리면 에러가 난다.

## 같이 해보기

```python
layer_name = "buildings"
feature_count = 10

print(layer_name)
print(feature_count)
print(layer_name, feature_count)
```

## 짧은 실습

1. 자신의 이름을 문자열 변수에 넣고 출력해 봅니다.
2. 정수 변수 두 개를 만들고 더한 결과를 출력해 봅니다.
3. `print(f"...")` 형식으로 자기소개 한 줄을 만들어 봅니다.

## PyQGIS 연결 메모

곧 배우게 될 PyQGIS에서도 방식은 같습니다.  
객체 이름을 변수에 담고, 값을 확인하고, 필요한 처리를 한 뒤 결과를 출력합니다.

