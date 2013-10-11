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
        
        self.failUnless( a.distance_vector.dest_via_nbors == {b:{None:0}} )
        self.failUnless( b.distance_vector.dest_via_nbors == {a:{None:0}} )

    def testBasicTwoRouterDisconnect(self):
        a = RIPRouter.create('b3')
        b = RIPRouter.create('b4')
        
        topo.link(b3, b4)
        time.sleep(5)
        topo.disconnect(b3)
        time.sleep(5)
        
        self.failUnless( a.distance_vector.dest_via_nbors == {} )
        self.failUnless( b.distance_vector.dest_via_nbors == {} )
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()