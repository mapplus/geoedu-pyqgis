# Learning PyQGIS
QGIS의 파이썬 콘솔에서 단계별로 실행 확인

# 1. 모듈 불러오기
```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.utils import *

from glob import glob
from os import path
```

## 모던 스타일
```python
from PyQt5.QtCore import (Qt,
                         QCoreApplication,
                         QVariant)
from qgis.core import (Qgis,
                       QgsMessageLog,
                       QgsExpression,
                       QgsFeature)
from qgis.utils import iface
from datetime import datetime
```

# 2. QGIS 버전 확인
## QGIS의 Major 버전 변경시 PyQGIS API 변경점 확인 필수

```python
print(Qgis.QGIS_VERSION_INT)

if Qgis.QGIS_VERSION_INT >= 30403:
    print("QGIS 3.4 uses python v3")
else:
    print("QGIS version is less than 3.4.")
```

# 3. 파일 정보 확인
## os.path
  - http://docs.python.org/3/library/os.path.html 사이트 확인

```python
file = "C:/OSGeo_Edu/data/seoul/admin_emd.shp"
(head, tail) = path.split(file)
# head : path
# tail : filename with ext
print(head)
print(tail)

(name, ext) = path.splitext(tail)
# name : file name
# ext : file format
print(name)
print(ext)
```

## Qt QFileInfo
  - http://qt-project.org/doc/qt-5/qfileinfo.html

```python
file_info = QFileInfo(file)
if file_info.exists():
    layer_name = file_info.completeBaseName()
    print(layer_name)
else:
    print("file not exist")
```

# 4. QGIS 벡터 파일 인코딩 정보
## Shapefile 등 벡터 파일의 기본 인코딩 확인

```python
# system default
settings = QSettings()  # 또는 QgsSettings
encode = settings.value("/UI/encoding")
print(encode)

# utf-8
settings.setValue("/UI/encoding", "UTF-8")
encode = settings.value("/UI/encoding")
print(encode)

# for korean
# CP949, ms949, windows-949, korean, EUC-KR
settings.setValue("/UI/encoding", "EUC-KR")
encode = settings.value("/UI/encoding")
print(encode)
```

# 5. 벡터 레이어 불러오기
## 5.1 Shapefile 레이어를 불러와서 지도에 추가하기

```python
# https://api.qgis.org/api/classQgsVectorLayer.html
vlayer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/admin_emd.shp", "admin_emd", "ogr")
QgsProject.instance().addMapLayer(vlayer)

# https://api.qgis.org/api/classQgisInterface.html
vlayer = iface.addVectorLayer("C:/OSGeo_Edu/data/seoul/admin_emd.shp", "admin_emd_2", "ogr")
```

## 5.2 iface(QgisInterface) 인터페이스와 캔버스 색상 변경
```python
canvas = iface.mapCanvas()

canvas.setCanvasColor(Qt.red)
canvas.refresh()

canvas.setCanvasColor(Qt.white)
canvas.refresh()

# active layer , 현재 선택된 레이어를 받아오는 방법 2가지
layer = iface.activeLayer()
print(layer.name())

layer = canvas.currentLayer()
print(layer.name())
```

## 5.3 PostGIS 레이어 불러오기
```python
uri = QgsDataSourceUri()

# set hostname, port, database, username and password
uri.setConnection("localhost", "5432", "database", "username", "password")

# set database schema, table name, geometry column and optionaly subset (WHERE clause)
uri.setDataSource("public", "roads", "the_geom", "cityid = 2643")

postgis_layer = QgsVectorLayer(uri.uri(), "roads", "postgres")
QgsProject.instance().addMapLayer(postgis_layer)
```

## 5.4 기타 벡터 레이어 불러오기
GeoServer WFS 레이어 불러오기
```python
uri = "http://localhost:8080/geoserver/wfs?srsname=EPSG:4326&typename=topp:states&version=1.0.0&request=GetFeature&service=WFS"

wfs_layer = QgsVectorLayer(uri, "WFS Layer", "WFS")
QgsProject.instance().addMapLayer(wfs_layer)
```

