#!/usr/bin/python
'''
10/4/14
mars networks

'''
import sys
import math

BIG_NUMBER = 100000

class Point(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.connected = False
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        
def get_connected(probes):
    '''
    returns list of points that are connected to network
    '''
    return {i for i in probes if i.connected}
    
def make_first_connection(distance_matrix, id_probe_dict):
    '''
    given a distance matrix, connects the probes that are closest
    returns a set with the ids of the connected probes
    '''
    global total_distance
    min_distance = BIG_NUMBER
    for row,probe1 in enumerate(distance_matrix):
        row_min = min(probe1)
        if row_min < min_distance:
            min_distance = row_min
            min_row = row
            min_col = probe1.index(min_distance)
    connect_pair(distance_matrix, min_row, min_col, id_probe_dict)
    total_distance += min_distance
    #print 'connected {} and {}'.format(min_row, min_col)
    return {min_row, min_col}
    #id_probe_dict[min_row].connected = True
    #id_probe_dict[min_col].connected = True
    
    
def connect_to_network(distance_matrix, id_probe_dict, connected_set):
    '''
    given a set of connected probes, looks for the closest unconnected probe
    to any of the connected probes, makes that connection 
    '''
    global total_distance
    min_distance = BIG_NUMBER
    for probe1_id in connected_set:
        row = distance_matrix[probe1_id]
        row_min = min(row)
        if row_min < min_distance:
            min_distance = row_min
            min_row = probe1_id
            min_col = row.index(min_distance)
    connect_pair(distance_matrix, min_row, min_col, id_probe_dict)
    total_distance += min_distance
    #print 'connected {} and {}'.format(min_row, min_col)
    return {min_row, min_col}
    
def connect_pair(distance_matrix, id1, id2, id_probe_dict):
    '''
    given 2 ids, will mark those corresponding probes as connected
    Also will set their distances to the max
    '''
    probe1 = id_probe_dict[id1]
    probe2 = id_probe_dict[id2]
    probe1.connected = True
    probe2.connected = True
    distance_matrix[id1][id2] = BIG_NUMBER
    distance_matrix[id2][id1] = BIG_NUMBER
    reset_column(distance_matrix, id1)
    reset_column(distance_matrix, id2)
        
def pairwise_distances(probes, id_probe_dict):
    '''
    given a set of probes calculate all pairwise distances
    returns as a 2d array
    '''
    n_probes = len(probes)
    distance_matrix = [[BIG_NUMBER for _ in xrange(n_probes)] for _ in xrange(n_probes)]
    for id1 in id_probe_dict:
        for id2 in id_probe_dict:
            if id1 != id2:
                distance = id_probe_dict[id1].distance_to(id_probe_dict[id2])
                distance_matrix[id1][id2] = distance
                distance_matrix[id2][id1] = distance
    return distance_matrix

def get_id_probe_dict(probes):
    '''
    given a set of probes map each probe to a specific id #
    return a dict where key is id, value is probe object
    '''
    return {pos:i for pos,i in enumerate(probes)} # my first dictionary comprehension!
    
def reset_column(distance_matrix, col):
    for row in distance_matrix:
        row[col] = BIG_NUMBER

with open(sys.argv[1]) as FH:
    for line in FH:
        total_distance = 0
        unique_set = {i for i in line.split()} # do this to remove duplicate points
        probes = {Point(i.split(',')[0], i.split(',')[1]) for i in unique_set}
        
        id_probe_dict = get_id_probe_dict(probes)

            
        distance_matrix = pairwise_distances(probes, id_probe_dict)
        
        connected_set = make_first_connection(distance_matrix, id_probe_dict)
        
        while len(connected_set) < len(probes):
            connected_set |= connect_to_network(distance_matrix, id_probe_dict, connected_set)
        print int(math.ceil(total_distance))
            
            
        


