# 03. 벡터 레이어와 속성

## 학습 목표

- 벡터 레이어의 필드와 피처를 읽을 수 있다.
- 속성값과 지오메트리를 함께 확인하는 흐름을 익힌다.
- `dataProvider()`와 `getFeatures()`의 역할을 이해한다.

## 활성 벡터 레이어 가져오기

```python
from qgis.utils import iface

layer = iface.activeLayer()
print(layer)
```

활성 레이어가 벡터 레이어인지 먼저 확인하는 습관이 필요합니다.

```python
from qgis.core import QgsMapLayerType

layer = iface.activeLayer()

if layer is None or layer.type() != QgsMapLayerType.VectorLayer:
    print("벡터 레이어를 선택해 주세요.")
else:
    print(layer.name())
```

## 필드 목록 확인

```python
provider = layer.dataProvider()
fields = provider.fields()

for field in fields:
    print(field.name(), field.typeName())
```

## 피처 순회

```python
for feature in layer.getFeatures():
    print(feature.id())
```

## 속성값 확인

```python
for feature in layer.getFeatures():
    print(feature.id(), feature.attributes())
```

특정 필드 이름으로도 접근할 수 있습니다.

```python
for feature in layer.getFeatures():
    print(feature["EMD_NM"])
```

## 지오메트리와 함께 보기

```python
for feature in layer.getFeatures():
    geometry = feature.geometry()
    print(feature.id(), geometry.centroid().asPoint())
```

## 피처 개수 확인

```python
print(layer.featureCount())
```

## 같이 해보기

1. 활성 레이어의 필드명을 모두 출력해 봅니다.
2. 첫 5개 피처의 ID와 특정 속성값을 출력해 봅니다.
3. 각 피처의 중심점 좌표를 출력해 봅니다.

## 꼭 짚고 갈 것

- `dataProvider()`는 데이터 소스와 연결되는 객체입니다.
- `getFeatures()`는 반복 가능한 피처 집합을 반환합니다.
- 필드명 접근은 읽기 쉽지만, 필드명이 바뀌면 코드도 수정해야 합니다.

