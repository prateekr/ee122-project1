import unittest

import sys
sys.path.append('.')

from sim.api import *
from sim.basics import *
from rip_router import RIPRouter
import sim.topo as topo
import os
import time

import sim.core
from hub import Hub as switch

import sim.api as api
import logging

class Test(unittest.TestCase):

    @classmethod  
    def setUpClass(cls):   
        start = sim.core.simulate
        start()
        
    def testDiscoveryPacket(self):
        r1 = RIPRouter()
        r1.name = "r1"
        r2 = RIPRouter()
        r2.name = "r2"
        r3 = RIPRouter()
        r3.name = "r3"
        
        r1.handle_rx(DiscoveryPacket(r2, 0), 1)
        r1.handle_rx(DiscoveryPacket(r3, 0), 2)
        
        self.failUnless(r1.distance_vector.dest_via_nbors == {r2:{None:0},r3:{None:0}})
        self.failUnless(r1.neighbor_ports == {r2:1, r3:2})

    """
    r1 -- r2
     |     |
    r3 -- r4
     |  /
     r5
    """
    def testDistanceVectorTable(self):
        r1 = RIPRouter()
        r1.name = "r1"
        r2 = RIPRouter()
        r2.name = "r2"
        r3 = RIPRouter()
        r3.name = "r3"
        r4 = RIPRouter()
        r4.name = "r4"
        r5 = RIPRouter()
        r5.name = "r5"
        
        r3.handle_rx(DiscoveryPacket(r1,0), None)
        r3.handle_rx(DiscoveryPacket(r4,0), None)
        r3.handle_rx(DiscoveryPacket(r5,0), None)
        
        packetOne = RoutingUpdate()
        packetOne.src = r1
        packetOne.paths = {r2:1,r3:1,r4:2,r5:2}
        packetFour = RoutingUpdate()
        packetFour.src = r4
        packetFour.paths = {r1:2,r2:1,r3:1,r5:1}
        packetFive = RoutingUpdate()
        packetFive.src = r5
        packetFive.paths = {r1:2,r2:2,r3:1,r4:1}
        
        r3.handle_rx(packetOne, 0)
        r3.handle_rx(packetFour, 0)
        r3.handle_rx(packetFive, 0)

        r3_table = {r1:{None:0,r4:2,r5:2},r2:{r1:1,r4:1,r5:2},r4:{r1:2,None:0,r5:1},r5:{r1:2,r4:1,None:0}}
        self.failUnless(r3.distance_vector.dest_via_nbors == r3_table)
        
    def testDistanceVectorRouteDeletion(self):
        r1 = RIPRouter()
        r1.name = "r1"
        r2 = RIPRouter()
        r2.name = "r2"
        r3 = RIPRouter()
        r3.name = "r3"
        r4 = RIPRouter()
        r4.name = "r4"
        r5 = RIPRouter()
        r5.name = "r5"
        
        r5.handle_rx(DiscoveryPacket(r3,0), None)
        r5.handle_rx(DiscoveryPacket(r4,0), None)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()