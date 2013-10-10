'''
Created on Oct 9, 2013

@author: Prateek
'''
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


    def tearDown(self):
        pass

    def testBasicTwoRouterConnect(self):
        a = RIPRouter.create('b1')
        b = RIPRouter.create('b2')
        
        topo.link(b1, b2)
        time.sleep(5)
        
        self.failUnless( a.distance_vector.dest_via_nbors == {b:None} )
        self.failUnless( b.distance_vector.dest_via_nbors == {a:None} )

    def testBasicTwoRouterDisconnect(self):
        a = RIPRouter.create('b3')
        b = RIPRouter.create('b4')
        
        topo.link(b3, b4)
        time.sleep(5)
        self.failUnless( a.distance_vector.dest_via_nbors == {b:None} )
        self.failUnless( b.distance_vector.dest_via_nbors == {a:None} )
        topo.disconnect(b3)
        time.sleep(5)
        
        self.failUnless( a.distance_vector.dest_via_nbors == {} )
        self.failUnless( b.distance_vector.dest_via_nbors == {} )

    def testBasicRouterNetwork(self):
        ss1 = RIPRouter.create('s1')
        ss2 = RIPRouter.create('s2')
        ss3 = RIPRouter.create('s3')
        ss4 = RIPRouter.create('s4')
        ss5 = RIPRouter.create('s5')
        
        h1 = BasicHost.create('h1a')
        h2 = BasicHost.create('h1b')
        h3 = BasicHost.create('h2a')
        h4 = BasicHost.create('h2b')

        topo.link(s1, h1a)
        topo.link(s1, h1b)
          
        topo.link(s2, h2a)
        topo.link(s2, h2b)

        topo.link(s1, s3)
        topo.link(s3, s2)

        topo.link(s1, s4)
        topo.link(s4, s5)
        topo.link(s5, s2)
        
        time.sleep(5)

        r1_table = ss1.distance_vector.get_routing_packet().paths
        r2_table = ss2.distance_vector.get_routing_packet().paths
        r3_table = ss3.distance_vector.get_routing_packet().paths
        r4_table = ss4.distance_vector.get_routing_packet().paths
        r5_table = ss5.distance_vector.get_routing_packet().paths

        expected_r1_table = {h1:1,h2:1,h3:3,h4:3,ss2:2,ss3:1,ss4:1,ss5:2}
        expected_r2_table = {h1:3,h2:3,h3:1,h4:1,ss1:2,ss3:1,ss4:2,ss5:1}
        expected_r3_table = {h1:2,h2:2,h3:2,h4:2,ss1:1,ss2:1,ss4:2,ss5:2}
        expected_r4_table = {h1:2,h2:2,h3:3,h4:3,ss1:1,ss2:2,ss3:2,ss5:1}
        expected_r5_table = {h1:3,h2:3,h3:2,h4:2,ss1:2,ss2:1,ss3:2,ss4:1}

        self.failUnless( r1_table == expected_r1_table )
        self.failUnless( r2_table == expected_r2_table )
        self.failUnless( r3_table == expected_r3_table )
        self.failUnless( r4_table == expected_r4_table )
        self.failUnless( r5_table == expected_r5_table )
        
        
    """s1 -- s2 -- s3
       |      |
       s4 -- s6
       |      |
       s5 -- s7
              |
             s8 Remove s4 and test that network wo"""

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()