# 6. 래스터 레이어 불러오기
## 6.1 GeoTIFF 파일 불러오기
```python
rlayer = QgsRasterLayer("C:/OSGeo_Edu/data/seoul_raster/dem30.tif", "dem30")
QgsProject.instance().addMapLayer(rlayer)

# or

rlayer = iface.addRasterLayer("C:/OSGeo_Edu/data/seoul_raster/dem30.tif", "dem30_2")
```

## 6.2 래스터 레이어의 특정 위치 값 조회하기
```python
point_location = QgsPointXY(198326.53051, 447706.97545)
identified = rlayer.dataProvider().identify(point_location, QgsRaster.IdentifyFormatValue).results()
value = float(identified[1])  # 1 based raster band index
print(value)
```

# 7. 벡터 레이어 다루기
## 7.1 레이어 목록 가져오기
```python
# only visible layers
for layer in iface.mapCanvas().layers():
    print(layer.name())

# all layers
allLayers = QgsProject.instance().mapLayers() # dict(key, value)로 모든 레이어 정보를 받음
for name,layer in allLayers.items():
    print(layer.name())
```

## 7.2 선택한 피쳐 목록 가져오기
Select 도구로 몇 개의 feature를 선택
```python
# admin_emd 선택
vlayer = iface.activeLayer()

features = vlayer.selectedFeatures()
count = vlayer.selectedFeatureCount()
print("selected features = " + str(count))

if count > 0:
    for feature in features:
        print(feature.id())
else:
    print("not selected")
```

## 7.3 레이어 필드 및 객체 속성 확인
```python
# select vector layers: 반드시 admin_emd 선택
vlayer = iface.activeLayer()
provider = vlayer.dataProvider()

# list fields
fields = provider.fields()
for field in fields:
    print(field.name())

# layer의 모든 feature ID와 중심점의 값, 속성값을 출력
features = vlayer.getFeatures()
for feature in features:
    geometry = feature.geometry()

    print("\nFeature ID = %d: " % feature.id(), geometry.centroid().asPoint())

    # show all attributes and their values
    for attr in feature.attributes():
        print(attr)
```

## 7.4 속성 및 공간 쿼리
### 7.4.1 fid query
```python
vlayer.removeSelection()
request = QgsFeatureRequest().setFilterFid(5)

# QgsFeatureIterator로 Feature를 받음, next() function returns the next item in an iterator.
feature = next(vlayer.getFeatures(request))
vlayer.select(feature.id())

print("Feature ID = %d: " % feature.id())
print(feature.id(), feature[4], feature["EMD_NM"])

# ZoomTo Feature Extent
iface.mapCanvas().setExtent(feature.geometry().boundingBox())
iface.mapCanvas().refresh()

### 7.4.2 QgsFeatureRequest Filter
# Filter options: NoFlags NoGeometry SubsetOfAttributes ExactIntersect
vlayer.removeSelection()

request = QgsFeatureRequest().setFilterFid(5)

# Geometry는 가져오지 않기
request.setFlags(QgsFeatureRequest.NoGeometry)

# 0, 1, 2 번째 속성만 가져오기
request.setSubsetOfAttributes([0, 1, 2])

feature = next(vlayer.getFeatures(request))
#setFlags : NoGeometry이기 때문에 geometry는 null로 return, 속성은 0, 1, 2번째만 가져오기 때문에 4번째 속성값은 None으로 return
print(feature.geometry(), feature[4])

### 7.4.3 QgsFeatureRequest rectangle filter
vlayer.removeSelection()

# rectangle 영역에 있는 Feature들의 Extent를 모두 하나로 합치기
unioned_geomery = QgsGeometry()
extent = QgsRectangle(194052.547, 447030.808, 197991.199,448635.444)
request = QgsFeatureRequest().setFilterRect(extent)

features = vlayer.getFeatures(request)
for feature in features:
    geometry = feature.geometry()
    if unioned_geomery.isEmpty() :
        unioned_geomery = geometry
    else:
        #combine : Returns a geometry representing all the points in this geometry and other
        unioned_geomery = unioned_geomery.combine(geometry)

    print("Feature ID = %d: " % feature.id(), geometry.centroid().asPoint())
    vlayer.select(feature.id())

map_extent = unioned_geomery.boundingBox()
iface.mapCanvas().setExtent(map_extent)
iface.mapCanvas().refresh()

vlayer.removeSelection()
```

