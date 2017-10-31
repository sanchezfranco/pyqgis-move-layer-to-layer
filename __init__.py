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

 This script initializes the plugin, making it known to QGIS.
"""
#name_of_file_without_py/name_of_class_on_it

def classFactory(iface):
    from move import MovewithSnap
    return MovewithSnap(iface)
