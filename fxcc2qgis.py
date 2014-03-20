#!/usr/bin/python
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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from fxcc2qgisdialog import fxcc2QgisDialog
import os.path


import codecs



try:
	from osgeo import ogr
except:
	import ogr


class fxcc2Qgis:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'fxcc2qgis_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = fxcc2QgisDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/fxcc2qgis/icon.png"),
            u"fxcc2Qgis", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&fxcc2Qgis", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&fxcc2Qgis", self.action)
        self.iface.removeToolBarIcon(self.action)


    def generaCapaParcela(self, dxfs_parcela):

        #Creamos la capa en memoria
        ml = QgsVectorLayer("Polygon", "PARCELA", "memory")
        pr = ml.dataProvider()
        #Creamos los campos de la capa
        pr.addAttributes( [ QgsField("refcat", QVariant.String) ] )
        pr.addAttributes( [ QgsField("cod_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("sg_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("nombre_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num", QVariant.String) ] )
        pr.addAttributes( [ QgsField("dup", QVariant.String) ] )
        pr.addAttributes( [ QgsField("anio_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("entidad_exp", QVariant.String) ] )
        ml.updateFields()

        for parcela in dxfs_parcela:
            try:
                print "Generando la capa parcela de la referencia: " + parcela
                featuresExternas = dxfs_parcela[parcela][0]
                datos_asc = dxfs_parcela[parcela][1]
                #Procesamos las features del dxf (lineas) y las unimos en una única geometría      
                geometry_out = None
                for feature in featuresExternas:
                    geometry_in = feature.GetGeometryRef()
                    if geometry_out is None:
                        geometry_out = geometry_in
                        geometry_out = ogr.ForceToMultiLineString(geometry_out)
                    else:
                        geometry_out = geometry_out.Union(geometry_in)

                #Convertimos la geometría de tipo linea en polígono
                geometryPoly = ogr.BuildPolygonFromEdges(geometry_out, dfTolerance = 0)
                geometryPolyWkt = geometryPoly.ExportToWkt()

                #Generamos la lista que contendrá los atributos de la feature
                atributos = []
                atributos.append(parcela)
                atributos.extend(datos_asc)

                #Creamos la feature y le seteamos la geometría y sus atributos
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromWkt(geometryPolyWkt))
                fet.setAttributes(atributos)
                
                #Añadimos la feature al data provider
                pr.addFeatures([fet])
            except:
                print u"Se encontró algún error generando la parcela " + parcela

        ml.updateExtents()
        ml.loadNamedStyle(self.plugin_dir + '/styles/parcela.qml')

        QgsMapLayerRegistry.instance().addMapLayer(ml)


    def generaCapaConstruccion(self):

        #Creamos la capa de memoria
        ml = QgsVectorLayer("Polygon", "CONTRUCCION", "memory")
        pr = ml.dataProvider()
        #Creamos los campos de la capa
        pr.addAttributes( [ QgsField("refcat", QVariant.String) ] )
        pr.addAttributes( [ QgsField("cod_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("sg_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("nombre_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num", QVariant.String) ] )
        pr.addAttributes( [ QgsField("dup", QVariant.String) ] )
        pr.addAttributes( [ QgsField("altura", QVariant.String) ] )
        pr.addAttributes( [ QgsField("anio_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("entidad_exp", QVariant.String) ] )
        ml.updateFields()

        pass


    def procesaAsc(self, fichero):

        infile = open(fichero, 'r')
        lineas = infile.readlines()
        cod_via = lineas[4].replace("\n", "")
        sg_via = lineas[5].replace("\n", "")
        nombre_via = lineas[6].replace("\n", "")
        num = lineas[7].replace("\n", "")
        dup = lineas[8].replace("\n", "")

        try:
            linea_exp = lineas.index("EXPEDIENTE\n")
            anoExp = lineas[linea_exp + 1].replace("\n", "")
            numExp = lineas[linea_exp + 2].replace("\n", "")
            entExp = lineas[linea_exp + 3].replace("\n", "")
        except:
            print "El FXCC no tiene expediente asociado."
            anoExp = "0"
            numExp = "0"
            entExp = "0"

        return [cod_via, sg_via, nombre_via, num, dup, anoExp, numExp, entExp]

        infile.close()


    def procesaDxf(self, ficheros):
        #probando la carga de fxcc

        dxfs_parcela = {}
        dxfs_constru = {}

        #Pasamos a procesar los dxf uno a uno
        for dxf in ficheros:
            nombreDxf = os.path.splitext(os.path.basename(dxf))[0]
            print "Se selecciona el fichero: " + dxf
            print "Referencia catastral: " + nombreDxf

            driverIn = ogr.GetDriverByName('DXF')
            dataSource = driverIn.Open(dxf, 0)
            dataSource.ExecuteSQL("SELECT * FROM entities WHERE Layer = 'PG-LP'")

            layerIn = dataSource.GetLayer()
            totalRegistros = layerIn.GetFeatureCount()
            print "Total registros: " + str(totalRegistros)
            layerIn.ResetReading()
            inFeature = layerIn.GetNextFeature()
            #print "1"

            #Recolectamos las features del dxf para poder procesarlas más adelante
            featuresExternas = []
            featuresInternas = []
            featuresCentroide = []
            outFeature = []
            cnt = 0
            while inFeature:
                #print "2"
                nombreCapa = inFeature.GetFieldAsString('Layer')
                if nombreCapa == 'PG-LP':
                    featuresExternas.append(inFeature)
                elif nombreCapa == 'PG-LI':
                    featuresInternas.append(inFeature)
                elif nombreCapa == 'PG-AA':
                    featuresCentroide.append(inFeature)
                
                cnt = cnt + 1
                if cnt < totalRegistros: 
                    inFeature = layerIn.GetNextFeature()
                else:
                    break
            
            #Procesamos el fichero alfanumérico
            asc = dxf.replace(".dxf", ".asc")
            datos_asc = self.procesaAsc(asc)

            #Mandamos las features del dxf a la funcion que le toque
            #self.generaCapaParcela(nombreDxf, featuresExternas, datos_asc)
            #self.generaCapaConstruccion(featuresInternas)

            dxfs_parcela[nombreDxf] = (featuresExternas, datos_asc)
            #dxfs_constru[nombreDxf] = ()

            
        self.generaCapaParcela(dxfs_parcela)


    def buscaDxf(self, baseDir):

        matches = []
        for root, dirnames, filenames in os.walk(baseDir):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.dxf':
                    matches.append(os.path.join(root, filename))
        return matches

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        read_path = "." 
        file = unicode(QFileDialog.getExistingDirectory(self.iface.mainWindow(), "Seleccione con FXCC a importar"))
        file
        #file = str(unicode(QFileDialog.getExistingDirectory(self.iface.mainWindow(), "Select con FXCC a importar"), "utf-8"))
        print "Se selecciona el directorio: " + file

        ficheros = self.buscaDxf(file)

        self.procesaDxf(ficheros)
        #self.prueba()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
			
	