## 7.5 스키마(필드) 다루기
### 7.5.1 필드 추가
```python
vlayer = iface.activeLayer()
provider = vlayer.dataProvider()

stringfield = QgsField("mytext", QVariant.String)
intfield = QgsField("myint", QVariant.Int)
doublefield = QgsField("mydouble", QVariant.Double)

caps = provider.capabilities()

# 1. add fields
if caps & QgsVectorDataProvider.AddAttributes:
    res = provider.addAttributes([stringfield, intfield, doublefield])
    vlayer.reload()
else:
    print("cannot add new fields")
```

### 7.5.2 필드 삭제
```python
# field 인덱스 찾기
print(provider.fieldNameIndex("mytext"))
print(provider.fieldNameIndex("myint"))
print(provider.fieldNameIndex("mydouble"))

if caps & QgsVectorDataProvider.DeleteAttributes:
    # 출력된 index를 적는다.. 10, 11, 12
    res = provider.deleteAttributes([10, 11, 12])
    vlayer.reload()
else:
    print("cannot delete fields")
```

# 8. Geometry 및 좌표체계 다루기
## 8.1 Geometry 생성 및 다루기
```python
point_geometry = QgsGeometry.fromPointXY(QgsPointXY(10,10))
line_geometry = QgsGeometry.fromPolylineXY([QgsPointXY(4,4), QgsPointXY(7,7)])
polygeon_geometry = QgsGeometry.fromPolygonXY([[QgsPointXY(1,1), QgsPointXY(2,2), QgsPointXY(2,1)]])

wkt_point = QgsGeometry.fromWkt("POINT(10 10)")
wkt_line = QgsGeometry.fromWkt("LINESTRING(4 4, 7 7)")
wkt_polygon = QgsGeometry.fromWkt("POLYGON((1 1, 2 2, 2 1, 1 1))")

point_geometry.asPoint()        # QgsPoint
line_geometry.asPolyline()      # QgsPolyline
polygeon_geometry.asPolygon()   # QgsPolygon

# area(), length(), distance()

print(line_geometry.distance(point_geometry))
printpolygeon_geometry.area())
```

## 8.2 좌표체계 변환
```python
source_crs = QgsCoordinateReferenceSystem('EPSG:4326')   # WGS84
target_crs = QgsCoordinateReferenceSystem('EPSG:5174')   # Korean 1985 Modified Centeral belt

# QgsCoordinateTransform(source: QgsCoordinateReferenceSystem, destination: QgsCoordinateReferenceSystem, sourceDatumTransformId: int, destinationDatumTransformId: int)
xform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())

# forward transformation: src -> dest
pt1 = xform.transform(QgsPointXY(127.0028902777778, 38))
print("transformed point:", pt1)

pt1 = xform.transform(QgsPointXY(127, 38))
print("transformed point:", pt1)
```

# 9. 메모리 레이어 다루기
## 9.1 메모리 레이어 1
```python
# create memory layer
tlayer = QgsVectorLayer("Polygon?crs=epsg:5174&index=yes", "Point_Buffered", "memory")
provider = tlayer.dataProvider()

# start editing mode
tlayer.startEditing()

# add fields
provider.addAttributes( [QgsField("dx", QVariant.Double), QgsField("dy", QVariant.Double) ] )

# create and add a feature
centroid = QgsPointXY(198326.53051, 447706.97545)
buffered_geom = QgsGeometry.fromPointXY(centroid).buffer(5000, 8)  # segments = 8

feature = QgsFeature(provider.fields())
feature.setGeometry(buffered_geom)
feature.setAttribute(0, centroid.x())
feature.setAttribute(1, centroid.y())

provider.addFeatures([feature])

# commit changes
tlayer.commitChanges()

# udpate extent
tlayer.updateExtents()

# add layer
QgsProject.instance().addMapLayer(tlayer)
iface.mapCanvas().setExtent(tlayer.extent())
iface.mapCanvas().refresh()
```

