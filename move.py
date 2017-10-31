# -*- coding: utf-8 -*-
"""
/***************************************************************************

A QGIS plugin for move all selected features from layer and snap it
to another vertex.

                              -------------------
        begin                : 2017-10-20
        copyright            : (C) 2017
        email                : saanchezfranco@gmail.com
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
import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
import resources_rc
# Import the code for the dialog
import os.path

rpointstart = QgsRubberBand(iface.mapCanvas(),QGis.Point )
rpointend = QgsRubberBand(iface.mapCanvas(),QGis.Point )
rl=QgsRubberBand(iface.mapCanvas(),QGis.Line )
premuto= False
linea=False
point0=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)
point1=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)

class MovewithSnap:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
    def initGui(self):
        self.iface.mapCanvas().setSelectionColor( QColor("lightgray") )
        self.action = QAction( QIcon( os.path.dirname(os.path.realpath(__file__)) +
            "/move.png" ), "Mover capa con snapping", self.iface.mainWindow() )

        #self.action = QAction( QIcon(":/plugins/move/icon.png"), u"move", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.action.setCheckable( True )
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Mover Capa", self.action)

    def unload(self):
        self.iface.removePluginMenu(u"&Mover Capa", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self,checked):
        if checked:
            caparedes = self.iface.activeLayer()
            QMessageBox.information(None, "Instrucciones de uso", " 1. Haga clic en vertice (x) de capa activa que desee ajustar."+'\n'+" 2. Haga clic en vertice de capa 2 donde quiere que se desplace la capa activa."+'\n'+" 3. Clic secundario para finalizar la edicion."+'\n\n'+"IMPORTANTE: Si es la primera vez en ejecucion de la herramienta, editar los siguientes atributos en Configuracion -> Opciones de autoensamblado: "+'\n\n'+"Seleccion de capa -> Todas las capas visibles "+'\n'+"Autoensamblar a -> A vertice "+'\n'+"Tolerancia -> 200 pixeles."+'\n'+"Aplicar y Aceptar.")
            selection = caparedes.selectAll()
            self.iface.setActiveLayer(self.iface.activeLayer())
            self.iface.actionToggleEditing().trigger()
            self.iface.actionMoveFeature().trigger()

            tool = PointTool(self.iface.mapCanvas())
            self.iface.mapCanvas().setMapTool(tool)

        else:
            for a in self.iface.attributesToolBar().actions():
              if a.objectName() == 'mActionDeselectAll':
                a.trigger()
                self.iface.setActiveLayer(self.iface.activeLayer())
                self.iface.actionToggleEditing().trigger()
                self.iface.actionMoveFeature().trigger()
                break

class PointTool(QgsMapTool):
        def __init__(self, canvas):
            QgsMapTool.__init__(self, canvas)
            self.canvas = canvas

        def canvasPressEvent(self, event):
            global rpointstart,rpointend,premuto ,point0,point1
            if event.button() == Qt.RightButton:
                rl.reset(QGis.Line)
                rpointstart.reset(QGis.Point)
                rpointend.reset(QGis.Point)

                premuto=False
                layer = iface.mapCanvas().currentLayer()

                #feature = layer.selectedFeatures()[0]

                reply = QMessageBox.question(None, "Deseas guardar los cambios?","Desea mover?", QMessageBox.Yes,QMessageBox.No)
                if reply == QMessageBox.Yes:
                  for feature in layer.selectedFeatures():
                     deltax = point1.x()-point0.x()
                     deltay = point1.y()-point0.y()
                     #QMessageBox.information(None, "snap0 :",str(deltax)+" "+str(deltay))
                     layer.translateFeature( feature.id(),deltax , deltay )
                  iface.mapCanvas().refresh()
                return None

            x = event.pos().x()
            y = event.pos().y()
            #QMessageBox.information(None, "snap0 :"+str(premuto),str(x)+" "+str(y))
            thisPoint = QPoint(x, y)
            snapper = QgsMapCanvasSnapper(self.canvas)
            (retval, result) = snapper.snapToBackgroundLayers(thisPoint)


            if not premuto:
              premuto=True
            else:
               premuto=False

            if result!=[]:
               x=result[0].snappedVertex.x()
               y=result[0].snappedVertex.y()

               #QMessageBox.information(None, "snap0 :"+str(premuto),str(point0.x())+" "+str(point0.y()))
               if premuto:
                point0 = result[0].snappedVertex
                rpointstart.setColor ( Qt.red )
                rpointstart.addPoint(point0)
               else:
                point1 = result[0].snappedVertex
                rpointend.setColor ( Qt.red )
                rpointend.addPoint(point1)
            else:

               if premuto:
                point0 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                rpointstart.setColor ( Qt.blue )
                rpointstart.addPoint(point0)
               else:
                point1 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                rpointend.setColor ( Qt.blue )
                rpointend.addPoint(point1)

               #MessageBox.information(None, "snap1 :"+str(premuto),str(point0.x())+" "+str(point0.y()))

        def canvasMoveEvent(self, event):

              x = event.pos().x()
              y = event.pos().y()
              global premuto,point0,point1,linea,rl
              if premuto:
               if not linea:
                rl.setColor ( Qt.red )
                point2 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                rl.addPoint(point0)
                rl.addPoint(point2)
                linea=True
               else:
                if linea:
                  point2 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                  rl.reset(QGis.Line)
                  rl.addPoint(point0)
                  rl.addPoint(point2)

        def canvasReleaseEvent(self, event):
         pass
#             global premuto,linea,rb,rl,point1,point0
#             angle = math.atan2(point1.x() - point0.x(), point1.y() - point0.y())
#             angle = math.degrees(angle)if angle>0 else (math.degrees(angle) + 180)+180
#             premuto=False
#             linea=False
#             actual_crs = self.canvas.mapRenderer().destinationCrs()
#             crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
#             xform = QgsCoordinateTransform(actual_crs, crsDest)
#             pt1 = xform.transform(point0)
#             webbrowser.open_new(dbName+'.html')
#             rl.reset()
#             rb.reset()

        def activate(self):
              pass

        def deactivate(self):
            pass

        def isZoomTool(self):
            pass


