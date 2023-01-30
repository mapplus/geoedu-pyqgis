# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Add shapefiles to map
Description          : Add shapefiles to map
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
    loader = Loader(iface)
    
    # replace your shapefile folder
    loader.load_shapefiles('C:/OSGeo_Edu/data/seoul')
    
class Loader:
    def __init__(self, iface):
        # initialize using the qgis.utils.iface object.
        self.iface = iface
        
    def load_shapefiles(self, shp_path):
        # Load all shapefiles found in shp_path
        # path.join = join one or more path components intelligently.
        print("Loading shapes from %s" % path.join(shp_path, "*.shp"))
        
        # set encoding
        settings = QSettings()
        settings.setValue("/UI/encoding", "EUC-KR")
        
        # glob = finds all the pathnames matching a specified pattern according to the rules
        shapefiles = glob(path.join(shp_path, "*.shp"))
        layer_count = 0
        for shp in shapefiles:
            # split the pathname path into a pair, (head, tail) 
            # where tail is the last pathname component and head is everything leading up to that.
            (shpdir, shpfile) = path.split(shp)
            
            # split the pathname path into a pair (root, ext) such that root + ext == path
            (filename, ext) = path.splitext(shpfile)
            
            # add vector layer to canvas using ogr driver
			# http://qgis.org/api/classQgisInterface.html
            self.iface.addVectorLayer(shp, filename, "ogr" )
            
            # 5 layers only
            layer_count += 1
            if layer_count == 5:
                break
            
        QMessageBox.information(self.iface.mainWindow(), "Information", "completed")
