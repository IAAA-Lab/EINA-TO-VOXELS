import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eina_to_voxels import eina_to_voxels
from eina_to_voxels.heuristic import *



import unittest

class TestEina_to_voxels(unittest.TestCase):
        
    def testBasic(self):
        self.world = eina_to_voxels.World("resources/EINA.las",None,None,None,None,None)
        self.world.exportWorld("resources/out.txt")
    
    
    def testHeuristic(self):
        self.world = eina_to_voxels.World("resources/EINA.las",None,None,None,None,None)
        
        
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

if __name__ == '__main__':
    unittest.main()