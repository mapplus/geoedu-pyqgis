# PyQGIS Practice Guide for QGIS

이 폴더는 `QGIS Python Console`에서 진행하는 PyQGIS 기초 실습 자료입니다.  
Python 기초를 익힌 뒤, QGIS 객체를 직접 다루는 흐름으로 넘어가기 위한 실습 문서입니다.

## 교육 범위

- 1단계: QGIS Python Console 적응
- 2단계: 프로젝트와 레이어 다루기
- 3단계: 피처, 속성, 지오메트리 다루기
- 4단계: 편집, 메모리 레이어, 결과 저장
- 이후 확장: 스크립팅 자동화, Processing, 플러그인 개발

## 실습 환경

- QGIS 3.44.x 버전과 내장 Python 3.12
- QGIS Python Console 사용
- 일부 예제는 `.py` 스크립트 파일로 저장해 다시 실행

## 교육 목표

- PyQGIS에서 자주 사용하는 핵심 객체를 이해한다.
- `iface`, `QgsProject`, `QgsVectorLayer`, `QgsFeature`, `QgsGeometry` 흐름을 익힌다.
- 레이어를 불러오고, 피처와 속성을 읽고, 간단한 편집과 저장을 수행할 수 있다.
- 이후 스크립팅과 플러그인 개발로 자연스럽게 연결할 준비를 마친다.

## 먼저 같이 시작해 보기

PyQGIS는 Python 문법 위에서 동작하지만, 실제로는 "QGIS 객체를 가져와서 확인하고, 처리하고, 결과를 반영하는 흐름"으로 이해하는 것이 더 중요합니다.  
그래서 본격적인 예제로 들어가기 전에 아래 코드를 먼저 같이 실행해 보겠습니다.

```python
from qgis.core import Qgis, QgsProject

print(Qgis.QGIS_VERSION)
print(QgsProject.instance())
print(QgsProject.instance().mapLayers())
```

먼저 확인할 포인트:

- PyQGIS는 QGIS가 제공하는 Python API입니다.
- `QgsProject.instance()`는 현재 열려 있는 프로젝트를 가리킵니다.
- QGIS Python Console에서는 `iface`를 통해 현재 화면과 상호작용할 수 있습니다.

## 실습 목차

| 순서 | 주제 | 파일 | 실습 초점 |
| --- | --- | --- | --- |
| 0 | 시작하기 | [00_start_here.md](./00_start_here.md) | 콘솔, `iface`, 프로젝트 객체 |
| 1 | 모듈과 환경 확인 | [01_imports_and_environment.md](./01_imports_and_environment.md) | import, 버전 확인, 주요 객체 |
| 2 | 프로젝트와 레이어 | [02_project_and_layers.md](./02_project_and_layers.md) | 레이어 추가, 활성 레이어, 레이어 목록 |
| 3 | 벡터 레이어와 속성 | [03_vector_layers_and_attributes.md](./03_vector_layers_and_attributes.md) | fields, features, attributes |
| 4 | 선택과 요청 | [04_selection_and_requests.md](./04_selection_and_requests.md) | selected features, `QgsFeatureRequest` |
| 5 | 지오메트리와 좌표계 | [05_geometry_and_crs.md](./05_geometry_and_crs.md) | geometry, centroid, buffer, 좌표계 변환 |
| 6 | 편집과 메모리 레이어 | [06_editing_and_memory_layers.md](./06_editing_and_memory_layers.md) | startEditing, field 추가, memory layer |
| 7 | 래스터 기초 | [07_raster_basics.md](./07_raster_basics.md) | raster layer, sample, identify |
| 8 | 저장과 내보내기 | [08_save_and_export.md](./08_save_and_export.md) | Shapefile, GeoPackage, GeoJSON |
| 9 | 자동화 예제 | [09_automation_examples.md](./09_automation_examples.md) | 기존 예제를 작은 스크립트로 확장 |
| 10 | 선택 심화 | [10_spatial_index.md](./10_spatial_index.md) | spatial index, 성능 개선 기초 |

## PyQGIS에서 꼭 잡아야 하는 핵심 개념

- `iface`: 현재 QGIS 인터페이스에 접근하는 창구
- `QgsProject`: 현재 프로젝트와 레이어 목록 관리
- `QgsMapLayer`: 레이어의 공통 부모 개념
- `QgsVectorLayer`, `QgsRasterLayer`: 실제 데이터 레이어
- `QgsFeature`: 레이어 안의 개별 객체
- `QgsGeometry`: 점, 선, 면과 같은 공간 정보
- `QgsFeatureRequest`: 필요한 피처만 효율적으로 조회하는 도구
- `dataProvider()`: 데이터 소스와 직접 연결되는 공급자
- 편집 세션: 값 변경 전후를 제어하는 기본 흐름

## Python 기초와 연결되는 지점

- 변수 -> 레이어, 피처, 지오메트리 객체를 담는 그릇
- 조건문 -> 레이어 유효성 검사, 선택 여부 확인
- 반복문 -> 피처 순회, 레이어 목록 순회
- 함수 -> 재사용 가능한 PyQGIS 도구 작성
- 딕셔너리/리스트 -> 필드명 목록, 속성값 정리
- 파일 입출력 -> 결과 저장, 로그 저장, 레이어 내보내기
- 예외 처리 -> 레이어 누락, 경로 오류, 필드 없음 대응

## 실습 규칙

- 예제는 콘솔에서 한 줄씩 직접 입력합니다.
- 활성 레이어가 필요한 예제는 먼저 레이어 상태를 확인합니다.
- 좌표계와 파일 경로는 반드시 눈으로 다시 확인합니다.
- 결과가 보이지 않으면 캔버스 새로고침과 레이어 추가 여부를 먼저 확인합니다.
- 콘솔에서 검증한 코드는 필요한 경우 `.py` 파일로 옮겨 정리합니다.
