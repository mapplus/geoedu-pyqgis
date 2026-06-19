import math

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsWkbTypes,
)


class MultipleRingBufferAlgorithm(QgsProcessingAlgorithm):
    """
    입력 벡터 피처별로 여러 거리의 버퍼를 생성하는 QGIS Processing 알고리즘입니다.

    OUTSIDE가 True인 경우:
        - 첫 번째 거리는 일반 버퍼로 출력합니다.
        - 두 번째 거리부터는 현재 버퍼에서 직전 전체 버퍼를 차감하여
          서로 겹치지 않는 링 폴리곤을 생성합니다.

    OUTSIDE가 False인 경우:
        - 각 거리에 대한 일반 누적 버퍼를 모두 출력합니다.
    """

    # Processing 입력 및 출력 파라미터의 고유 키입니다.
    INPUT = "INPUT"
    DISTANCES = "DISTANCES"
    OUTSIDE = "OUTSIDE"
    OUTPUT = "OUTPUT"

    # 요청된 출력 거리 필드명입니다.
    RIND_DIST_FIELD = "rind_dist"

    def tr(self, string):
        """
        문자열을 QGIS 번역 시스템에서 처리할 수 있도록 반환합니다.
        """

        return QCoreApplication.translate(
            "MultipleRingBufferAlgorithm",
            string,
        )

    def createInstance(self):
        """
        Processing 레지스트리가 알고리즘을 복제할 때 사용할
        새로운 알고리즘 인스턴스를 반환합니다.
        """

        return MultipleRingBufferAlgorithm()

    def name(self):
        """
        Processing 내부에서 사용하는 알고리즘의 고유 이름을 반환합니다.
        """

        return "multiple_ring_buffer"

    def displayName(self):
        """
        Processing 툴박스에 표시할 알고리즘 이름을 반환합니다.
        """

        return self.tr("Multiple Ring Buffer")

    def group(self):
        """
        Processing 툴박스에서 알고리즘이 속할 그룹 이름을 반환합니다.
        """

        return self.tr("MangoSystem Scripts")

    def groupId(self):
        """
        Processing 내부에서 사용하는 그룹 ID를 반환합니다.
        """

        return "mangoscripts"

    def shortHelpString(self):
        """
        Processing 알고리즘 도움말에 표시할 설명을 반환합니다.
        """

        return self.tr(
            "입력 벡터 피처별로 쉼표로 구분된 여러 거리의 버퍼를 생성합니다. "
            "OUTSIDE를 활성화하면 첫 번째 버퍼 이후부터 현재 버퍼와 직전 "
            "버퍼의 차이를 계산하여 겹치지 않는 링 폴리곤을 생성합니다. "
            "출력에는 각 버퍼의 생성 거리를 저장하는 'rind_dist' 필드가 "
            "포함됩니다. 거리 단위는 입력 레이어 CRS의 지도 단위입니다."
        )

    def initAlgorithm(self, config=None):
        """
        알고리즘에서 사용할 입력 및 출력 파라미터를 정의합니다.
        """

        # 포인트, 라인, 폴리곤을 포함한 모든 지오메트리 유형의
        # 벡터 입력 레이어를 허용합니다.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input vector layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        # 사용자가 다음과 같은 형식으로 여러 버퍼 거리를 입력합니다.
        #
        #     500, 1000, 1500
        #
        # 각 값의 단위는 입력 레이어 CRS의 좌표 단위입니다.
        self.addParameter(
            QgsProcessingParameterString(
                self.DISTANCES,
                self.tr("Distances (comma-separated)"),
                defaultValue="500, 1000, 1500",
            )
        )

        # True이면 첫 번째 버퍼 이후부터 직전 버퍼를 차감하여
        # 서로 겹치지 않는 링 폴리곤을 생성합니다.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.OUTSIDE,
                self.tr("Create outside rings"),
                defaultValue=True,
            )
        )

        # 버퍼 결과는 폴리곤 계열 지오메트리이므로
        # Processing 출력 파라미터를 폴리곤 타입으로 정의합니다.
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Multiple ring buffer"),
                QgsProcessing.TypeVectorPolygon,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        입력 피처별로 다중 버퍼 또는 다중 링을 생성합니다.
        """

        # -------------------------------------------------------------
        # 1. 입력 벡터 레이어 읽기
        # -------------------------------------------------------------

        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context,
        )

        # 입력 레이어를 QgsFeatureSource로 변환할 수 없는 경우
        # Processing 예외를 발생시킵니다.
        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        # -------------------------------------------------------------
        # 2. DISTANCES 및 OUTSIDE 파라미터 읽기
        # -------------------------------------------------------------

        distance_text = self.parameterAsString(
            parameters,
            self.DISTANCES,
            context,
        )

        outside = self.parameterAsBool(
            parameters,
            self.OUTSIDE,
            context,
        )

        # -------------------------------------------------------------
        # 3. 쉼표로 구분된 거리 문자열 파싱
        # -------------------------------------------------------------

        # 쉼표를 기준으로 문자열을 분리하고 각 항목의 공백을 제거합니다.
        #
        # 예:
        #     "500, 1000, 1500"
        #
        # 결과:
        #     ["500", "1000", "1500"]
        distance_tokens = [
            token.strip()
            for token in distance_text.split(",")
        ]

        # 빈 문자열이나 빈 항목이 포함된 경우를 검사합니다.
        #
        # 잘못된 입력 예:
        #     ""
        #     "500,,1000"
        #     "500, ,1000"
        if not distance_tokens or any(
            token == ""
            for token in distance_tokens
        ):
            raise QgsProcessingException(
                self.tr(
                    "DISTANCES에는 하나 이상의 유효한 숫자를 "
                    "쉼표로 구분하여 입력해야 합니다."
                )
            )

        # 모든 거리 문자열을 float로 변환합니다.
        # 하나라도 숫자로 변환할 수 없으면 알고리즘 실행을 중단합니다.
        try:
            distances = [
                float(token)
                for token in distance_tokens
            ]
        except ValueError as exc:
            raise QgsProcessingException(
                self.tr(
                    "DISTANCES에 숫자가 아닌 값이 포함되어 있습니다: {0}"
                ).format(distance_text)
            ) from exc

        # NaN, Infinity, 0 및 음수 거리는 허용하지 않습니다.
        invalid_distances = [
            distance
            for distance in distances
            if not math.isfinite(distance) or distance <= 0
        ]

        if invalid_distances:
            raise QgsProcessingException(
                self.tr(
                    "모든 버퍼 거리는 0보다 큰 유한한 숫자여야 합니다: {0}"
                ).format(
                    ", ".join(
                        str(value)
                        for value in invalid_distances
                    )
                )
            )

        # OUTSIDE가 True이면 현재 버퍼가 직전 버퍼를 완전히 포함해야
        # 정상적인 링 차분이 만들어집니다.
        #
        # 따라서 거리가 다음과 같이 엄격한 오름차순인지 검사합니다.
        #
        # 정상:
        #     500, 1000, 1500
        #
        # 오류:
        #     1000, 500, 1500
        #     500, 500, 1000
        if outside:
            for previous_distance, current_distance in zip(
                distances,
                distances[1:],
            ):
                if current_distance <= previous_distance:
                    raise QgsProcessingException(
                        self.tr(
                            "OUTSIDE가 활성화된 경우 DISTANCES는 "
                            "중복 없이 엄격한 오름차순이어야 합니다."
                        )
                    )

        # -------------------------------------------------------------
        # 4. 출력 필드 정의
        # -------------------------------------------------------------

        # 입력 레이어의 전체 필드 정의를 복사합니다.
        output_fields = source.fields()

        # 입력 레이어에 이미 rind_dist라는 필드가 있으면
        # 동일한 이름의 필드를 추가할 수 없으므로 명확한 오류를 발생시킵니다.
        if output_fields.indexFromName(self.RIND_DIST_FIELD) >= 0:
            raise QgsProcessingException(
                self.tr(
                    "입력 레이어에 이미 '{0}' 필드가 존재합니다."
                ).format(self.RIND_DIST_FIELD)
            )

        # 버퍼 거리를 저장할 rind_dist 필드를 추가합니다.
        #
        # 필드 타입: Double
        # 길이:      10
        # 정밀도:    4
        field_added = output_fields.append(
            QgsField(
                self.RIND_DIST_FIELD,
                QVariant.Double,
                "",
                10,
                4,
            )
        )

        if not field_added:
            raise QgsProcessingException(
                self.tr(
                    "'{0}' 출력 필드를 추가할 수 없습니다."
                ).format(self.RIND_DIST_FIELD)
            )

        # -------------------------------------------------------------
        # 5. 출력 Feature Sink 생성
        # -------------------------------------------------------------

        # 단일 피처의 버퍼는 Polygon이 될 수 있지만, 멀티파트 입력이나
        # 차분 결과는 MultiPolygon이 될 수 있습니다.
        #
        # 따라서 실제 출력 싱크는 MultiPolygon으로 생성합니다.
        sink, destination_id = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,
            QgsWkbTypes.MultiPolygon,
            source.sourceCrs(),
        )

        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )

        # -------------------------------------------------------------
        # 6. 진행률 계산을 위한 초기값 설정
        # -------------------------------------------------------------

        feature_count = source.featureCount()
        distance_count = len(distances)

        # 한 입력 피처마다 거리 개수만큼 버퍼 연산을 수행하므로
        # 전체 처리 단계를 다음과 같이 계산합니다.
        #
        # 전체 단계 = 입력 피처 수 × 거리 수
        total_steps = (
            feature_count * distance_count
            if feature_count > 0
            else 0
        )

        progress_per_step = (
            100.0 / total_steps
            if total_steps > 0
            else 0.0
        )

        completed_steps = 0

        # -------------------------------------------------------------
        # 7. 입력 피처 반복
        # -------------------------------------------------------------

        for input_feature in source.getFeatures():
            # 사용자가 Processing 실행을 취소했는지 확인합니다.
            if feedback.isCanceled():
                break

            input_geometry = input_feature.geometry()

            # NULL 또는 빈 지오메트리는 버퍼를 생성할 수 없으므로
            # 오류 메시지를 기록하고 해당 피처를 건너뜁니다.
            if input_geometry.isNull() or input_geometry.isEmpty():
                feedback.reportError(
                    self.tr(
                        "피처 ID {0}은(는) 비어 있는 지오메트리이므로 "
                        "건너뜁니다."
                    ).format(input_feature.id()),
                    fatalError=False,
                )

                # 건너뛴 피처도 전체 진행 단계에 포함되어 있으므로
                # 거리 개수만큼 처리 완료 단계에 반영합니다.
                completed_steps += distance_count

                if total_steps > 0:
                    feedback.setProgress(
                        min(
                            100.0,
                            completed_steps * progress_per_step,
                        )
                    )

                continue

            # 직전 거리에서 생성된 "전체 버퍼"를 저장합니다.
            #
            # 주의:
            # 이 변수에는 차분 결과인 링을 저장하면 안 됩니다.
            # 다음 링은 항상 현재 전체 버퍼에서 직전 전체 버퍼를
            # 빼는 방식으로 생성해야 합니다.
            previous_buffer = None

            # ---------------------------------------------------------
            # 8. 각 거리별 버퍼 및 링 생성
            # ---------------------------------------------------------

            for rind_distance in distances:
                if feedback.isCanceled():
                    break

                # 24개의 세그먼트를 사용하여 곡선을 근사하는
                # 일반 버퍼를 생성합니다.
                current_buffer = input_geometry.buffer(
                    rind_distance,
                    24,
                )

                # 버퍼 생성 결과가 NULL 또는 빈 지오메트리인지 검사합니다.
                if current_buffer.isNull() or current_buffer.isEmpty():
                    error_detail = current_buffer.lastError()

                    raise QgsProcessingException(
                        self.tr(
                            "피처 ID {0}, 거리 {1}에서 버퍼 생성에 "
                            "실패했습니다. {2}"
                        ).format(
                            input_feature.id(),
                            rind_distance,
                            error_detail,
                        )
                    )

                # OUTSIDE가 True이고 첫 번째 버퍼가 아닌 경우,
                # 현재 전체 버퍼에서 직전 전체 버퍼를 차감합니다.
                #
                # 예:
                #     current_buffer  = 1000m 버퍼
                #     previous_buffer = 500m 버퍼
                #
                #     output_geometry = 500m 초과 ~ 1000m 이하 영역
                if outside and previous_buffer is not None:
                    output_geometry = current_buffer.difference(
                        previous_buffer
                    )
                else:
                    # 첫 번째 버퍼 또는 OUTSIDE=False인 경우에는
                    # 현재 전체 버퍼를 그대로 출력합니다.
                    output_geometry = current_buffer

                # 차분 또는 버퍼 결과가 정상적으로 생성되었는지 검사합니다.
                if output_geometry.isNull() or output_geometry.isEmpty():
                    error_detail = output_geometry.lastError()

                    raise QgsProcessingException(
                        self.tr(
                            "피처 ID {0}, 거리 {1}에서 링 지오메트리 "
                            "생성에 실패했습니다. {2}"
                        ).format(
                            input_feature.id(),
                            rind_distance,
                            error_detail,
                        )
                    )

                # 다음 거리의 차분 연산을 위해 현재 전체 버퍼를 저장합니다.
                #
                # output_geometry가 아니라 current_buffer를 저장해야 합니다.
                previous_buffer = current_buffer

                # 버퍼와 차분 결과는 Polygon 또는 MultiPolygon이 될 수 있습니다.
                # 출력 싱크의 WKB 타입과 일치하도록 MultiPolygon으로 승격합니다.
                if not output_geometry.convertToMultiType():
                    raise QgsProcessingException(
                        self.tr(
                            "피처 ID {0}, 거리 {1}의 결과를 "
                            "MultiPolygon으로 변환할 수 없습니다."
                        ).format(
                            input_feature.id(),
                            rind_distance,
                        )
                    )

                # -----------------------------------------------------
                # 9. 출력 피처 생성
                # -----------------------------------------------------

                # 출력 필드 구조를 사용하는 새로운 QgsFeature를 생성합니다.
                output_feature = QgsFeature(output_fields)

                # 생성된 버퍼 또는 링 지오메트리를 설정합니다.
                output_feature.setGeometry(output_geometry)

                # 입력 피처의 전체 속성을 복사하고 마지막에
                # 현재 버퍼 거리 값을 추가합니다.
                output_feature.setAttributes(
                    input_feature.attributes() + [rind_distance]
                )

                # 출력 Feature Sink에 새 피처를 기록합니다.
                #
                # FastInsert는 출력 피처의 ID를 다시 갱신할 필요가 없는 경우
                # 보다 빠르게 피처를 추가하도록 요청하는 플래그입니다.
                if not sink.addFeature(
                    output_feature,
                    QgsFeatureSink.FastInsert,
                ):
                    raise QgsProcessingException(
                        self.tr(
                            "피처 ID {0}, 거리 {1}의 결과를 "
                            "출력 싱크에 기록할 수 없습니다."
                        ).format(
                            input_feature.id(),
                            rind_distance,
                        )
                    )

                # -----------------------------------------------------
                # 10. 진행률 업데이트
                # -----------------------------------------------------

                completed_steps += 1

                if total_steps > 0:
                    feedback.setProgress(
                        min(
                            100.0,
                            completed_steps * progress_per_step,
                        )
                    )

            # 내부 거리 반복 중 취소된 경우 외부 피처 반복도 종료합니다.
            if feedback.isCanceled():
                break

        # 정상적으로 완료된 경우 진행률을 정확히 100으로 설정합니다.
        if not feedback.isCanceled():
            feedback.setProgress(100.0)

        # Processing 알고리즘의 출력 목적지 ID를 반환합니다.
        return {
            self.OUTPUT: destination_id,
        }