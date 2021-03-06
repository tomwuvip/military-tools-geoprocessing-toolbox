# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
TableToPolylineTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/11/2016 - JH - initial creation
6/1/2016 - MF - update error handling
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class TableToPolylineTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Polyline tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputPolylines = None
    proBaseFC = None
    desktopBaseFC = None
    platform = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPolylineTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        csvPath = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvPath, "TabletoPolyline.csv")
        self.outputPolylines = os.path.join(Configuration.militaryScratchGDB, "outputPolylines")
        self.BaseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToPolyline")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, self.inputTable, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPolylineTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_polyline_desktop(self):
        '''Test Table To Polyline for ArcGIS Desktop'''
        try:
            runToolMessage = ".....TableToPolylineTestCase.test_table_to_polyline_desktop"
            arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.TableToPolyline_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolylines)
            
            self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
            
            polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
            expectedFeatures = int(1)
            self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))
            
            compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPolylines, "Shape_Length")
            # identical = 'true' means that there are no differences between the base and the output feature class
            identical = compareFeatures.getOutput(1)
            self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
            
        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()        

        
    def test_table_to_polyline_pro(self):
        '''Test Table To Polyline for ArcGIS Pro'''
        try:
            runToolMessage = ".....TableToPolylineTestCase.test_table_to_polyline_pro"
            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.TableToPolyline_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolylines)
            
            self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
            
            polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
            expectedFeatures = int(1)
            self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))
            
            compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPolylines, "Shape_Length")
            # identical = 'true' means that there are no differences between the base and the output feature class
            identical = compareFeatures.getOutput(1)
            self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
            
        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()
        