# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright 2016 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# ==================================================
# AddLLOSFieldsTestCase.py
# --------------------------------------------------
# requirements:
# * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
# * Python 2.7 or Python 3.4
#
# author: ArcGIS Solutions
# company: Esri
#
# ==================================================
# history:
# ==================================================

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class AddLLOSFieldsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Add LLOS Fields tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     AddLLOSFieldsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        originalObservers = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers")
        originalTargets = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets")

        self.inputObservers = os.path.join(Configuration.militaryScratchGDB, "LLOS_Observers")
        self.inputTargets = os.path.join(Configuration.militaryScratchGDB, "LLOS_Targets")

        arcpy.CopyFeatures_management(originalObservers, self.inputObservers)
        arcpy.CopyFeatures_management(originalTargets, self.inputTargets)

    def tearDown(self):
        if Configuration.DEBUG == True: print("     AddLLOSFieldsTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_add_llos_fields_pro(self):
        try:
            arcpy.AddMessage("Testing Add LLOS Fields (Pro).")
            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            runToolMessage = "Running tool (Add LLOS Fields)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            self.assertTrue(arcpy.Exists(self.inputObservers), "Input dataset does not exist, %s" % self.inputObservers)
            self.assertTrue(arcpy.Exists(self.inputTargets), "Input dataset does not exist, %s" % self.inputTargets)

            arcpy.AddLLOSFields_mt(self.inputObservers, 2, self.inputTargets, 0)

            fieldList = arcpy.ListFields(self.inputObservers, "height")
            fieldCount = len(fieldList)

            self.assertEqual(fieldCount, 1, "Expected a field count of 1 for Observers but got %s." % str(fieldCount))

            fieldList = arcpy.ListFields(self.inputTargets, "height")
            fieldCount = len(fieldList)

            self.assertEqual(fieldCount, 1, "Expected a field count of 1 for Targets but got %s." % str(fieldCount))

        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()

