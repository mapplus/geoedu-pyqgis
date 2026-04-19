# 05. 지오메트리와 좌표계

## 학습 목표

- PyQGIS에서 점, 선, 면 지오메트리를 만들고 다룰 수 있다.
- 중심점, 버퍼, 면적, 길이 같은 기본 연산을 이해한다.
- 좌표계 변환의 기본 흐름을 익힌다.

## 지오메트리 생성

```python
from qgis.core import QgsGeometry, QgsPointXY

point_geom = QgsGeometry.fromPointXY(QgsPointXY(10, 10))
line_geom = QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(5, 5)])
polygon_geom = QgsGeometry.fromPolygonXY([[QgsPointXY(0, 0), QgsPointXY(4, 0), QgsPointXY(4, 4), QgsPointXY(0, 0)]])
```

## WKT로 생성

```python
wkt_geom = QgsGeometry.fromWkt("POINT(127.0 37.5)")
print(wkt_geom.asWkt())
```

## 기본 연산

```python
buffer_geom = point_geom.buffer(1000, 16)

print(line_geom.length())
print(buffer_geom.area())
print(point_geom.distance(line_geom))
```

## 피처 지오메트리 다루기

```python
layer = iface.activeLayer()

for feature in layer.getFeatures():
    geom = feature.geometry()
    print(feature.id(), geom.centroid().asPoint())
```

## 좌표계 확인

```python
layer = iface.activeLayer()
print(layer.crs().authid())
```

## 좌표계 변환

```python
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsPointXY,
    QgsProject,
)

source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
target_crs = QgsCoordinateReferenceSystem("EPSG:5174")
xform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())

pt = xform.transform(QgsPointXY(127.0, 37.5))
print(pt)
```

## 같이 해보기

1. 점 지오메트리 하나를 만들어 봅니다.
2. 버퍼를 만들고 면적을 출력해 봅니다.
3. 활성 레이어의 좌표계를 확인해 봅니다.

## 꼭 짚고 갈 것

- 좌표가 같아 보여도 좌표계가 다르면 의미가 달라집니다.
- 거리와 면적 계산은 좌표계 영향을 크게 받습니다.
- 벡터 분석의 중심은 결국 `QgsGeometry`입니다.

