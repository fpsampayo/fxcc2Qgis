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
from qgis._core import QgsVectorLayer
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from gui.fxcc2qgisdialog import fxcc2QgisDialog
import os.path
import re

try:
    from shapely.wkt import dumps, loads
    from shapely.ops import polygonize
except:
    print "Este plugin necesita el módulo Shapely para poder funcionar."

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


        QObject.connect(self.dlg.btnSeleccionarRuta, SIGNAL("clicked()"), self.dlg.seleccionaDirectorio)
        QObject.connect(self.dlg.btnSeleccionarCrs, SIGNAL("clicked()"), self.dlg.seleccionaCrs)
        QObject.connect(self.dlg.buttonBox, SIGNAL("accepted()"), self.dlg.validateFields)

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
                #print "Generando la capa parcela de la referencia: " + parcela
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
                pass
                #print u"Se encontró algún error generando la parcela " + parcela

        ml.loadNamedStyle(self.plugin_dir + '/styles/parcela.qml')
        ml.setCrs(QgsCoordinateReferenceSystem(self.dlg.cmpCrs.text()))

        QgsMapLayerRegistry.instance().addMapLayer(ml)
        ml.updateExtents()


    def generaCapaConstru(self, dxfs_constru):

        #Creamos la capa de memoria
        ml = QgsVectorLayer("Polygon", "CONTRUCCION", "memory")
        pr = ml.dataProvider()
        #Creamos los campos de la capa
        pr.addAttributes( [ QgsField("refcat", QVariant.String) ] )
        pr.addAttributes( [ QgsField("rotulo", QVariant.String) ] )
        pr.addAttributes( [ QgsField("cod_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("sg_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("nombre_via", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num", QVariant.String) ] )
        pr.addAttributes( [ QgsField("dup", QVariant.String) ] )
        pr.addAttributes( [ QgsField("anio_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("num_exp", QVariant.String) ] )
        pr.addAttributes( [ QgsField("entidad_exp", QVariant.String) ] )
        ml.updateFields()

        for parcela in dxfs_constru:
            featuresExternas = dxfs_constru[parcela][0]
            featuresInternas = dxfs_constru[parcela][1]
            featuresCentroide = dxfs_constru[parcela][2]
            datos_asc = dxfs_constru[parcela][3]
            atributos = []
            centroides = []
            for centroide in featuresCentroide:
                punto = ogr.Geometry(type = 1)
                rotulo = centroide[0]
                x = centroide[1]
                y = centroide[2]
                punto.SetPoint(point = 0, x = float(x), y = float(y))

                centroides.append((rotulo, punto))

            featuresProceso = featuresExternas + featuresInternas

            features = []

            if len(featuresProceso) > 1:
                geometry_out = None
                for inFeature in featuresProceso:
                    geometry_in = inFeature.GetGeometryRef()
                    if geometry_out is None:
                        geometry_out = geometry_in
                        geometry_out = ogr.ForceToMultiLineString(geometry_out)
                    else:
                        geometry_out = geometry_out.Union(geometry_in)

                lineasInternasShapely = loads(geometry_out.ExportToWkt())
                polygonsShapely = polygonize(lineasInternasShapely)

                polygonGeom = []
                for polygon in polygonsShapely:
                    polygonGeom.append(ogr.CreateGeometryFromWkt(dumps(polygon)))

                for pol in polygonGeom:
                    for cen in centroides:
                        if pol.Contains(cen[1]):
                            geometryPolyWkt = pol.ExportToWkt()
                            fet = QgsFeature()
                            fet.setGeometry(QgsGeometry.fromWkt(geometryPolyWkt))
                            atributos = []
                            atributos.append(parcela)
                            atributos.append(cen[0])
                            atributos.extend(datos_asc)
                            fet.setAttributes(atributos)
                            features.append(fet)
            else:
                geometryPoly = ogr.BuildPolygonFromEdges(ogr.ForceToMultiLineString(featuresProceso[0].GetGeometryRef()), dfTolerance = 0)
                geometryPolyWkt = geometryPoly.ExportToWkt()
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromWkt(geometryPolyWkt))
                atributos.append(parcela)
                atributos.append(centroides[0][0])
                atributos.extend(datos_asc)
                fet.setAttributes(atributos)
                features.append(fet)

            pr.addFeatures(features)

        ml.loadNamedStyle(self.plugin_dir + '/styles/constru.qml')
        ml.setCrs(QgsCoordinateReferenceSystem(self.dlg.cmpCrs.text()))

        QgsMapLayerRegistry.instance().addMapLayer(ml)
        ml.updateExtents()


    def procesaAsc(self, fichero):

        try:
            inFile = open(fichero, 'r')
            lineas = inFile.read().splitlines()
            inFile.close()
        except:
            print "Error abriendo el fichero ASC"
            pass

        cod_via = lineas[4]
        sg_via = lineas[5]
        nombre_via = lineas[6]
        num = lineas[7]
        dup = lineas[8]

        try:
            linea_exp = lineas.index("EXPEDIENTE")
            anoExp = lineas[linea_exp + 1]
            numExp = lineas[linea_exp + 2]
            entExp = lineas[linea_exp + 3]
        except:
            #print "El FXCC no tiene expediente asociado."
            anoExp = "0"
            numExp = "0"
            entExp = "0"

        return [cod_via, sg_via, nombre_via, num, dup, anoExp, numExp, entExp]




    def procesaDxf(self, ficheros):
        #probando la carga de fxcc

        dxfs_parcela = {}
        dxfs_constru = {}

        #Pasamos a procesar los dxf uno a uno
        for dxf in ficheros:
            nombreDxf = os.path.splitext(os.path.basename(dxf))[0]
            #print "Se selecciona el fichero: " + unicode(dxf)
            #print "Referencia catastral: " + nombreDxf

            driverIn = ogr.GetDriverByName('DXF')
            dataSource = driverIn.Open(dxf, 0)
            dataSource.ExecuteSQL("SELECT * FROM entities WHERE Layer = 'PG-LP' OR Layer = 'PG-LI'")

            layerIn = dataSource.GetLayer()
            totalRegistros = layerIn.GetFeatureCount()
            #print "Total registros: " + unicode(totalRegistros)
            layerIn.ResetReading()
            inFeature = layerIn.GetNextFeature()

            #Recolectamos las features del dxf para poder procesarlas más adelante
            featuresExternas = []
            featuresInternas = []
            outFeature = []
            cnt = 0
            while inFeature:
                nombreCapa = inFeature.GetFieldAsString('Layer')
                if nombreCapa == 'PG-LP':
                    featuresExternas.append(inFeature)
                elif nombreCapa == 'PG-LI':
                    featuresInternas.append(inFeature)

                cnt = cnt + 1
                if cnt < totalRegistros:
                    inFeature = layerIn.GetNextFeature()
                else:
                    break

            #Hacemos segunda pasada para recuperar los textos de rotulo del dxf a pelo
            inFile = open(dxf)
            lineas = inFile.read().splitlines()
            inFile.close()
            centroides = []
            index = 0
            for line in lineas:
                line = line
                if line == 'TEXT':
                    if lineas[index + 2] == 'PG-AA':
                        rotulo = None
                        for l in range(30):
                            linea = lineas[index + l]
                            p_rot = re.compile('\s*\s1$')
                            p_cox = re.compile('\s*\s11$')
                            p_coy = re.compile('\s*\s21$')
                            #if linea == '   1':
                            if p_rot.match(linea):
                                if not rotulo:
                                    rotulo = lineas[index + l + 1]
                            #if linea == '  11':
                            if p_cox.match(linea):
                                coordx = lineas[index + l + 1]
                            #if linea == '  21':
                            if p_coy.match(linea):
                                coordy = lineas[index + l + 1]
                                break
                        centroides.append([rotulo, coordx, coordy])
                        #print rotulo + "[" + coordx + ", " + coordy + "]"
                index += 1

            #Procesamos el fichero alfanumérico
            asc = dxf.replace(".dxf", ".asc").replace(".DXF", ".ASC")
            try:
                datos_asc = self.procesaAsc(asc)

                 #Almacenamos las features de cada dxf
                dxfs_parcela[nombreDxf] = (featuresExternas, datos_asc)
                dxfs_constru[nombreDxf] = (featuresExternas, featuresInternas, centroides, datos_asc)
            except:
                print "FXCC " + nombreDxf + "Incompleto"
                pass

           

        #Pasamos todas las features recolectadas a las funciones encargadas de generar las capas
        self.generaCapaConstru(dxfs_constru)
        self.generaCapaParcela(dxfs_parcela)


    def buscaDxf(self, baseDir):

        matches = []
        for root, dirnames, filenames in os.walk(baseDir):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.dxf'  or \
                        os.path.splitext(filename)[1] == '.DXF':
                    matches.append(os.path.join(root, filename))
        return matches

    # run method that performs all the real work
    def run(self):

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        #self.prueba()
        # See if OK was pressed
        if result == 1:
            file = self.dlg.cmpRuta.text()
            if file != "":
                #print "Se selecciona el directorio: " + unicode(file)
                ficheros = self.buscaDxf(file)
                self.procesaDxf(ficheros)
                self.iface.zoomFull()