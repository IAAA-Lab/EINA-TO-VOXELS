import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eina_to_voxels import eina_to_voxels
from eina_to_voxels.heuristic import *



import unittest

class TestEina_to_voxels(unittest.TestCase):
    """
    def setUp(self):
        self.world = eina_to_voxels.World("resources/EINA.las")
    """
        
        
    def testBasic(self):
        self.world = eina_to_voxels.World("resources/EINA.las")
        self.world.exportWorld("resources/out.txt")
    
    
    def testHeuristic(self):
        self.world = eina_to_voxels.World("resources/EINA.las")
        
        
        self.world.add(UseOpenStreetMap([]))
        self.world.add(MergeColors([]))
        self.world.add(DeleteIsolated([]))
        self.world.add(DeleteIsolatedGroups([]))
        self.world.add(ExpandBlocks([]))
        self.world.add(Join([]))
        self.world.add(SetGreenZone([]))
        self.world.add(SetRoads([]))
        #world.add(eina_to_voxels.AddBuilding([sys.argv[3],float(sys.argv[4]),float(sys.argv[5]), float(sys.argv[6])]))    
        self.world.add(CreateWalls([]))
        
        self.world.start()
        self.world.exportWorld("resources/out.txt")
    
    """
        
    def testOpenStreetworld(self):
        self.world.read("resources/EINA.las")
        self.world.useOpenStreetMap()
        self.world.exportWorld("resources/out.txt")
        
        
    def testFull(self):
        self.world.read("resources/EINA.las")
        self.world.useOpenStreetMap()
        self.world.useHeuristic()
        self.world.exportWorld("resources/out.txt")

    
    def testAddBuilding(self):
        self.world.read("resources/EINA.las")
        self.world.addBuilding("resources/adaByron.binvox",62,49,5)
        self.world.addSign(5,5)
        self.world.exportWorld("resources/out.txt")
        
        
    def testAddBuildingWithHeuristic(self):
        self.world.read("resources/EINA.las")
        self.world.addBuilding("resources/adaByron.binvox",62,49,5)
        self.world.useHeuristic()
        self.world.createWalls()
        self.world.exportWorld("resources/out.txt")
    """


if __name__ == '__main__':
    unittest.main()