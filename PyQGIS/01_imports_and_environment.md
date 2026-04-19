# 01. 모듈과 환경 확인

## 학습 목표

- PyQGIS에서 자주 쓰는 import 패턴을 익힌다.
- 현재 QGIS 버전과 실행 환경을 확인할 수 있다.
- 어떤 객체를 어디서 가져오는지 구분한다.

## 필요한 모듈 가져오기

초급 과정에서는 `import *` 대신 필요한 객체만 가져오는 방식을 사용합니다.

```python
from qgis.core import Qgis, QgsProject, QgsVectorLayer, QgsRasterLayer
from qgis.utils import iface
```

## QGIS 버전 확인

```python
from qgis.core import Qgis

print(Qgis.QGIS_VERSION)
print(Qgis.QGIS_VERSION_INT)
```

## 현재 프로젝트 확인

```python
from qgis.core import QgsProject

project = QgsProject.instance()
print(project.fileName())
print(project.homePath())
```

## 화면과 연결된 객체 확인

```python
from qgis.utils import iface

print(iface.mainWindow())
print(iface.mapCanvas())
```

## 꼭 짚고 갈 것

- `qgis.core`에는 핵심 데이터 객체가 많습니다.
- `qgis.utils`의 `iface`는 현재 QGIS 화면과 연결됩니다.
- QGIS 버전이 바뀌면 일부 API 사용 방식이 달라질 수 있습니다.

## 같이 해보기

1. 현재 QGIS 버전을 출력해 봅니다.
2. 현재 프로젝트 경로를 확인해 봅니다.
3. `iface.mapCanvas()`를 출력해 봅니다.

