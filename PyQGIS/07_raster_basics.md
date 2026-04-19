# 07. 래스터 기초

## 학습 목표

- 래스터 레이어를 불러오고 유효성을 확인할 수 있다.
- 특정 위치의 래스터 값을 조회할 수 있다.
- 벡터와 래스터를 함께 쓰는 기본 흐름을 이해한다.

## 래스터 레이어 불러오기

```python
from qgis.core import QgsProject, QgsRasterLayer

raster_path = "C:/OSGeo_Edu/data/seoul_raster/dem30.tif"
rlayer = QgsRasterLayer(raster_path, "dem30")

print(rlayer.isValid())

if rlayer.isValid():
    QgsProject.instance().addMapLayer(rlayer)
```

## 특정 좌표 값 조회

```python
from qgis.core import QgsPointXY, QgsRaster

point_location = QgsPointXY(198326.53051, 447706.97545)
result = rlayer.dataProvider().identify(point_location, QgsRaster.IdentifyFormatValue).results()

print(result)
print(result[1])
```

## 피처 위치에서 래스터 값 읽기

```python
vector_layer = iface.activeLayer()

for feature in vector_layer.getFeatures():
    point = feature.geometry().asPoint()
    sample = rlayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()
    print(feature.id(), sample.get(1))
```

## 같이 해보기

1. 래스터 레이어 하나를 추가해 봅니다.
2. 지정한 좌표에서 밴드 1 값을 읽어 봅니다.
3. 포인트 레이어를 선택해 각 포인트 위치의 래스터 값을 출력해 봅니다.

## 꼭 짚고 갈 것

- 래스터 값 조회는 좌표계가 맞아야 제대로 동작합니다.
- `identify()` 결과는 밴드 번호를 key로 가지는 딕셔너리입니다.
- 점 레이어와 래스터를 조합하면 다양한 샘플링 작업을 만들 수 있습니다.

