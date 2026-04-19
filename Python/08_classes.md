# 08. 클래스

## 학습 목표

- 클래스와 인스턴스의 개념을 이해한다.
- 속성과 메서드를 하나로 묶는 이유를 이해한다.
- PyQGIS 플러그인 구조를 배울 때 필요한 최소 개념을 익힌다.

## 기본 구조

```python
class Employee:
    def __init__(self, name, team):
        self.name = name
        self.team = team

    def introduce(self):
        print(f"{self.team} 팀의 {self.name}입니다.")

employee = Employee("Kim", "Geo")
employee.introduce()
```

## 클래스와 인스턴스

- 클래스는 설계도입니다.
- 인스턴스는 실제로 만들어진 객체입니다.
- `self`는 자기 자신의 인스턴스를 가리킵니다.

## 속성과 메서드

```python
class LayerSummary:
    def __init__(self, name, feature_count):
        self.name = name
        self.feature_count = feature_count

    def show(self):
        print(f"{self.name}: {self.feature_count}")

summary = LayerSummary("roads", 120)
summary.show()
```

## 꼭 짚고 갈 것

- 클래스는 관련 있는 데이터와 동작을 묶을 때 사용합니다.
- 초급 단계에서는 상속보다 기본 구조 이해가 더 중요합니다.
- 플러그인 개발을 시작하면 클래스 문법을 더 자주 만나게 됩니다.

## 같이 해보기

1. `Book` 클래스를 만들고 제목과 저자를 저장해 봅니다.
2. `introduce()` 같은 메서드를 하나 추가해 봅니다.
3. 레이어 이름과 개수를 저장하는 클래스를 만들어 봅니다.

## PyQGIS 연결

플러그인 개발 단계에서는 다음처럼 클래스 기반 구조를 많이 사용합니다.

- 플러그인 메인 클래스
- 다이얼로그 클래스
- 설정 관리 클래스

