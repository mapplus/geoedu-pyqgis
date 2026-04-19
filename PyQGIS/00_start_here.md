# 00. 시작하기

## 같이 먼저 해볼 것

PyQGIS는 Python 문법을 그대로 사용하지만, 실제로는 QGIS 객체를 꺼내서 확인하고 조작하는 흐름으로 익히는 것이 중요합니다.  
먼저 아래 코드를 같이 실행해 보겠습니다.

```python
from qgis.utils import iface
from qgis.core import QgsProject

print(iface)
print(QgsProject.instance())
print(len(QgsProject.instance().mapLayers()))
```

## QGIS Python Console에서 먼저 익힐 것

- 현재 프로젝트에 접근하는 방법
- 현재 활성 레이어를 확인하는 방법
- 실행 결과가 지도 화면과 연결되는 방식

```python
canvas = iface.mapCanvas()
layer = iface.activeLayer()

print(canvas)
print(layer)
```

## 꼭 짚고 갈 것

- `iface`는 QGIS 화면과 연결된 인터페이스 객체입니다.
- 활성 레이어가 없는 상태에서는 `iface.activeLayer()`가 `None`일 수 있습니다.
- 콘솔에서 보이는 결과와 지도 화면의 변화는 서로 연결됩니다.

## 같이 해보기

1. 현재 프로젝트 레이어 개수를 출력해 봅니다.
2. 활성 레이어 이름을 출력해 봅니다.
3. 활성 레이어가 없을 때 메시지를 출력해 봅니다.

```python
layer = iface.activeLayer()

if layer is None:
    print("현재 활성 레이어가 없습니다.")
else:
    print(layer.name())
```

