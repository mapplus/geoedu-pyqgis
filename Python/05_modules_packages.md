# 05. 모듈과 패키지

## 학습 목표

- 다른 파일이나 라이브러리의 기능을 가져와 쓸 수 있다.
- Python 기본 모듈과 QGIS 모듈을 구분할 수 있다.
- PyQGIS 코드의 시작점인 `qgis.core`를 자연스럽게 받아들인다.

## import 기본

```python
import math

print(math.sqrt(16))
```

## 필요한 것만 가져오기

```python
from datetime import datetime

print(datetime.now())
```

## 내가 만든 모듈 사용하기

`utils.py`

```python
def format_layer_name(name):
    return f"Layer: {name}"
```

`main.py`

```python
import utils

print(utils.format_layer_name("roads"))
```

## QGIS 모듈 맛보기

```python
from qgis.core import QgsProject

project = QgsProject.instance()
print(project.fileName())
```

## 꼭 짚고 갈 것

- `import *`는 초급 과정에서는 사용하지 않습니다.
- 표준 라이브러리와 QGIS 제공 모듈은 다릅니다.
- 같은 기능을 반복해서 쓰면 모듈로 분리할 수 있습니다.

## 같이 해보기

1. `math` 모듈로 제곱근을 계산해 봅니다.
2. `datetime`으로 현재 시각을 출력해 봅니다.
3. `QgsProject.instance()`를 실행해 봅니다.

## PyQGIS 연결

PyQGIS 수업에서는 다음 import를 가장 자주 보게 됩니다.

```python
from qgis.core import QgsProject, QgsVectorLayer
```

