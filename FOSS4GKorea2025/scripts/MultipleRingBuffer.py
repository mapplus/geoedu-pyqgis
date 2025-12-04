# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                  : Multiple Ring Buffer
Description           : Creates multiple buffers (rings) at specified distances
                        around the input vector features using PyQGIS Processing.
Date                  : 28/Dec/2018 (Refactored: 2025/12/04)
Copyright             : (C) 2015 by Minpa Lee (mapplus@gmail.com)
License               : GNU General Public License v2 or later
***************************************************************************/
"""

# 필요한 PyQt 및 QGIS 모듈 임포트
from PyQt5.QtCore import (QCoreApplication,
                          QVariant)
from qgis.core import (QgsProcessing,
                        QgsFeature,
                        QgsFeatureSink,
                        QgsField,
                        QgsWkbTypes,
                        QgsProcessingException,
                        QgsProcessingAlgorithm,
                        QgsProcessingParameterFeatureSource,
                        QgsProcessingParameterString,
                        QgsProcessingParameterBoolean,
                        QgsProcessingParameterFeatureSink)

# 'processing' 모듈은 이 코드가 외부 알고리즘을 호출하지 않으므로 제거함.


class MultipleRingBufferAlgorithm(QgsProcessingAlgorithm):
    """
    입력 피처를 기반으로 쉼표로 구분된 여러 거리에 대한
    다중 링 버퍼(Ring Buffer)를 생성하는 QGIS Processing 알고리즘 클래스.
    'Outside Polygons Only' 옵션을 통해 중첩 버퍼 또는 고리(Ring) 형태의 출력을 제어.
    """
    # --- 파라미터 상수 정의 (클래스 내부 속성으로 정의) ---
    INPUT = 'INPUT'
    DISTANCES = 'DISTANCES'
    OUTSIDE = 'OUTSIDE'
    OUTPUT = 'OUTPUT'


    def tr(self, string):
        """
        문자열을 번역 가능하도록 처리하는 함수 (다국어 지원).
        """
        return QCoreApplication.translate('Processing', string)


    def createInstance(self):
        """
        알고리즘 인스턴스를 반환하여 프레임워크가 알고리즘을 로드할 수 있도록 함.
        """
        return MultipleRingBufferAlgorithm()


    def name(self):
        """
        알고리즘의 고유한 내부 이름 (소문자, 공백 없음 권장).
        """
        return 'multiple_ring_buffer'


    def displayName(self):
        """
        QGIS 툴박스에 표시될 알고리즘 이름.
        """
        return self.tr('Multiple Ring Buffer')


    def group(self):
        """
        툴박스에서 알고리즘이 속할 그룹 이름.
        """
        return self.tr('FOSS4G Korea 2025')


    def groupId(self):
        """
        그룹의 고유 ID.
        """
        return 'foss4gkorea'


    def shortHelpString(self):
        """
        알고리즘의 간단한 도움말 설명.
        """
        return self.tr('입력 피처를 중심으로 지정된 거리만큼의 다중 버퍼를 생성합니다. "바깥쪽 폴리곤만" 옵션을 선택하면, 연속적인 버퍼들 간의 **차이(Difference)**를 계산하여 **동심원 모양의 링(고리)**이 생성됩니다. 출력 레이어에는 버퍼 거리를 나타내는 "rind_dist" 필드가 포함됩니다.')


    def initAlgorithm(self, config=None):
        """
        알고리즘의 입력 및 출력 파라미터를 정의.
        """
        # 1. 입력 벡터 레이어 파라미터 정의
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input Vector Layer'),
                [QgsProcessing.TypeVector]  # 벡터 타입만 허용
            )
        )

        # 2. 쉼표로 구분된 거리 값 문자열 파라미터 정의
        self.addParameter(
            QgsProcessingParameterString(
                self.DISTANCES,
                self.tr('Comma Separated Distance Values (e.g., 500, 1000, 1500)'),
                defaultValue='500, 1000, 1500',
                multiLine=False
            )
        )

        # 3. 'Outside Polygons Only' 부울(Boolean) 파라미터 정의
        # True: 링 버퍼(차이 영역) 생성, False: 중첩된 버퍼를 생성.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.OUTSIDE,
                self.tr('Outside Polygons Only (Create rings)'),
                defaultValue=True,  # 기본값: 링(차이 영역) 생성
                optional=True
            )
        )

        # 4. 출력 벡터 레이어 파라미터 정의 (싱크)
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Buffered Output Layer'),
                QgsProcessing.TypeVectorPolygon  # 출력은 항상 폴리곤 타입
            )
        )


    def processAlgorithm(self, parameters, context, feedback):
        """
        알고리즘의 실제 처리 로직.
        """
        # 1. 입력 소스(Source) 가져오기 및 유효성 검사
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            # 소스가 유효하지 않은 경우 예외 발생
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        # 2. 거리 값 문자열 및 부울 파라미터 가져오기 및 파싱
        distances_str = self.parameterAsString(parameters, self.DISTANCES, context)

        # 문자열을 파싱하여 유효한 float 리스트로 변환 (오류 처리 포함)
        try:
            # 쉼표를 기준으로 분리하고 공백 제거 후, float으로 변환 시도
            distance_values = [float(d.strip()) for d in distances_str.split(',') if d.strip()]
            # 거리 값은 0보다 커야 함
            if any(d <= 0 for d in distance_values):
                raise ValueError("Distance values must be greater than 0.")
        except ValueError as e:
            raise QgsProcessingException(self.tr(f'Invalid distance value(s) provided. Error: {e}'))

        # 유효한 거리 값이 하나도 없는 경우
        if not distance_values:
            raise QgsProcessingException(self.tr('No valid distance values provided. Comma separated distance values are required!'))

        # 거리를 오름차순으로 정렬 (링 계산의 필수 전제 조건)
        distance_values.sort()

        outside_only = self.parameterAsBool(parameters, self.OUTSIDE, context)
        feedback.pushInfo(self.tr('Processing features for distances: {}').format(distance_values))

        # 3. 출력 필드 설정 및 싱크(Sink) 생성
        output_fields = source.fields()
        # 'rind_dist' 필드 추가 (링 거리) - Double 타입
        output_fields.append(QgsField('rind_dist', QVariant.Double, 'double', 10, 4))

        # 출력 싱크(Sink) 생성 및 결과 레이어 ID 가져오기
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,                      # 새로 정의된 필드 사용
            QgsWkbTypes.Polygon,                # 출력 지오메트리 타입: Polygon
            source.sourceCrs()                  # 입력 레이어의 CRS 사용
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # 4. 진행률 보고를 위한 설정
        total_features = source.featureCount()
        if total_features == 0:
            return {self.OUTPUT: dest_id} # 피처가 없으면 빈 레이어 반환

        total_steps = 100.0 / total_features

        # 5. 피처 반복 처리 및 버퍼 생성 로직
        features = source.getFeatures()

        for current_feature_index, feature in enumerate(features):
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            previous_buffer = None # 각 입력 피처마다 이전 버퍼 초기화

            # 각 거리 값에 대해 버퍼 생성
            for index, rind_distance in enumerate(distance_values):
                # 5-1. 버퍼 지오메트리 생성
                # 세그먼트 수 24 (기본값)를 사용하여 부드러운 원형 버퍼 생성
                current_buffer = geometry.buffer(rind_distance, 24)

                # 5-2. 새 피처 생성 및 지오메트리 설정
                new_feature = QgsFeature()

                if outside_only and index > 0:
                    # 'Outside Only' 모드이고 첫 번째 버퍼가 아닌 경우:
                    # 현재 버퍼(큰 버퍼)에서 바로 이전 버퍼(작은 버퍼)를 뺀 차이(Difference) 계산
                    if previous_buffer is not None and previous_buffer.isEmpty():
                        new_geometry = current_buffer.difference(previous_buffer)
                        new_feature.setGeometry(new_geometry)
                    else:
                        # 로직상 오류 발생 가능성 낮으나, 이전 버퍼가 유효하지 않으면 현재 버퍼를 사용
                        new_feature.setGeometry(current_buffer)
                        feedback.pushWarning(self.tr("Could not calculate difference for ring (index {}). Outputting full buffer.").format(index))
                else:
                    # 'Outside Only'가 False이거나 첫 번째 버퍼인 경우:
                    # 일반 버퍼 지오메트리 그대로 사용 (중첩된 폴리곤)
                    new_feature.setGeometry(current_buffer)

                # 5-3. 속성 설정
                # 입력 피처의 속성을 그대로 복사
                new_attributes = feature.attributes()
                # 마지막에 버퍼 거리 (rind_distance) 속성을 추가
                new_attributes.append(rind_distance)
                new_feature.setAttributes(new_attributes)

                # 5-4. 싱크에 새 피처 추가
                sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
                
                # 다음 루프를 위해 현재 버퍼를 이전 버퍼로 저장
                previous_buffer = current_buffer

            # 진행률 업데이트
            feedback.setProgress(int(current_feature_index * total_steps))

        # 6. 결과 반환
        return {self.OUTPUT: dest_id}