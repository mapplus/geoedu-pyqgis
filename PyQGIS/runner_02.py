# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Features to point
Description          : Features to point
Date                 : 29/Jan/2013
copyright            : (C) 2013 by MapPlus
email                : mapplus@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

from glob import glob
from os import path

def run_script(iface):
    process = FeaturesToPoint(iface)
    
    # get layer
    # TOC에 admin_emd 레이어가 추가 되어 있어야 함
    inputlayer = Utilities.getLayer("admin_emd")
    if inputlayer is None:
        QMessageBox.information(iface.mainWindow(), "Information", "cannot find specified layer")
        return
    
    # execute process
    outputlayer = process.execute(inputlayer, "C:/OSGeo_Edu/data/seoul/admin_emd_point.shp")
    
    # add layer
    if outputlayer:
        QgsProject.instance().addMapLayer(outputlayer)
        QMessageBox.information(iface.mainWindow(), "Information", "feature to point process completed!")
    else:
        QMessageBox.information(iface.mainWindow(), "Error", "failed!")
        
class Utilities(object):
    """
    Utilities for QGIS Objects
    """
    @staticmethod
    def getLayer(layerName):
        # http://qgis.org/api/classQgsMapLayerRegistry.html
        allLayers = QgsProject.instance().mapLayers()
        for name, layer in allLayers.items():
            if layer.name() == layerName:
                if layer.isValid():
                    return layer
                else:
                    return None
        return None
    
    @staticmethod
    def getFolder(file):
        (shpdir, shpfile) = path.split(file)
        return shpdir
    
    @staticmethod
    def getFileNameWithoutExt(file):
        (shpdir, shpfile) = path.split(file)
        (filename, ext) = path.splitext(shpfile)
        return filename
        
class FeaturesToPoint:
    
    def __init__(self, iface):
        # initialize using the qgis.utils.iface object.
        self.iface = iface
    
    def execute(self, inputlayer, outputPath):
        provider = inputlayer.dataProvider()
        encoding = provider.encoding()      # "EUC-KR"
        
        # http://qgis.org/api/classQgsVectorFileWriter.html("ESRI Shapefile" Parameter Value 지정하지 않으면 Default : GPKG(지오패키지)로 생성)
        writer = QgsVectorFileWriter(outputPath, encoding, provider.fields(), QgsWkbTypes.Point, provider.crs(), "ESRI Shapefile")
                
        output_feature = QgsFeature()
        
        features = inputlayer.getFeatures()
        for input_feature in features:
            input_geometry = input_feature.geometry()
            attributes = input_feature.attributes()

            centroid = input_geometry.centroid()
            if centroid:
                output_feature.setGeometry(centroid)
                output_feature.setAttributes(attributes)
                writer.addFeature(output_feature)

        del writer
        
        layerName = Utilities.getFileNameWithoutExt(outputPath)

        return QgsVectorLayer(outputPath, layerName, "ogr")
