from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
        # Add your code here!
        self.distance_vector = DistanceVector(this)
        self.routing_packet = RoutingUpdate()
 
    def handle_rx (self, packet, port):
        # Add your code here!
        if type(packet) is DiscoveryPacket:
            if packet.is_link_up and not packet.src in self.neighbors: #TODO: make sure to check what happens if router goes down after packet is sent.
                if self.distance_vector.update_vector(packet.src, None, 0): self.send_dv_update()
        elif type(packet) is RoutingUpdate:
            if self.distance_vector.update_vector(packet): self.send_dv_update(port) 
    
    def send_dv_update(self):
        self.distance_vector.update_routing_packet(self.routing_packet)
        self.send(self.routing_packet, None, true)
            
class DistanceVector ():
    def __init__(self, owner):
        self.dest_via_nbors = {}
        self.owner = owner
        
    def update_vector(self, update_packet):
        update_required = false
        for dest in update_packet.all_dests:
            if dest == self.src: continue
            oldClosestDist = self.distance_to(dest)
            self.update_vector(dest, update_packet.src, update_packet.get_distance(dest) + 1)
            update_required = update_required or oldClosestDist > self.distance_to(key)
        return update_required
                
            
    def update_vector(self, dest, neighbor, dist):
        update_required = (not dest in self.dest_via_nbors) or (dist < self.distance_to(dest))
        if update_required:
            if not dest in self.dest_via_nbors:
                self.dest_via_nbors[dest] = {}
            self.dest_via_nbors[dest][neighbor] = dist + 1
        return update_required
    
    def update_routing_packet(self, routing_packet):
        for dest in self.dest_via_nbors:
            routing_packet.add_destination(dest, self.distance_to(dest))
    
    def distance_to(self, dest):
        return min(self.dest_via_nbors[dest].values())
    
    def get_neighbors(self):
        neighbors = []
        for key in self.dest_via_nbors.keys():
            if self.dest_via_nbors[key] == None:
                neighbors.append(key)
        return neighbors
        