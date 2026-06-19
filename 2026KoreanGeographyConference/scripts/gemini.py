from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsWkbTypes
)
from PyQt5.QtCore import QVariant

class MultipleRingBufferAlgorithm(QgsProcessingAlgorithm):
    """
    QGIS 3 Processing 툴박스용 다중 링 버퍼(Multiple Ring Buffer) 생성 알고리즘.
    입력 피처를 기준으로 사용자가 입력한 여러 거리에 대한 버퍼 또는 링 폴리곤을 생성합니다.
    """

    # 파라미터 및 출력 상수 정의
    INPUT = 'INPUT'
    DISTANCES = 'DISTANCES'
    OUTSIDE = 'OUTSIDE'
    OUTPUT = 'OUTPUT'

    def name(self):
        # 알고리즘의 고유 ID (영문 소문자, 공백 없음)
        return 'multiple_ring_buffer'

    def displayName(self):
        # 툴박스에 표시될 알고리즘 이름
        return 'Multiple Ring Buffer'

    def group(self):
        # 알고리즘이 속할 그룹 이름
        return 'MangoSystem Scripts'

    def groupId(self):
        # 알고리즘이 속할 그룹의 고유 ID
        return 'mangoscripts'

    def shortHelpString(self):
        # 사용자에게 제공되는 간략한 도움말 도움말
        return (
            "이 알고리즘은 입력 벡터 피처를 중심으로 쉼표로 구분된 여러 거리에 대한 다중 링 버퍼를 생성합니다.\n\n"
            "생성된 버퍼 거리가 포함된 'rind_dist' 필드가 속성 테이블(출력)에 자동으로 추가됩니다.\n"
            "'Outside' 옵션이 활성화되면 각 거리별 인접 버퍼 간의 차이를 계산하여 도넛 모양의 링 폴리곤을 생성합니다."
        )

    def initAlgorithm(self, config=None):
        # 1. 입력 벡터 레이어 파라미터 (점, 선, 면 모두 허용)
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                'Input vector layer',
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # 2. 쉼표로 구분된 거리 값 문자열 파라미터
        self.addParameter(
            QgsProcessingParameterString(
                self.DISTANCES,
                'Buffer distances (comma-separated)',
                defaultValue='500, 1000, 1500'
            )
        )

        # 3. 링 모양 생성 여부를 결정하는 Boolean 파라미터
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.OUTSIDE,
                'Produce rings outside previous buffers (Difference)',
                defaultValue=True
            )
        )

        # 4. 출력 피처 싱크 파라미터 (결과물은 항상 폴리곤/멀티폴리곤 타입)
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Output layer',
                QgsProcessing.TypeVectorPolygon
            )
        )

    def createInstance(self):
        # QGIS가 알고리즘의 새 인스턴스를 생성할 때 호출
        return MultipleRingBufferAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        # 파라미터 값 가져오기
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        distances_str = self.parameterAsString(parameters, self.DISTANCES, context)
        outside_only = self.parameterAsBoolean(parameters, self.OUTSIDE, context)

        # 거리 문자열 파싱 및 유효성 검사
        distances = []
        if not distances_str.strip():
            raise QgsProcessingException("거리(DISTANCES) 입력값이 비어 있습니다.")

        try:
            # 쉼표 분리 후 공백 제거, float 변환 및 오름차순 정렬
            distances = [float(d.strip()) for d in distances_str.split(',') if d.strip()]
            distances.sort()
        except ValueError:
            raise QgsProcessingException("거리 값은 쉼표로 구분된 올바른 숫자 형태여야 합니다. (예: 500, 1000, 1500)")

        if not distances:
            raise QgsProcessingException("유효한 거리 값이 파싱되지 않았습니다.")

        # 출력 레이어의 필드(스키마) 정의
        # 원본 레이어의 모든 필드를 복사한 후, 'rind_dist' 필드를 추가합니다.
        fields = source.fields()
        fields.append(QgsField('rind_dist', QVariant.Double, 'double', 10, 4))

        # 피처 싱크(Sink) 초기화
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.MultiPolygon, # 버퍼 차이 연산 시 멀티폴리곤이 생성될 수 있으므로 MultiPolygon 지정
            source.sourceCrs()
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # 피처 반복 처리 및 진행률 설정을 위한 준비
        total = source.featureCount()
        features = source.getFeatures()
        current = 0

        for feature in features:
            # 취소 버튼 클릭 시 프로세스 중단
            if feedback.isCanceled():
                break

            geom = feature.geometry()
            if geom.isNull():
                continue

            # 이전 단계의 버퍼 지오메트리를 저장할 변수 (차이 연산용)
            previous_geom = None

            # 각 거리별로 버퍼 및 링 생성
            for rind_distance in distances:
                # 24개 세그먼트를 사용하여 부드러운 버퍼 생성
                current_geom = geom.buffer(rind_distance, 24)

                if current_geom.isNull():
                    continue

                # 출력용 지오메트리 변수 초기화
                output_geom = current_geom

                # Outside 옵션이 True이고, 직전 버퍼가 존재하는 경우 (두 번째 거리부터)
                if outside_only and previous_geom is not None:
                    # 현재 버퍼에서 직전 버퍼 영역을 제외하여 링(도넛) 생성
                    output_geom = current_geom.difference(previous_geom)

                # 새로운 출력 피처 생성 및 속성 정의
                out_feature = QgsFeature(fields)
                out_feature.setGeometry(output_geom)
                
                # 원본 속성 복사 후, 마지막 필드에 현재 버퍼 거리 설정
                attributes = feature.attributes()
                attributes.append(rind_distance)
                out_feature.setAttributes(attributes)

                # 싱크에 피처 추가
                sink.addFeature(out_feature, QgsFeatureSink.FastInsert)

                # 현재 버퍼를 다음 루프의 이전 버퍼로 저장
                previous_geom = current_geom

            # 진행률 업데이트
            current += 1
            feedback.setProgress(int(current / total * 100))

        # 결과 맵 레이어 ID 반환
        return {self.OUTPUT: dest_id}