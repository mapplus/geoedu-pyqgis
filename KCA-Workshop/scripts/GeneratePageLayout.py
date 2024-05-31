# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Generate PageLayout Algorithm
Description          : 출력 레이아웃 작성하기.
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
import os
from qgis.PyQt.QtCore import (Qt, QCoreApplication)
from qgis.PyQt.QtGui import (QColor, QFont)
from qgis.core import (QgsApplication,
                       QgsLayoutItem,
                       QgsLayoutItemMap,
                       QgsLayoutItemLabel,
                       QgsLayoutItemLegend,
                       QgsLayoutItemPicture,
                       QgsLayoutItemPage,
                       QgsLayoutItemScaleBar,
                       QgsLayoutMeasurement,
                       QgsLayoutPoint,
                       QgsLayoutSize,
                       QgsLegendStyle,
                       QgsPrintLayout,
                       QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingOutputString,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterVectorLayer,
                       QgsProject,
                       QgsPrintLayout,
                       QgsSymbol,
                       QgsStyle,
                       QgsUnitTypes,
                       QgsWkbTypes)
from qgis.utils import iface

class GeneratePageLayoutAlgorithm(QgsProcessingAlgorithm):

    LAYOUT_NAME = 'LAYOUT_NAME'
    TITLE = 'TITLE'
    LEGEND = 'LEGEND'
    SCALEBAR = 'SCALEBAR'
    NORTHARROW = 'NORTHARROW'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GeneratePageLayoutAlgorithm()

    def name(self):
        return 'GeneratePageLayoutAlgorithm'.lower()

    def displayName(self):
        return self.tr('출력 레이아웃 작성하기')

    def group(self):
        return self.tr('한국지도학회')

    def groupId(self):
        return 'kcascripts'

    def shortHelpString(self):
        return self.tr('출력 레이아웃 작성하기')

    def initAlgorithm(self, config=None):
        project = QgsProject.instance()

        self.addParameter(QgsProcessingParameterString(self.LAYOUT_NAME, self.tr('레이아웃 이름'),
                            defaultValue=project.baseName(), multiLine=False))

        self.addParameter(QgsProcessingParameterString(self.TITLE, self.tr('지도 제목'),
                            defaultValue='지도 제목', multiLine=False))

        self.addParameter(QgsProcessingParameterBoolean(self.LEGEND, self.tr('범례'),
                                                        defaultValue=True, optional=True))

        self.addParameter(QgsProcessingParameterBoolean(self.SCALEBAR, self.tr('축척 막대'),
                                                        defaultValue=True, optional=True))

        self.addParameter(QgsProcessingParameterBoolean(self.NORTHARROW, self.tr('방위표시'),
                                                        defaultValue=True, optional=True))

        self.addOutput(QgsProcessingOutputString(self.OUTPUT, self.tr('레이아웃')))

    def processAlgorithm(self, parameters, context, feedback):
        project = QgsProject.instance()
        canvas = iface.mapCanvas()

        layout_name = self.parameterAsString(parameters, self.LAYOUT_NAME, context)
        title = self.parameterAsString(parameters, self.TITLE, context)

        legend = self.parameterAsBool(parameters, self.LEGEND, context)
        scalebar = self.parameterAsBool(parameters, self.SCALEBAR, context)
        north_arrow = self.parameterAsBool(parameters, self.NORTHARROW, context)

        layout_name = project.baseName() if layout_name is None else layout_name
        title = project.baseName() if title is None else title

        manager = project.layoutManager()
        layout =  manager.layoutByName(layout_name)
        if layout is not None:
            feedback.pushInfo(f'{layout_name} 레이아웃이 이미 있습니다.')
            return {self.OUTPUT: None}

        # create a new layout
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        layout.setName(layout_name)
        manager.addLayout(layout)

        # Add A Map Frame to Layout
        map = self.add_default_map(layout, canvas)

        # Add Map Title
        if title and len(title) > 0:
            self.add_title(layout, title)

        # Add Scale Bar
        if scalebar:
            self.add_scalebar(layout, map, canvas.scale())

        # Add Map Legend
        if legend:
            self.add_legend(layout, map)

        # Add North Arrow
        if north_arrow:
            self.add_northarrow(layout)

        return {self.OUTPUT: layout_name}

    def add_default_map(self, layout, canvas):
        # Create a QgsLayoutItemMap
        map_item = QgsLayoutItemMap(layout)

        # Set legend frame properties
        map_item.setFrameEnabled(True)  # Activate the border
        map_item.setFrameStrokeColor(QColor('gray'))  # Set the color
        map_item.setFrameStrokeWidth(QgsLayoutMeasurement(0.1, QgsUnitTypes.LayoutMillimeters))  # Specify width of the border

        # Set the initial position and size
        map_item.setRect(10, 10, 10, 10)

        # Zoom the map to the extent of the canvas
        map_item.zoomToExtent(canvas.extent())

        # Set a unique ID for the map item
        map_item.setId('map')

        # Add the map item to the layout
        layout.addLayoutItem(map_item)

        # Attempt to move and resize the map item
        map_item.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
        map_item.attemptResize(QgsLayoutSize(285, 180, QgsUnitTypes.LayoutMillimeters))

        return map_item

    def add_title(self, layout, mapTitle):
        if not mapTitle:
            return None  # Return None if mapTitle is None or an empty string

        # Create a QgsLayoutItemLabel for the title
        title = QgsLayoutItemLabel(layout)
        title.setText(mapTitle)

        # Set font properties
        title.setFont(QFont('맑은 고딕', 28, QFont.Bold))

        # Set horizontal alignment to center
        title.setReferencePoint(QgsLayoutItem.UpperLeft)
        title.setHAlign(Qt.AlignCenter)

        # Set a unique ID for the title item
        title.setId('title')

        # Add the title item to the layout
        layout.addLayoutItem(title)

        # Adjust the size of the title item to fit the text
        title.adjustSizeToText()

        # Move and resize the title item
        title.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))
        title.attemptResize(QgsLayoutSize(285, 13, QgsUnitTypes.LayoutMillimeters))
        title.refresh()

        return title

    def add_scalebar(self, layout, map, scale):
        # Create a QgsLayoutItemScaleBar
        scalebar = QgsLayoutItemScaleBar(layout)
        scalebar.setStyle('Single Box')
        scalebar.setLinkedMap(map)
        scalebar.setId('scalebar')

        # Set properties for the scale bar
        scalebar.setNumberOfSegments(2)
        scalebar.setUnitsPerSegment(1.0)
        scalebar.setMapUnitsPerScaleBarUnit(1.0)

        # Guess the units and set properties accordingly
        guess_units = scalebar.guessUnits()
        unit_label = 'm' if guess_units == QgsUnitTypes.DistanceMeters else 'km'
        scalebar.applyDefaultSize(guess_units)
        scalebar.setUnits(guess_units)
        scalebar.setUnitLabel(unit_label)

        # Set font and color properties
        scalebar.setFont(QFont('맑은 고딕', 12))
        scalebar.setFontColor(QColor('Black'))
        scalebar.setFillColor(QColor('Black'))

        # Update the scale bar
        scalebar.update()

        # Add the scale bar to the layout
        layout.addLayoutItem(scalebar)

        # Move and resize the scale bar
        scalebar.attemptMove(QgsLayoutPoint(5, 182, QgsUnitTypes.LayoutMillimeters))
        scalebar.attemptResize(QgsLayoutSize(65, 15, QgsUnitTypes.LayoutPixels))

        return scalebar

    def add_northarrow(self, layout):
        # Create a QgsLayoutItemPicture for the north arrow
        north_arrow = QgsLayoutItemPicture(layout)
        north_arrow.setMode(QgsLayoutItemPicture.FormatSVG)
        north_arrow.setId('north_arrow')

        # Set the path to the SVG file
        svg_paths = QgsApplication.svgPaths()
        for svg_path in svg_paths:
            path = os.path.join(svg_path, 'arrows', 'NorthArrow_06.svg')
            if os.path.exists(path):
                north_arrow.setPicturePath(path)
                break

        # Add the north arrow to the layout
        layout.addLayoutItem(north_arrow)

        # Move and resize the north arrow
        north_arrow.attemptMove(QgsLayoutPoint(270, 22, QgsUnitTypes.LayoutMillimeters))
        north_arrow.attemptResize(QgsLayoutSize(195, 211, QgsUnitTypes.LayoutPixels))

        return north_arrow

    def add_legend(self, layout, map, auto_update=True):
        """
        Add a legend to the layout.

        :param layout: QgsPrintLayout
        :param map: QgsLayoutItemMap (linked map)
        :param auto_update: Whether to automatically update the legend based on the linked map
        :return: QgsLayoutItemLegend
        """
        # Create a QgsLayoutItemLegend for the legend
        legend = QgsLayoutItemLegend(layout)

        # Set legend frame properties
        legend.setFrameEnabled(True)  # Activate the border
        legend.setFrameStrokeColor(QColor('gray'))  # Set the color
        legend.setFrameStrokeWidth(QgsLayoutMeasurement(0.1, QgsUnitTypes.LayoutMillimeters))  # Specify width of the border

        # Set font properties for the legend
        legend.setStyleFont(QgsLegendStyle.Title, QFont('맑은 고딕', 12, QFont.Bold))
        legend.setStyleFont(QgsLegendStyle.Group, QFont("맑은 고딕", 11, QFont.Bold))
        legend.setStyleFont(QgsLegendStyle.Subgroup, QFont('맑은 고딕', 10, QFont.Bold))
        legend.setStyleFont(QgsLegendStyle.Symbol, QFont("맑은 고딕", 8))
        legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont('맑은 고딕', 8))
        legend.setId('legend')

        if auto_update:
            # Link the legend to the map for automatic updates
            legend.setLinkedMap(map)
            legend.setAutoUpdateModel(True)
            legend.setLegendFilterByMapEnabled(True)
        else:
            # Manually update the legend based on visible vector layers in the current map
            legend.setAutoUpdateModel(False)
            root_group = legend.model().rootGroup()

            # Save the visibility status of layers
            visibility = {tree_layer.layer().name(): tree_layer.isVisible() for tree_layer in root_group.findLayers()}

            # Clear the legend and add visible vector layers
            root_group.clear()
            legend_available = False

            for layer in QgsProject.instance().mapLayers().values():
                if isinstance(layer, QgsVectorLayer) and visibility.get(layer.name(), False):
                    root_group.addLayer(layer)
                    legend_available = True

            if not legend_available:
                return None  # No legend available

        layout.addLayoutItem(legend)
        legend.setTitle('범례')
        legend.setResizeToContents(True)
        legend.adjustBoxSize()

        # Set legend position
        legend.attemptMove(QgsLayoutPoint(6, 21, QgsUnitTypes.LayoutMillimeters))

        # Update the legend
        legend.updateLegend()

        return legend
