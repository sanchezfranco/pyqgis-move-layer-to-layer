import os

# Import the PyQt and QGIS libraries
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsProject
from PyQt4.QtGui import *

class Main:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Selection color of features
        self.iface.mapCanvas().setSelectionColor( QColor("yellow") )
        # Create action that will start plugin configuration
        self.btnredes = QAction( QIcon( os.path.dirname(os.path.realpath(__file__)) +
            "/move.png" ), "Mover capa geografica activa", self.iface.mainWindow() )
        # connect the button to the run method
        self.btnredes.triggered.connect( self.run )
        self.btnredes.setCheckable( True )
        # Add toolbar button to the Plugins toolbar
        self.iface.addToolBarIcon(self.btnredes)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu( "&Plugin Inggepro", self.btnredes )
        self.iface.removeToolBarIcon(self.btnredes)

    # run method that performs all the real work
    def run(self, checked): 
        if checked:
            caparedes = self.iface.activeLayer()
            selection = caparedes.selectAll()
            self.iface.setActiveLayer(self.iface.activeLayer())
            self.iface.actionToggleEditing().trigger()
            self.iface.actionMoveFeature().trigger()
        else:
            for a in self.iface.attributesToolBar().actions(): 
              if a.objectName() == 'mActionDeselectAll':
                a.trigger()                
                self.iface.setActiveLayer(self.iface.activeLayer())
                self.iface.actionToggleEditing().trigger()    
                break   