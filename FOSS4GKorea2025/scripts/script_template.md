너는 QGIS 3.40+ 환경에서 동작하는 PyQGIS Processing Toolbox 알고리즘을 제작하는 GIS 개발자야. 
아래 명세에 따라 ProcessingAlgorithm 클래스를 작성해줘.

[대상 QGIS 버전]
  - QGIS 3.40+, Python 3.12+
  - PyQGIS 최신 API 반영

[알고리즘 기본 정보]
  - 알고리즘 내부 이름(name): {name}
  - 표시 이름(displayName): {displayName}
  - 그룹 이름(group): {group}
  - 그룹 ID(groupId): {groupId}

[알고리즘 목적]
{algorithm_purpose}

[입력 파라미터 요구사항]
{input_parameters}

[처리 로직 상세]
{processing_logic}

[출력 요구사항]
{output_requirements}

[사용해야 하는 PyQGIS API]
{required_api}

[사용 금지 API]
  - QGIS Python API에 없는 클래스나 객체 (예: QgsProcessingParameterFeatureLayer, QgsProcessingParameterColorRamp 등 미존재 클래스)
  - processing.run(), native:* 알고리즘 호출(필요 시 명시적 허용 제외)
  - deprecated API 사용 금지

[좌표계/지오메트리 처리 옵션]
  - Multi-part geometry 확인 및 처리
  - geometry.isMultipart() 검사 후 분해 또는 처리
  - 레이어/피처 CRS 적절한 처리
  - buffer/unit 변환 시 프로젝트 또는 레이어 CRS 기준 사용

[코딩 규칙]
  - 들여쓰기는 4 spaces만 사용하고 탭 사용 금지
  - Python PEP 8 스타일 가이드라인 준수
  - 명확한 변수명 사용
  - 초보자도 이해 가능한 상세 주석 포함
  - 하나의 파일 형태로 제공

[예외 처리 규칙]
  - 문자, 숫자 값이 Null인 경우 QgsProcessingException 발생
  - 입력 레이어가 비어 있으면 처리 중단 후 예외 발생
  - geometry가 None이거나 Invalid일 경우 예외 처리
  - 파라미터 파싱 실패 시 명확한 예외 메시지 표시

위 명세에 따라 완전한 PyQGIS 알고리즘 코드를 작성하고, class 기반 ProcessingAlgorithm 형태로 제공해줘.
