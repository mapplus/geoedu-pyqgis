# 10. 선택 심화: 공간 인덱스

## 학습 목표

- 공간 인덱스가 왜 필요한지 이해한다.
- 많은 피처를 비교할 때 속도를 개선하는 기본 개념을 익힌다.
- 심화 과정으로 넘어가기 전에 성능 관점의 첫 감을 잡는다.

## 왜 필요한가

모든 피처를 모든 피처와 직접 비교하면 매우 느려질 수 있습니다.  
공간 인덱스는 먼저 후보를 빠르게 줄인 뒤, 실제 교차 여부를 다시 검사하는 방식으로 성능을 개선합니다.

## 기본 예제

```python
from qgis.core import QgsFeatureRequest, QgsSpatialIndex, QgsVectorLayer

admin_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/admin_sgg.shp", "admin_sgg", "ogr")
store_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/stores.shp", "stores", "ogr")

spatial_index = QgsSpatialIndex(store_layer.getFeatures())

feature = next(admin_layer.getFeatures(QgsFeatureRequest().setFilterFid(18)))
admin_geom = feature.geometry()

candidate_fids = spatial_index.intersects(admin_geom.boundingBox())
print(candidate_fids)
```

## 실제 교차 검사

```python
count = 0

for fid in candidate_fids:
    store_feature = next(store_layer.getFeatures(QgsFeatureRequest().setFilterFid(fid)))
    if admin_geom.intersects(store_feature.geometry()):
        count += 1

print(count)
```

## Prepared geometry

교차 검사를 반복할 때는 prepared geometry를 함께 쓰면 더 효율적일 수 있습니다.

```python
engine = admin_geom.createGeometryEngine(admin_geom.constGet())
engine.prepareGeometry()
```

## 같이 해보기

1. 공간 인덱스를 만든 뒤 후보 FID 개수를 확인해 봅니다.
2. 실제 교차 개수와 후보 개수를 비교해 봅니다.
3. 왜 bounding box 후보와 실제 교차 결과가 다를 수 있는지 설명해 봅니다.

## 운영 메모

이 문서는 선택 심화입니다.  
입문 과정에서는 개념 소개 정도로 다루고, 실습 중심은 `프로젝트/레이어/피처/지오메트리/편집/저장`에 두는 편이 좋습니다.

