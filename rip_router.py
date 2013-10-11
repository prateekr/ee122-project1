from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
        # Add your code here!
        self.distance_vector = DistanceVector(self)
        self.neighbor_ports = {}
         
    def handle_rx (self, packet, port):
        # Add your code here!
        if type(packet) is DiscoveryPacket:
            if packet.is_link_up and not packet.src in self.distance_vector.get_neighbors(): #TODO: make sure to check what happens if router goes down after packet is sent.
                if self.distance_vector.update_vector(packet.src, None, 0):
                    self.neighbor_ports[packet.src] = port
                    self.send_dv_update()
            elif not packet.is_link_up or packet.latency >= 100:
                if self.distance_vector.delete_node(packet.src):
                    del(self.neighbor_ports[packet.src])
                    self.send_dv_update()
                
        elif type(packet) is RoutingUpdate:
            if self.distance_vector.update_from_packet(packet): self.send_dv_update() 
    
    def send_dv_update(self):
        for neighbor in self.neighbor_ports.keys():
            routing_packet = self.distance_vector.get_routing_packet(neighbor)
            self.send(routing_packet, None, True)
            
class DistanceVector ():
    def __init__(self, owner):
        self.dest_via_nbors = {}
        self.owner = owner
        
    def update_from_packet(self, update_packet):
        update_required = False
        for dest in list(set(self.dest_via_nbors.keys()) | set(update_packet.all_dests())):
            oldClosestDist = self.distance_to(dest)
            if update_packet.src == dest or self.owner == dest:
                continue
            elif not dest in update_packet.all_dests():
                del(self.dest_via_nbors[dest][update_packet.src])
                if len(self.dest_via_nbors[dest].keys()) == 0: del(self.dest_via_nbors[dest])
            elif not dest in self.dest_via_nbors:
                self.update_vector(dest, update_packet.src, update_packet.get_distance(dest))
            self.update_vector(dest, update_packet.src, update_packet.get_distance(dest))
            update_required = update_required or oldClosestDist != self.distance_to(dest)
        return update_required
            
    def update_vector(self, dest, neighbor, dist_from_neighbor):
        old_distance = self.distance_to(dest)
        if not dest in self.dest_via_nbors: self.dest_via_nbors[dest] = {}
        if dist_from_neighbor >= 99:
            if neighbor in self.dest_via_nbors:
                del(self.dest_via_nbors[dest][neighbor])
                if len(self.dest_via_nbors) == 0: del(self.dest_via_nbor[dest][neighbor])
        else:
            self.dest_via_nbors[dest][neighbor] = dist_from_neighbor
        return old_distance != self.distance_to(dest)
    
    def delete_link(self, node):
        update_required = False
        for dest in self.dest_via_nbors.keys():
            oldDist = self.distance_to(dest)
            if dest == node and None in self.dest_via_nbors[dest]:
                del(self.dest_via_nbors[dest][None])
                if len(self.dest_via_nbors[dest].keys()) == 0: del(self.dest_via_nbors[dest])
                update_required = True
            else:
                if node in self.dest_via_nbors[dest]:
                    del(self.dest_via_nbors[dest][node])
            if oldDist != self.distance_to(dest): update_required = True
        return update_required      
    
    def get_routing_packet(self,packet_dst):
        routing_packet = RoutingUpdate()
        routing_packet.src = self.owner
        for dest in self.dest_via_nbors.keys():
            if dest not in self.owner.neighbor_ports.keys() and self.closestNeighborTo(dest) == packet_dst:
                continue
            routing_packet.add_destination(dest, self.distance_to(dest))
        return routing_packet
    
    def distance_to(self, dest):
        if not dest in self.dest_via_nbors: return float("inf")
        return min(self.dest_via_nbors[dest].values()) + 1
    
    def closestNeighborTo(self, dest):
        distance = self.distance_to(dest)
        if distance >= 100: return None
        closestNeighbors = {}
        for neighbor in self.dest_via_nbors[dest].keys():
            if distance == self.dest_via_nbors[dest][neighbor]:
                closestNeighbors[self.owner.neighbor_ports[neighbor]] = neighbor
        return closestNeighbors[min(closestNeighbors.values())]
    
    
    def get_neighbors(self):
        neighbors = []
        for key in self.dest_via_nbors.keys():
            if None in self.dest_via_nbors[key]:
                neighbors.append(key)
        return neighbors
        