# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                  : Graduated Color Renderer Algorithm
Description           : 단계구분도(Choropleth Map) 작성 알고리즘.
Date                  : 24/May/2024 (Refactored: 2025/12/04)
Copyright             : (C) 2024 by Minpa Lee (mapplus@gmail.com)
License               : GNU General Public License v2 or later
***************************************************************************/
"""

# 필요한 PyQt 및 QGIS 모듈 임포트
from PyQt5.QtCore import (Qt, QCoreApplication)
from PyQt5.QtGui import (QColor) # QFont는 사용되지 않아 제거
from qgis.core import (QgsProcessing,
                        QgsClassificationEqualInterval,
                        QgsClassificationQuantile,
                        QgsClassificationJenks,
                        QgsClassificationStandardDeviation,
                        QgsClassificationPrettyBreaks,
                        QgsSimpleFillSymbolLayer,
                        QgsGraduatedSymbolRenderer,
                        QgsProcessingException,
                        QgsProcessingAlgorithm,
                        QgsProcessingParameterField,
                        QgsProcessingParameterString,
                        QgsProcessingParameterNumber,
                        QgsProcessingParameterEnum,
                        QgsProcessingParameterBoolean,
                        QgsProcessingParameterVectorLayer,
                        QgsProcessingOutputVectorLayer,
                        QgsRendererRangeLabelFormat,
                        QgsSymbol,
                        QgsStyle,
                        QgsWkbTypes)


class GraduatedColorRendererAlgorithm(QgsProcessingAlgorithm):
    """
    입력 벡터 레이어의 수치 필드를 기반으로
    단계구분 심볼 렌더러(Graduated Symbol Renderer)를 적용하는 QGIS Processing 알고리즘.
    """
    # --- 파라미터 상수 정의 ---
    INPUT = 'INPUT'         # 입력 레이어
    FIELD = 'FIELD'         # 분류에 사용할 필드
    METHOD = 'METHOD'       # 분류 방법 (급간 설정)
    CLASS = 'CLASS'         # 급간 수
    RAMP = 'RAMP'           # 색상표 이름
    OUTPUT = 'OUTPUT'       # 출력 (적용된 레이어)

    # 급간 분류 방법 목록 정의 (Enum 파라미터에 사용)
    CLASS_METHODS = ['Equal Interval (등간격)', 'Quantile (분위)', 'Jenks (자연적 구분)', 'Standard Deviation (표준편차)', 'Pretty Breaks (예쁜 구분)']

    # QGIS 스타일에 등록된 기본 색상표 이름 목록을 가져옴
    RAMPS = QgsStyle().defaultStyle().colorRampNames()

    def tr(self, string):
        """
        문자열을 번역 가능하도록 처리하는 함수 (다국어 지원).
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """
        알고리즘 인스턴스를 반환하여 프레임워크가 알고리즘을 로드할 수 있도록 함.
        """
        return GraduatedColorRendererAlgorithm()

    def name(self):
        """
        알고리즘의 고유한 내부 이름.
        """
        return 'graduatedcolorrenderer' # 소문자 사용

    def displayName(self):
        """
        QGIS 툴박스에 표시될 알고리즘 이름.
        """
        return self.tr('단계구분도 작성하기 (Graduated Color)')


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
        return self.tr('선택한 레이어의 수치 필드를 기반으로 다양한 분류 방법을 적용하여 단계구분도 렌더러를 설정합니다.')

    def initAlgorithm(self, config=None):
        """
        알고리즘의 입력 및 출력 파라미터를 정의.
        """
        # 1. 입력 벡터 레이어 파라미터 정의 (모든 벡터 타입 허용)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('입력 벡터 레이어 (Input Layer)'),
                types=[QgsProcessing.TypeVectorPolygon]
            )
        )

        # 2. 분류에 사용할 필드 파라미터 정의 (숫자 필드만 허용)
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                self.tr('분류 기준 필드 (Numeric Field)'),
                type=QgsProcessingParameterField.Numeric,
                parentLayerParameterName=self.INPUT # 이 파라미터는 INPUT 레이어에 종속됨
            )
        )

        # 3. 단계 구분 방법 파라미터 정의 (Enum, 기본값: Jenks)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD,
                self.tr('단계 구분 방법 (Classification Method)'),
                self.CLASS_METHODS,
                defaultValue=2, # Jenks (자연적 구분)
                optional=False
            )
        )

        # 4. 급간 수 파라미터 정의 (정수, 최소 3개, 최대 10개)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLASS,
                self.tr('급간 수 (Number of Classes)'),
                defaultValue=5,
                minValue=3,
                maxValue=10,
                type=QgsProcessingParameterNumber.Integer,
                optional=False
            )
        )

        # 5. 색상표 파라미터 정의 (Enum, QGIS 등록된 색상표 목록 사용)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.RAMP,
                self.tr('색상표 (Color Ramp)'),
                self.RAMPS,
                defaultValue=0, # 목록의 첫 번째 항목을 기본값으로 사용
                optional=False
            )
        )

        # 6. 출력 레이어 정의 (입력 레이어에 렌더러를 적용하는 결과를 반환)
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT, self.tr('렌더링 적용된 레이어')))


    def processAlgorithm(self, parameters, context, feedback):
        """
        알고리즘의 실제 처리 로직: 입력 레이어에 단계구분 렌더러를 적용.
        """
        # 1. 파라미터 값 가져오기
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        field = self.parameterAsString(parameters, self.FIELD, context)
        classes = self.parameterAsInt(parameters, self.CLASS, context)
        method_enum = self.parameterAsEnum(parameters, self.METHOD, context)
        ramp_enum = self.parameterAsEnum(parameters, self.RAMP, context)

        if layer is None:
            raise QgsProcessingException(self.tr('입력 레이어를 찾을 수 없습니다.'))

        # 2. 분류 방법 객체 매핑
        # QgsProcessingParameterEnum의 인덱스를 QgsClassificationMethod 객체와 연결
        if method_enum == 0:
            method = QgsClassificationEqualInterval()
        elif method_enum == 1:
            method = QgsClassificationQuantile()
        elif method_enum == 2:
            method = QgsClassificationJenks()
        elif method_enum == 3:
            method = QgsClassificationStandardDeviation()
        elif method_enum == 4:
            method = QgsClassificationPrettyBreaks()
        else:
            # 기본값 또는 오류 발생 시 Jenks 사용 (이미 Enum 파라미터에서 처리되지만 안전을 위해)
            method = QgsClassificationJenks()

        # 3. 선택된 색상표 이름 가져오기
        brewer_ramp = self.RAMPS[ramp_enum]

        # 4. 핵심 렌더러 적용 함수 호출
        self.set_graduated_symbol_renderer(layer, field, method, classes, brewer_ramp)

        # 5. 결과 반환 (렌더러가 적용된 입력 레이어를 반환)
        return {self.OUTPUT: parameters[self.INPUT]}


    def set_graduated_symbol_renderer(self, layer, field, method, classes, brewer_ramp, template_symbol=None):
        """
        지정된 레이어에 단계구분 심볼 렌더러를 설정하는 내부 도우미 함수.
        """
        geometryType = layer.geometryType()

        # 1. 템플릿 심볼 생성 및 설정
        if template_symbol is None:
            # 기본 심볼을 생성하고 투명도를 설정
            template_symbol = QgsSymbol.defaultSymbol(geometryType)
            template_symbol.setOpacity(1.0)

            if geometryType == QgsWkbTypes.PolygonGeometry:
                # 폴리곤 레이어의 경우, 경계를 회색으로 설정하여 급간 경계를 명확히 함
                symbolLayer = QgsSimpleFillSymbolLayer()
                symbolLayer.setStrokeColor(QColor('#a0a0a4'))  # 회색 (gray)
                symbolLayer.setStrokeWidth(0.1)
                symbolLayer.setStrokeStyle(Qt.SolidLine)
                # 기본 심볼의 첫 번째 레이어를 새로 만든 심볼 레이어로 교체
                template_symbol.changeSymbolLayer(0, symbolLayer)

        # 2. 라벨 포맷 설정
        label_format = QgsRendererRangeLabelFormat()
        label_format.setFormat("%1 - %2")          # 라벨 형식: Min - Max
        label_format.setPrecision(2)               # 소수점 정밀도 2자리
        label_format.setTrimTrailingZeroes(True)   # 끝에 붙는 0 제거

        # 3. 색상표 객체 가져오기
        defaultStyle = QgsStyle().defaultStyle()
        colorRamp = defaultStyle.colorRamp(brewer_ramp)

        # 4. QgsGraduatedSymbolRenderer 객체 생성 및 설정
        renderer = QgsGraduatedSymbolRenderer()
        renderer.setSourceSymbol(template_symbol)  # 템플릿 심볼 설정
        renderer.setLabelFormat(label_format)      # 라벨 포맷 설정
        renderer.setClassAttribute(field)          # 분류 기준 필드 설정
        renderer.setClassificationMethod(method)   # 분류 방법 객체 설정

        # 5. 급간 계산 및 색상 적용
        # 레이어의 데이터를 기반으로 지정된 급간 수(classes)에 맞게 분류 범위(Ranges) 계산
        renderer.updateClasses(layer, classes)
        # 계산된 분류 범위에 지정된 색상표(colorRamp) 적용
        renderer.updateColorRamp(colorRamp)

        # 6. 렌더러 적용 및 레이어 갱신
        layer.setRenderer(renderer)
        layer.triggerRepaint() # 변경 사항이 맵 캔버스에 즉시 반영되도록 강제 갱신