## 9.2 메모리 레이어 2
```python
# create memory layer
crs = QgsCoordinateReferenceSystem('EPSG:5174')   # Korean 1985 Modified Centeral belt
tlayer = QgsVectorLayer("Point", "circle_points", "memory") #좌표계 정의 안되어 있기 때문에 좌표계 설정 창 표출
tlayer.setCrs(crs)

provider = tlayer.dataProvider()

# provider.name() << memory 확인가능

# start editing mode
tlayer.startEditing()

# add fields
# QgsField("COUNT", QVariant.Double, "real", 24, 16)
provider.addAttributes([
                QgsField("id",  QVariant.Int),
                QgsField("name", QVariant.String),
                QgsField("angle", QVariant.Double),
                QgsField("dx", QVariant.Double),
                QgsField("dy", QVariant.Double)])

fields = provider.fields()

# add a feature
features = []

# create circle
import math
sides = 32
radius = 5000.0 # 반지름 5km
centroid = QgsPointXY(198326.53051, 447706.97545)

# 첫번째 Feature는 중심점 Feature 생성
feature = QgsFeature(fields)

feature.setGeometry(QgsGeometry.fromPointXY(centroid))
feature.setAttribute(0, 0)
feature.setAttribute(1, "Name_" + str(0))
feature.setAttribute(2, 0)
feature.setAttribute(3, centroid.x())
feature.setAttribute(4, centroid.y())

# 리스트에 추가
features.append(feature)

for index in range(sides):
    radians = (float(index) / float(sides)) * (math.pi * 2.0)
    degree = radians * (180.0 / math.pi);
    dx = centroid.x() + math.cos(radians) * radius
    dy = centroid.y() + math.sin(radians) * radius
    print(degree, radius, dx, dy)

    feature = QgsFeature(fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(dx, dy)))
    feature.setAttribute(0, int(index + 1))
    feature.setAttribute(1, "Name_" + str(index + 1))
    feature.setAttribute(2, degree)
    feature.setAttribute(3, dx)
    feature.setAttribute(4, dy)

    features.append(feature)

# features 리스트의 feature를 추가
provider.addFeatures(features)

# commit changes
tlayer.commitChanges()

# udpate extent
tlayer.updateExtents()

# add layer
QgsProject.instance().addMapLayer(tlayer)
iface.mapCanvas().setExtent(tlayer.extent())
iface.mapCanvas().refresh()

# show some stats
print("fields:", len(provider.fields()))
print("features:", provider.featureCount())
extent = provider.extent()
print("extent: ", extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum())

minimum = provider.minimumValue(2)  # 2 = field index
maximum = provider.maximumValue(2)  # 2 = field index
print(minimum, maximum)

# write shapefile
output_file = 'C:/OSGeo_Edu/data/seoul/memory_circle_points.shp'
error = QgsVectorFileWriter.writeAsVectorFormat(tlayer, output_file, "EUC-KR", crs, "ESRI Shapefile")
if error[0] == QgsVectorFileWriter.NoError:
    print("shapefile exported!")

# write GeoJSON
output_file = 'C:/OSGeo_Edu/data/seoul/circle_points.json'
error = QgsVectorFileWriter.writeAsVectorFormat(tlayer, output_file, "UTF-8", crs, "GeoJSON")
if error[0] == QgsVectorFileWriter.NoError:
    print("geojson exported!")
```

# 10. 벡터 레이어 계산하기
## 10.1 계산 1
```python
vlayer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/stores.shp", "stores", "ogr")
provider = vlayer.dataProvider()

xfield = provider.fieldNameIndex("xc")
yfield = provider.fieldNameIndex("yc")
print(xfield, yfield)

if xfield == -1:
    # add field
    xc = QgsField("xc", QVariant.Double)
    res = provider.addAttributes([xc])

if yfield == -1:
    # add field
    yc = QgsField("yc", QVariant.Double)
    res = provider.addAttributes([yc])

# reload attributes
xfield = provider.fieldNameIndex("xc")
yfield = provider.fieldNameIndex("yc")
print(xfield, yfield)

# Loop through each vector feature
features = vlayer.getFeatures()
for feature in features:
    geometry = feature.geometry()

    # centroid
    centroid = geometry.centroid().asPoint()

    fid = int(feature.id())
    vlayer.startEditing()
    # changeAttributeValue(feature id, index of field to be changed, new attribute value)
    vlayer.changeAttributeValue(fid, xfield, centroid.x())
    vlayer.changeAttributeValue(fid, yfield, centroid.y())
    vlayer.commitChanges()

# 결과 Map에 로딩
QgsProject.instance().addMapLayer(vlayer)
```

