# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Graduated Color Renderer Algorithm
Description          : 단계구분도 작성.
Date                 : 24/May/2024
copyright            : (C) 2024 by Minpa Lee
email                : mapplus@gmail.com
reference:
***************************************************************************/

***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import (Qt, QCoreApplication)
from qgis.PyQt.QtGui import (QColor, QFont)
from qgis.core import (QgsProcessing,
                       QgsClassificationEqualInterval,
                       QgsClassificationQuantile,
                       QgsClassificationJenks,
                       QgsClassificationStandardDeviation,
                       QgsClassificationPrettyBreaks,
                       QgsClassificationLogarithmic,
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
                       QgsProcessingParameterBand,
                       QgsProcessingParameterRasterDestination,
                       QgsRendererRangeLabelFormat,
                       QgsSymbol,
                       QgsStyle,
                       QgsWkbTypes)


class GraduatedColorRendererAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    FIELD = 'FIELD'
    METHOD = 'METHOD'
    CLASS = 'CLASS'
    RAMP = 'RAMP'
    OUTPUT = 'OUTPUT'

    CLASS_METHODS = ['Equal Interval', 'Quantile', 'Jenks', 'Standard Deviation', 'Pretty Breaks']
    RAMPS = QgsStyle().defaultStyle().colorRampNames()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GraduatedColorRendererAlgorithm()

    def name(self):
        return 'GraduatedColorRendererAlgorithm'.lower()

    def displayName(self):
        return self.tr('단계구분도 작성하기')

    def group(self):
        return self.tr('한국지도학회')

    def groupId(self):
        return 'kcascripts'

    def shortHelpString(self):
        return self.tr('단계구분도 작성하기')

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(self.INPUT, self.tr('폴리곤 레이어'),
                          types=[QgsProcessing.TypeVector]))

        self.addParameter(QgsProcessingParameterField(self.FIELD,
                                                      self.tr('필드 선택'),
                                                      type=QgsProcessingParameterField.Numeric,
                                                      parentLayerParameterName=self.INPUT))

        self.addParameter(QgsProcessingParameterEnum(self.METHOD, self.tr('단계구분방법'),
                                                    self.CLASS_METHODS, defaultValue=2, optional=False))

        self.addParameter(QgsProcessingParameterNumber(self.CLASS, self.tr('급간'),
                                defaultValue=5, minValue=3, maxValue=10, type=QgsProcessingParameterNumber.Integer,
                                                           optional=False))

        self.addParameter(QgsProcessingParameterEnum(self.RAMP, self.tr('색상표'),
                self.RAMPS, defaultValue=0, optional=False))

        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT, self.tr('적용')))

    def processAlgorithm(self, parameters, context, feedback):
        # 파라미터
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        field = self.parameterAsString(parameters, self.FIELD, context)
        classes = self.parameterAsInt(parameters, self.CLASS, context)

        method_enum = self.parameterAsEnum(parameters, self.METHOD, context)
        if method_enum == 0:
            method = QgsClassificationEqualInterval()
        elif method_enum == 1:
            method = QgsClassificationQuantile()
        elif method_enum == 2:
            method = QgsClassificationJenks()
        elif method_enum == 3:
            method = QgsClassificationStandardDeviation()
        elif method_enum == 3:
            method = QgsClassificationPrettyBreaks()

        ramp_enum = self.parameterAsEnum(parameters, self.RAMP, context)
        brewer_ramp = self.RAMPS[ramp_enum]

        # 단계구분도 적용
        self.set_graduated_symbol_renderer(layer, field, method, classes, brewer_ramp)

        return {self.OUTPUT: parameters[self.INPUT]}

    def set_graduated_symbol_renderer(self, layer, field, method=QgsClassificationJenks(),
                       classes=5, brewer_ramp='YlOrRd', template_symbol=None):
        geometryType = layer.geometryType()

        if template_symbol is None:
            template_symbol = QgsSymbol.defaultSymbol(geometryType)
            template_symbol.setOpacity(1.0) # default
            if geometryType == QgsWkbTypes.PolygonGeometry:
                # set stroke color to white for polygon type
                symbolLayer = QgsSimpleFillSymbolLayer()
                symbolLayer.setStrokeColor(QColor('#a0a0a4'))  # gray
                symbolLayer.setStrokeWidth(0.1)
                symbolLayer.setStrokeStyle(Qt.SolidLine)
                template_symbol.changeSymbolLayer(0, symbolLayer)

        # label format
        labelFormat = QgsRendererRangeLabelFormat()
        labelFormat.setFormat("%1 - %2")        # default
        labelFormat.setPrecision(2)             # default
        labelFormat.setTrimTrailingZeroes(True) # default

        # default ramp
        defaultStyle = QgsStyle().defaultStyle()
        colorRamp = defaultStyle.colorRamp(brewer_ramp)

        if method is None:
            method = QgsClassificationEqualInterval() # default

        # create renderer
        renderer = QgsGraduatedSymbolRenderer()
        renderer.setSourceSymbol(symbol)
        renderer.setLabelFormat(labelFormat) # deprecated
        renderer.setClassAttribute(field)
        renderer.setClassificationMethod(method)
        renderer.updateClasses(layer, classes)
        renderer.updateColorRamp(colorRamp)

        # apply renderer to layer and refresh
        layer.setRenderer(renderer)
        layer.triggerRepaint()
