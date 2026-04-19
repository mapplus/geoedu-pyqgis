# 08. 저장과 내보내기

## 학습 목표

- 결과 레이어를 파일로 저장할 수 있다.
- Shapefile, GeoPackage, GeoJSON 차이를 이해한다.
- 출력 경로와 좌표계를 확인하는 습관을 익힌다.

## 벡터 레이어 저장

최근 QGIS에서는 `QgsVectorFileWriter.writeAsVectorFormatV3()` 사용이 일반적입니다.

```python
from qgis.core import QgsCoordinateTransformContext, QgsProject, QgsVectorFileWriter

layer = iface.activeLayer()
output_path = "C:/OSGeo_Edu/data/output/result.geojson"

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GeoJSON"
options.fileEncoding = "UTF-8"

error, message, new_path, new_layer = QgsVectorFileWriter.writeAsVectorFormatV3(
    layer,
    output_path,
    QgsProject.instance().transformContext(),
    options,
)

print(error, message, new_path)
```

## 메모리 레이어 저장

```python
layer = iface.activeLayer()
output_path = "C:/OSGeo_Edu/data/output/memory_result.gpkg"

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.layerName = "memory_result"

error, message, new_path, new_layer = QgsVectorFileWriter.writeAsVectorFormatV3(
    layer,
    output_path,
    QgsProject.instance().transformContext(),
    options,
)

print(error, message)
```

## 형식 선택 기준

- Shapefile: 호환성은 좋지만 제약이 많습니다.
- GeoPackage: 현재 실습과 저장 포맷으로 가장 추천됩니다.
- GeoJSON: 웹/텍스트 친화적이고 가볍게 공유하기 좋습니다.

## 같이 해보기

1. 활성 레이어를 GeoJSON으로 저장해 봅니다.
2. 메모리 레이어를 GeoPackage로 저장해 봅니다.
3. 저장 후 다시 불러와 프로젝트에 추가해 봅니다.

## 꼭 짚고 갈 것

- 출력 경로가 실제로 존재하는지 먼저 확인합니다.
- 좌표계와 인코딩을 눈으로 확인합니다.
- 입문 과정에서는 기본 저장 포맷으로 GeoPackage를 우선 추천합니다.