## 10.2 계산 2
```python
vlayer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/stores.shp", "stores", "ogr")
provider = vlayer.dataProvider()

rlayer = QgsRasterLayer("C:/OSGeo_Edu/data/seoul_raster/dem30.tif", "dem30")

value_field = "elev" #dem 값이 입력될 필드 추가
field_index = provider.fieldNameIndex(value_field)

if field_index == -1:
    # add field
    res = provider.addAttributes([QgsField(value_field, QVariant.Double)])

    # reload attributes
    field_index = provider.fieldNameIndex(value_field)

# Loop through each vector feature
features = vlayer.getFeatures()
for feature in features:
    geom = feature.geometry()

    # get the raster value of the cell under the vector point
    rasterSample = rlayer.dataProvider().identify(geom.asPoint(), QgsRaster.IdentifyFormatValue).results()

    # the key is the raster band, and the value is the cell's raster value
    elevation = float(rasterSample[1])  # band index

    # changeAttributeValue(feature id, index of field to be changed, new attribute value)
    vlayer.startEditing()
    vlayer.changeAttributeValue(int(feature.id()), field_index, elevation)
    vlayer.commitChanges()

# 결과 Map에 로딩
QgsProject.instance().addMapLayer(vlayer)
```

# 11. 공간 인덱스 다루기
## 11.1 QgsSpatialIndex
```python
# admin_sgg 레이어의 fid가 18번인 피처와 교차하는 stores 레이어의 피처 수는?
admin_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/admin_sgg.shp", "admin_sgg", "ogr")
store_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/stores.shp", "stores", "ogr")
spatial_index = QgsSpatialIndex(store_layer.getFeatures())

request = QgsFeatureRequest().setFilterFid(18)  # fid
feature = next(admin_layer.getFeatures(request))
admin_geom = feature.geometry()

intersection_count = 0
stores_fids = spatial_index.intersects(admin_geom.boundingBox())
for fid in stores_fids:
    request = QgsFeatureRequest().setFilterFid(int(fid))
    store_feature = next(store_layer.getFeatures(request))
    store_geometry = store_feature.geometry()
    if admin_geom.intersects(store_geometry):
        intersection_count += 1
        print("Feature ID = %d: " % store_feature.id(), store_feature.geometry().centroid().asPoint())

print(intersection_count)
```

## 11.2 QgsSpatialIndex + Prepared Geometry
```python
# admin_sgg 레이어의 fid가 18번인 피처와 교차하는 stores 레이어의 피처 수는?
admin_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/admin_sgg.shp", "admin_sgg", "ogr")
store_layer = QgsVectorLayer("C:/OSGeo_Edu/data/seoul/stores.shp", "stores", "ogr")
spatial_index = QgsSpatialIndex(store_layer.getFeatures())

request = QgsFeatureRequest().setFilterFid(18)  # fid
feature = next(admin_layer.getFeatures(request))
admin_geom = feature.geometry()
admin_prepared = QgsGeometry.createGeometryEngine(admin_geom.constGet())
admin_prepared.prepareGeometry()

intersection_count = 0
stores_fids = spatial_index.intersects(admin_geom.boundingBox())
for fid in stores_fids:
    request = QgsFeatureRequest().setFilterFid(int(fid))
    store_feature = next(store_layer.getFeatures(request))
    store_geometry = store_feature.geometry()
    if admin_prepared.intersects(store_geometry.constGet()):
        intersection_count += 1
        print("Feature ID = %d: " % store_feature.id(), store_geometry.centroid().asPoint())

print(intersection_count)
```

# 참고사이트
  - PyQGIS
    - https://qgis.org/pyqgis/3.0/
    - https://qgis.org/api/modules.html

  - PyQT
    - https://doc.qt.io/qtforpython-5/api.html
    - https://wikidocs.net/book/2944

  - GDAL/OGR(고급 사용자 추천)
    - https://gdal.org/api/python.html
