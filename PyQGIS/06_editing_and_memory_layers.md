# 06. 편집과 메모리 레이어

## 학습 목표

- 벡터 레이어 편집 기본 흐름을 익힌다.
- 필드 추가와 속성 변경을 할 수 있다.
- 메모리 레이어를 생성해 결과를 시각화할 수 있다.

## 필드 추가

```python
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField

layer = iface.activeLayer()
provider = layer.dataProvider()

layer.startEditing()
provider.addAttributes([
    QgsField("my_text", QVariant.String),
    QgsField("my_value", QVariant.Double),
])
layer.updateFields()
layer.commitChanges()
```

## 속성값 수정

```python
layer = iface.activeLayer()
field_index = layer.fields().indexFromName("my_value")

layer.startEditing()

for feature in layer.getFeatures():
    layer.changeAttributeValue(feature.id(), field_index, 100.0)

layer.commitChanges()
```

## 메모리 레이어 생성

```python
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsField, QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer

memory_layer = QgsVectorLayer("Point?crs=EPSG:5174", "sample_points", "memory")
provider = memory_layer.dataProvider()

provider.addAttributes([
    QgsField("name", QVariant.String),
    QgsField("value", QVariant.Double),
])
memory_layer.updateFields()

feature = QgsFeature(memory_layer.fields())
feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(198326.53, 447706.98)))
feature.setAttributes(["point_1", 1.0])

provider.addFeatures([feature])
memory_layer.updateExtents()

QgsProject.instance().addMapLayer(memory_layer)
```

## 버퍼 메모리 레이어 예제

```python
center = QgsPointXY(198326.53, 447706.98)
buffer_geom = QgsGeometry.fromPointXY(center).buffer(5000, 16)

buffer_layer = QgsVectorLayer("Polygon?crs=EPSG:5174", "buffer_result", "memory")
buffer_provider = buffer_layer.dataProvider()
buffer_provider.addAttributes([QgsField("name", QVariant.String)])
buffer_layer.updateFields()

feature = QgsFeature(buffer_layer.fields())
feature.setGeometry(buffer_geom)
feature.setAttributes(["buffer_5km"])

buffer_provider.addFeatures([feature])
buffer_layer.updateExtents()
QgsProject.instance().addMapLayer(buffer_layer)
```

## 같이 해보기

1. 활성 레이어에 새 필드를 추가해 봅니다.
2. 새 필드에 같은 값을 넣어 봅니다.
3. 점 메모리 레이어를 하나 만들어 프로젝트에 추가해 봅니다.

## 꼭 짚고 갈 것

- 편집 전 `startEditing()`, 완료 후 `commitChanges()` 흐름을 익혀야 합니다.
- 필드를 추가한 뒤에는 `updateFields()`가 필요합니다.
- 결과 레이어를 바로 확인하려면 메모리 레이어가 매우 유용합니다.

