# -*- coding: utf-8 -*-
"""
/***************************************************************************
 fxcc2Qgis
                                 A QGIS plugin
 prueba
                             -------------------
        begin                : 2014-02-25
        copyright            : (C) 2014 by Francisco Pérez Sampayo
        email                : fpsampayo@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load fxcc2Qgis class from file fxcc2Qgis
    from fxcc2qgis import fxcc2Qgis
    return fxcc2Qgis(iface)
