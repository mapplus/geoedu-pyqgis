# -*- coding: utf-8 -*-
"""
Multiple Ring Buffer Algorithm for QGIS 3.x Processing Toolbox
--------------------------------------------------------------
이 스크립트는 입력 벡터 피처를 중심으로 쉼표로 구분된 여러 거리에 대한
다중 링(ring) 버퍼를 생성하는 QGIS Processing 알고리즘을 구현합니다.

사용법:
    QGIS Processing Toolbox > Scripts > Add Script from File
    또는 ~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/ 에 배치

작성 기준: PyQGIS 3 / QGIS 3.x
"""

# ------------------------------------------------------------------
# 필수 PyQGIS 및 Qt 모듈 임포트
# ------------------------------------------------------------------
from qgis.PyQt.QtCore import QCoreApplication, QVariant

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterString,
    QgsProcessingParameterBoolean,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsWkbTypes,
)


class MultipleRingBufferAlgorithm(QgsProcessingAlgorithm):
    """
    입력 벡터 레이어의 각 피처에 대해 다중 거리 기반 링 버퍼를 생성합니다.

    - OUTSIDE 옵션이 True이면 인접 버퍼 간의 차이(difference)를 계산하여
      도넛(ring) 형태의 폴리곤을 반환합니다.
    - 출력 레이어에는 버퍼 거리를 나타내는 'rind_dist' 필드가 포함됩니다.
    """

    # ------------------------------------------------------------------
    # 파라미터 상수 정의
    # 문자열 상수로 관리하면 오탈자 방지 및 유지보수가 용이합니다.
    # ------------------------------------------------------------------
    INPUT     = 'INPUT'      # 입력 벡터 레이어
    DISTANCES = 'DISTANCES'  # 쉼표 구분 거리 문자열
    OUTSIDE   = 'OUTSIDE'   # 링(ring) 모드 활성화 여부
    OUTPUT    = 'OUTPUT'     # 출력 싱크(레이어)

    # ------------------------------------------------------------------
    # 1. 알고리즘 기본 정보 메서드
    # ------------------------------------------------------------------

    def name(self):
        """
        알고리즘의 고유 내부 식별자입니다.
        소문자와 밑줄만 사용해야 하며 공백은 허용되지 않습니다.
        """
        return 'multiple_ring_buffer'

    def displayName(self):
        """
        Processing Toolbox UI에 표시될 사람이 읽기 쉬운 알고리즘 이름입니다.
        """
        return self.tr('Multiple Ring Buffer')

    def group(self):
        """
        이 알고리즘이 속할 그룹(폴더)의 표시 이름입니다.
        """
        return self.tr('MangoSystem Scripts')

    def groupId(self):
        """
        그룹의 고유 내부 식별자입니다.
        소문자와 밑줄만 사용합니다.
        """
        return 'mangoscripts'

    def shortHelpString(self):
        """
        Processing 패널의 우측에 표시되는 짧은 도움말 문자열입니다.
        알고리즘의 목적과 출력 스키마 변경 사항을 사용자에게 안내합니다.
        """
        return self.tr(
            '입력 벡터 피처를 중심으로 쉼표로 구분된 여러 거리에 대한 '
            '다중 링(Ring) 버퍼를 생성합니다.\n\n'
            '■ OUTSIDE 옵션이 True이면 인접 버퍼 간의 차이(difference)를 '
            '계산하여 도넛 형태의 링 폴리곤만 반환합니다.\n\n'
            '■ 출력 레이어에는 생성된 버퍼 거리가 저장된 [rind_dist] 필드가 '
            '자동으로 추가됩니다. 이 필드는 Double 타입이며 '
            '길이 10, 소수점 이하 4자리로 설정됩니다.'
        )

    def tr(self, string):
        """
        다국어 번역을 위한 헬퍼 메서드입니다.
        번역 파일(.qm)이 없을 경우 원본 문자열을 그대로 반환합니다.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """
        Processing 프레임워크가 새 알고리즘 인스턴스를 생성할 때 호출됩니다.
        반드시 자신의 클래스 인스턴스를 반환해야 합니다.
        """
        return MultipleRingBufferAlgorithm()

    # ------------------------------------------------------------------
    # 2. 파라미터 정의 (initAlgorithm)
    # ------------------------------------------------------------------

    def initAlgorithm(self, config=None):
        """
        알고리즘의 입출력 파라미터를 정의합니다.
        Processing 프레임워크 초기화 시 한 번 호출됩니다.

        파라미터 추가 순서가 UI 표시 순서와 동일합니다.
        """

        # ── 파라미터 1: INPUT ──────────────────────────────────────────
        # 입력 벡터 레이어를 받는 파라미터입니다.
        # QgsProcessing.TypeVectorAnyGeometry 대신 TypeVector를 사용하여
        # 포인트, 라인, 폴리곤 등 모든 벡터 지오메트리 타입을 허용합니다.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name=self.INPUT,
                description=self.tr('입력 레이어'),
                types=[QgsProcessing.TypeVectorAnyGeometry],  # 모든 벡터 타입 허용
            )
        )

        # ── 파라미터 2: DISTANCES ──────────────────────────────────────
        # 쉼표로 구분된 거리 값 문자열을 입력받습니다.
        # 예: '500, 1000, 1500'
        # 입력 레이어의 CRS 단위(미터 또는 도)에 따라 거리 단위가 결정됩니다.
        self.addParameter(
            QgsProcessingParameterString(
                name=self.DISTANCES,
                description=self.tr('버퍼 거리 (쉼표로 구분, 예: 500, 1000, 1500)'),
                defaultValue='500, 1000, 1500',
                multiLine=False,  # 단일 행 입력
                optional=False,   # 필수 파라미터
            )
        )

        # ── 파라미터 3: OUTSIDE ────────────────────────────────────────
        # True: 인접 버퍼 간의 차이(difference)를 계산하여 링(도넛) 폴리곤 생성
        # False: 각 거리에 대한 단순 버퍼 폴리곤 생성 (서로 겹침)
        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.OUTSIDE,
                description=self.tr('링(Ring) 모드: 인접 버퍼 간 차이만 출력'),
                defaultValue=True,  # 기본값: 링 모드 활성화
                optional=True,      # 선택 파라미터 (기본값 사용 가능)
            )
        )

        # ── 파라미터 4: OUTPUT ─────────────────────────────────────────
        # 처리 결과를 저장할 출력 싱크(레이어)를 정의합니다.
        # 결과는 항상 폴리곤 지오메트리 타입으로 출력됩니다.
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                name=self.OUTPUT,
                description=self.tr('다중 링 버퍼 출력'),
                type=QgsProcessing.TypeVectorPolygon,  # 출력은 폴리곤으로 고정
            )
        )

    # ------------------------------------------------------------------
    # 3. 핵심 처리 로직 (processAlgorithm)
    # ------------------------------------------------------------------

    def processAlgorithm(self, parameters, context, feedback):
        """
        알고리즘의 실제 처리 로직입니다.
        'Run' 버튼 클릭 또는 배치 처리 시 호출됩니다.

        Args:
            parameters (dict): initAlgorithm에서 정의한 파라미터 값 딕셔너리
            context (QgsProcessingContext): 처리 컨텍스트 (프로젝트 CRS 등 포함)
            feedback (QgsProcessingFeedback): 진행률 보고 및 취소 감지 객체

        Returns:
            dict: 출력 파라미터 이름과 결과 값의 딕셔너리
        """

        # ── Step 1: 파라미터 값 추출 ───────────────────────────────────

        # 입력 벡터 레이어 소스를 가져옵니다.
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # 입력 레이어 유효성 검사: None이면 즉시 예외를 발생시킵니다.
        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        # 거리 문자열을 파싱하여 float 리스트로 변환합니다.
        distances_raw = self.parameterAsString(parameters, self.DISTANCES, context)

        # 쉼표 기준으로 분리 후 공백 제거 → float 변환 시도
        distance_list = []
        for token in distances_raw.split(','):
            token = token.strip()
            if not token:
                continue  # 빈 토큰은 건너뜁니다.
            try:
                val = float(token)
                distance_list.append(val)
            except ValueError:
                # 숫자로 변환할 수 없는 값이 포함된 경우 예외 발생
                raise QgsProcessingException(
                    self.tr(
                        f"거리 값 파싱 오류: '{token}'은(는) 유효한 숫자가 아닙니다. "
                        "쉼표로 구분된 숫자만 입력하세요. (예: 500, 1000, 1500)"
                    )
                )

        # 유효한 거리 값이 하나도 없으면 예외 발생
        if not distance_list:
            raise QgsProcessingException(
                self.tr(
                    "거리 값이 비어 있습니다. "
                    "쉼표로 구분된 숫자를 하나 이상 입력하세요."
                )
            )

        # 거리 목록을 오름차순으로 정렬합니다.
        # 링(difference) 계산의 정확성을 위해 반드시 정렬이 필요합니다.
        distance_list.sort()

        # 링 모드 활성화 여부를 Boolean으로 가져옵니다.
        use_rings = self.parameterAsBoolean(parameters, self.OUTSIDE, context)

        # ── Step 2: 출력 스키마(필드) 정의 ────────────────────────────

        # 입력 레이어의 기존 필드를 모두 복사합니다.
        output_fields = QgsFields(source.fields())

        # 버퍼 거리를 저장할 'rind_dist' 필드를 추가합니다.
        # - 타입: Double (QVariant.Double)
        # - 길이(len): 10 (전체 자릿수)
        # - 정밀도(prec): 4 (소수점 이하 자릿수)
        rind_dist_field = QgsField(
            name='rind_dist',
            type=QVariant.Double,
            len=10,
            prec=4,
            comment='버퍼 생성 거리',  # 필드 설명 (선택 사항)
        )
        output_fields.append(rind_dist_field)

        # ── Step 3: 출력 싱크 생성 ────────────────────────────────────

        # 출력 싱크(레이어)를 초기화합니다.
        # - WKB 타입: MultiPolygon (difference() 결과가 멀티파트일 수 있음)
        # - CRS: 입력 레이어의 CRS를 그대로 사용
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,
            QgsWkbTypes.MultiPolygon,  # 멀티파트 폴리곤으로 설정
            source.sourceCrs(),
        )

        # 출력 싱크 유효성 검사
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )

        # ── Step 4: 피처 반복 및 버퍼/링 생성 ─────────────────────────

        # 전체 피처 수를 가져옵니다 (진행률 계산에 사용).
        total_features = source.featureCount()

        # 진행률 계산의 분모가 0이 되지 않도록 처리합니다.
        if total_features > 0:
            progress_step = 100.0 / total_features
        else:
            progress_step = 0

        # 입력 레이어의 모든 피처를 순차적으로 처리합니다.
        for current_index, feature in enumerate(source.getFeatures()):

            # 사용자가 취소 버튼을 눌렀는지 확인합니다.
            # Processing 프레임워크의 취소 신호를 주기적으로 확인해야 합니다.
            if feedback.isCanceled():
                feedback.pushInfo(self.tr('사용자에 의해 처리가 취소되었습니다.'))
                break

            # 현재 피처의 원본 지오메트리를 가져옵니다.
            geom = feature.geometry()

            # 지오메트리가 유효하지 않으면 이 피처는 건너뜁니다.
            if geom is None or geom.isEmpty():
                feedback.pushWarning(
                    self.tr(f'피처 ID {feature.id()}의 지오메트리가 비어 있어 건너뜁니다.')
                )
                continue

            # 이전 거리의 버퍼 지오메트리를 추적하는 변수입니다.
            # 링 모드에서 difference() 계산에 사용됩니다.
            prev_buffer_geom = None

            # ── 각 거리에 대해 버퍼 생성 ──────────────────────────────
            for rind_distance in distance_list:

                # 원본 지오메트리를 기준으로 버퍼를 생성합니다.
                # - 두 번째 인수 (segments=24): 원의 근사 정밀도
                #   값이 클수록 더 부드러운 원형 버퍼가 생성됩니다.
                current_buffer_geom = geom.buffer(rind_distance, 24)

                # 최종 출력에 사용할 지오메트리를 결정합니다.
                if use_rings and prev_buffer_geom is not None:
                    # ── 링 모드: 현재 버퍼에서 이전 버퍼의 차이를 계산 ──
                    # 결과는 도넛(ring) 형태의 폴리곤이 됩니다.
                    # 첫 번째 버퍼(prev_buffer_geom이 None인 경우)는
                    # 차이 계산 없이 원형 버퍼 그대로 사용됩니다.
                    output_geom = current_buffer_geom.difference(prev_buffer_geom)
                else:
                    # ── 일반 모드 또는 첫 번째 버퍼: 버퍼 지오메트리 그대로 사용 ──
                    output_geom = current_buffer_geom

                # 현재 버퍼를 다음 반복의 '이전 버퍼'로 저장합니다.
                prev_buffer_geom = current_buffer_geom

                # ── 출력 피처 구성 및 싱크에 추가 ──────────────────────

                # 새 피처 객체를 생성하고 필드 스키마를 설정합니다.
                out_feature = QgsFeature(output_fields)

                # 계산된 버퍼/링 지오메트리를 피처에 할당합니다.
                out_feature.setGeometry(output_geom)

                # 입력 피처의 모든 원본 속성 값을 복사합니다.
                # output_fields에 rind_dist가 추가되었으므로
                # 인덱스 0부터 len(source.fields())-1 까지만 복사합니다.
                original_attrs = feature.attributes()
                out_attrs = original_attrs + [rind_distance]  # rind_dist 값 추가
                out_feature.setAttributes(out_attrs)

                # 완성된 피처를 출력 싱크에 추가합니다.
                sink.addFeature(out_feature)

            # ── 진행률 업데이트 ────────────────────────────────────────
            # 현재 처리된 피처 수를 기준으로 진행률(0~100%)을 업데이트합니다.
            feedback.setProgress(int((current_index + 1) * progress_step))

        # ── Step 5: 처리 완료 메시지 출력 및 결과 반환 ────────────────

        feedback.pushInfo(
            self.tr(
                f'처리 완료: {total_features}개 피처 × '
                f'{len(distance_list)}개 거리 = '
                f'총 {total_features * len(distance_list)}개 링 버퍼 생성'
            )
        )

        # 출력 레이어의 대상 ID를 딕셔너리로 반환합니다.
        # Processing 프레임워크가 이 값으로 출력 레이어를 QGIS 프로젝트에 로드합니다.
        return {self.OUTPUT: dest_id}
