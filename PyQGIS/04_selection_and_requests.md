# 04. 선택과 요청

## 학습 목표

- 선택된 피처를 읽을 수 있다.
- 필요한 피처만 조회하는 `QgsFeatureRequest`를 사용할 수 있다.
- 속성 기반, ID 기반, 영역 기반 조회 흐름을 이해한다.

## 선택된 피처 확인

```python
from qgis.utils import iface

layer = iface.activeLayer()
features = layer.selectedFeatures()

print(layer.selectedFeatureCount())

for feature in features:
    print(feature.id())
```

## FID 기반 조회

```python
from qgis.core import QgsFeatureRequest

request = QgsFeatureRequest().setFilterFid(5)
feature = next(layer.getFeatures(request))

print(feature.id())
print(feature.attributes())
```

## 일부 속성만 가져오기

```python
request = QgsFeatureRequest()
request.setSubsetOfAttributes([0, 1, 2], layer.fields())
request.setFlags(QgsFeatureRequest.NoGeometry)

feature = next(layer.getFeatures(request))
print(feature.geometry())
print(feature.attributes())
```

## 영역으로 조회

```python
from qgis.core import QgsFeatureRequest, QgsRectangle

extent = QgsRectangle(194052.547, 447030.808, 197991.199, 448635.444)
request = QgsFeatureRequest().setFilterRect(extent)

for feature in layer.getFeatures(request):
    print(feature.id())
```

## 선택 영역으로 확대

```python
feature = next(layer.getFeatures(QgsFeatureRequest().setFilterFid(5)))
iface.mapCanvas().setExtent(feature.geometry().boundingBox())
iface.mapCanvas().refresh()
```

## 같이 해보기

1. 선택된 피처 수를 출력해 봅니다.
2. 특정 FID의 속성값을 확인해 봅니다.
3. 사각형 영역 안에 있는 피처 ID를 출력해 봅니다.

## 꼭 짚고 갈 것

- 전체 피처를 다 읽지 않고 필요한 것만 읽는 습관이 중요합니다.
- `NoGeometry`, `setSubsetOfAttributes()`는 성능 최적화의 첫걸음입니다.
- 조회와 선택은 비슷해 보여도 목적이 다릅니다.

