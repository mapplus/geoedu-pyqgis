# 02. 프로젝트와 레이어

## 학습 목표

- 프로젝트에 레이어를 추가하고 제거하는 흐름을 이해한다.
- 활성 레이어와 전체 레이어 목록을 다룰 수 있다.
- 벡터와 래스터 레이어를 구분할 수 있다.

## 벡터 레이어 불러오기

```python
from qgis.core import QgsProject, QgsVectorLayer

layer_path = "C:/OSGeo_Edu/data/seoul/admin_emd.shp"
layer = QgsVectorLayer(layer_path, "admin_emd", "ogr")

print(layer.isValid())

if layer.isValid():
    QgsProject.instance().addMapLayer(layer)
```

## iface로 레이어 추가하기

```python
from qgis.utils import iface

layer = iface.addVectorLayer("C:/OSGeo_Edu/data/seoul/admin_emd.shp", "admin_emd_2", "ogr")
print(layer)
```

## 래스터 레이어 불러오기

```python
from qgis.core import QgsProject, QgsRasterLayer

raster_path = "C:/OSGeo_Edu/data/seoul_raster/dem30.tif"
rlayer = QgsRasterLayer(raster_path, "dem30")

if rlayer.isValid():
    QgsProject.instance().addMapLayer(rlayer)
```

## 레이어 목록 확인

```python
from qgis.core import QgsProject

all_layers = QgsProject.instance().mapLayers()

for layer_id, layer in all_layers.items():
    print(layer_id, layer.name(), layer.type())
```

## 활성 레이어 확인

```python
from qgis.utils import iface

layer = iface.activeLayer()

if layer is None:
    print("활성 레이어가 없습니다.")
else:
    print(layer.name())
```

## 캔버스와 화면 갱신

```python
canvas = iface.mapCanvas()
canvas.refresh()
```

## 같이 해보기

1. 벡터 레이어 하나를 추가해 봅니다.
2. 현재 프로젝트의 모든 레이어 이름을 출력해 봅니다.
3. 활성 레이어 이름과 타입을 확인해 봅니다.

## 꼭 짚고 갈 것

- `isValid()`로 레이어 유효성을 먼저 확인합니다.
- 프로젝트에 추가해야 화면에 보입니다.
- `iface.activeLayer()`는 현재 선택된 레이어를 가리킵니다.

