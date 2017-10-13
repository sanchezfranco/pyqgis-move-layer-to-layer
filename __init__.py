"""
/***************************************************************************
Move features
A QGIS plugin
Move massive elements to layer plugin
-------------------
begin : 2017-10-13
copyright : (C) 2017 by sanchezfranco
email : saanchezfranco@gmail.com
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
def name():
    return "Plugin GasSur"
def description():
    return "Move massive elements to layer plugin"
def version():
    return "Version 1.0"
def icon():
    return "move.png"
def qgisMinimumVersion():
    return "2.0"
def classFactory(iface):
    # load Main class from file gassur.py
    from gassur import Main
    return Main(iface)
