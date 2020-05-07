# -*- coding: utf-8 -*-

"""
/***************************************************************************
 RRIM
                                 A QGIS plugin
 Genera RRIM a partir de datos de elevación
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-05
        copyright            : (C) 2020 by David Ríos Santana
        email                : davriosan@gmail.com
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

__author__ = 'David Ríos Santana'
__date__ = '2020-05-05'
__copyright__ = '(C) 2020 by David Ríos Santana'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect
from qgis.PyQt.QtGui import QIcon

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class RRIMAlgorithm(QgsProcessingAlgorithm):
    """
    Código para la generación de RRIM (Red Relief Image Map) a partir de datos de elevación raster.

    Se ha simplificado la generación para integrar una metodología sencilla dentro de Qgis, siguiendo
    los principios descritos en https://www.isprs.org/proceedings/XXXVII/congress/2_pdf/11_ThS-6/08.pdf
    y https://proceedings.esri.com/library/userconf/proc16/papers/446_644.pdf

    Funcionamiento probado en las versiones 3.6.3, 3.10.4 y 3.12 de Qgis.
    """

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config=None):
        """
        Se defienen los inputs y outputs del algoritmo junto con otras propiedades.
        """

        self.addParameter(QgsProcessingParameterRasterLayer('digitalelevationmodel', 'Digital Elevation Model', defaultValue=None))

        # Se define la entrada del DEM necesario para el funcionamiento del algoritmo.
        # Se acepta cualquier formato raster de elevación.
        # Posteriormente, se definen los dos datos de salida del algoritmo que componen el RRIM.
        
        self.addParameter(
            QgsProcessingParameterRasterDestination('Slope', 'Slope', createByDefault=True, defaultValue=''))
        
        self.addParameter(
            QgsProcessingParameterRasterDestination('Rvi', 'RVI', createByDefault=True, defaultValue=None))
        

    def processAlgorithm(self, parameters, context, model_feedback):
        """
        Here is where the processing itself takes place.
        """
        
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}
        
        # Slope
        alg_params = {
            'INPUT': parameters['digitalelevationmodel'],
            'Z_FACTOR': 1,
            'OUTPUT': parameters['Slope']
        }
        outputs['Slope'] = processing.run('qgis:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Slope'] = outputs['Slope']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        

        # Topographic openness. Salidas Openness positivo y negativo.
        alg_params = {
            'DEM': parameters['digitalelevationmodel'],
            'DLEVEL': 3,
            'METHOD': 0,
            'NDIRS': 8,
            'RADIUS': 8000,
            'NEG': QgsProcessing.TEMPORARY_OUTPUT,
            'POS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TopographicOpenness'] = processing.run('saga:topographicopenness', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
            
                       
        # Establecer estilo para capa ráster. Se definen rutas relativas en la carga para acceder a la carpeta
        # donde se haya instalado el complemento.
        alg_params = {
            'INPUT': outputs['Slope']['OUTPUT'],
            'STYLE': os.path.join(os.path.join(cmd_folder, 'slope_style.qml'))
        }
        outputs['EstablecerEstiloParaCapaRster'] = processing.run('qgis:setstyleforrasterlayer', alg_params, context=context, feedback=feedback,is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
            slope.triggerRepaint()

        # Calculadora ráster. Expresión para general el RVI o Ridge-Valley Index.
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': '(A-B)/2',
            'INPUT_A': outputs['TopographicOpenness']['POS'],
            'INPUT_B': outputs['TopographicOpenness']['NEG'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': parameters['Rvi']
        }
        outputs['CalculadoraRster'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Rvi'] = outputs['CalculadoraRster']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
            
        # Establecer estilo para capa ráster.Se definen rutas relativas en la carga para acceder a la carpeta
        # donde se haya instalado el complemento.
        alg_params = {
            'INPUT': outputs['CalculadoraRster']['OUTPUT'],
            'STYLE': os.path.join(os.path.join(cmd_folder, 'rvi_style.qml'))
        }
        outputs['EstablecerEstiloParaCapaRster'] = processing.run('qgis:setstyleforrasterlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
        rvi.triggerRepaint()
        

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Red Relief Image Map generator'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def icon(self):
        """
        Cadena para retornar el icono del complemento mediante rutas relativas.
        """
    
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'logo.png')))
        return icon

    def createInstance(self):
        return RRIMAlgorithm()
