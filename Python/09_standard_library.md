# 09. 표준 라이브러리

## 학습 목표

- Python이 기본 제공하는 유용한 모듈을 익힌다.
- 간단한 계산, 날짜 처리, 경로 처리, JSON 처리를 해 본다.
- PyQGIS 자동화에 바로 연결할 수 있는 표준 도구를 확보한다.

## math

```python
import math

print(math.ceil(3.2))
print(math.floor(3.8))
print(math.sqrt(25))
```

## random

```python
import random

print(random.randint(1, 10))
```

## datetime

```python
from datetime import datetime, timedelta

now = datetime.now()
tomorrow = now + timedelta(days=1)

print(now)
print(tomorrow)
```

## pathlib

```python
from pathlib import Path

current_path = Path.cwd()
print(current_path)
```

## json

```python
import json

data = {"layer": "roads", "count": 120}
text = json.dumps(data, ensure_ascii=False, indent=2)
print(text)
```

## 같이 해보기

1. `math`로 반올림과 제곱근을 계산해 봅니다.
2. 현재 시각과 하루 뒤 시각을 출력해 봅니다.
3. 딕셔너리를 JSON 문자열로 바꿔 봅니다.

## PyQGIS 연결

- `datetime`: 실행 시간 기록
- `pathlib`: 결과 파일 경로 생성
- `json`: 설정값 저장

