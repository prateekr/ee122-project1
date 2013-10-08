from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
        # Add your code here!
        self.distance_vector = DistanceVector()
        self.neighbors = []
 
    def handle_rx (self, packet, port):
        # Add your code here!
        if type(packet) is DiscoveryPacket:
            if packet.is_link_up:
                self.neighbors.append(packet.src) 
                
        raise NotImplementedError

class DistanceVector ():
    def __init__(self):
        self.dest_dist = {} 
        self.dest_via_closest_neighbor = {}
    
    def updateVector(self, dest, neighbor, dist):
        update_required = (not dest in self.dest_dist) or (dist < self.dest_dist[dest])
        if update_required:
            self.dest_dist[dest] = dist + 1
            self.dest_via_closest_neighbor[dest] = neighbor
        return update_required