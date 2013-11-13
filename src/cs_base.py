##
## Circuitscape (C) 2013, Brad McRae and Viral B. Shah. 
##

import sys, time, gc, traceback, logging, inspect
import numpy as np
from scipy.sparse.linalg import cg
from scipy import sparse
from pyamg import smoothed_aggregation_solver, ruge_stuben_solver
from scipy.sparse.csgraph import connected_components

from cs_cfg import CSConfig
from cs_state import CSState
from cs_io import CSIO

print_timings_spaces = 0
print_timings = False

def print_timing_enabled(is_enabled):
    """Enables or disables the print_timings decorator."""
    global print_timings
    print_timings = is_enabled

def print_timing(func):
    """Prints time elapsed for functions with print_timings decorator."""  
    def wrapper(*arg):
        if not print_timings:
            return func(*arg)
        global print_timings_spaces
        print_timings_spaces +=  2
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print_timings_spaces -=  2
        print("%10d sec: %s%s"%((t2-t1), " "*print_timings_spaces, func.func_name))
        sys.stdout.flush()
        return res
    return wrapper

class CSBase(object):    
    """Circuitscape base class, common across all circuitscape modules"""
    def __init__(self, configFile, gui_logger):
        np.seterr(invalid='ignore')
        np.seterr(divide='ignore')
        
        self.state = CSState()
        self.state.amg_hierarchy = None
        self.options = CSConfig(configFile)
        
        #self.options.low_memory_mode = True        

        print_timing_enabled(self.options.print_timings)
        #print_timing_enabled(True)
        
        if gui_logger == 'Screen':
            self.options.screenprint_log = True
            gui_logger = None
        else:
            self.options.screenprint_log = False
        #self.options.screenprint_log = True
        
        self.gui_logger = gui_logger
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                            datefmt='%m/%d/%Y %I.%M.%S.%p',
                            level=logging.DEBUG)


    # TODO: should ultimately be replaced with the logging module.
    # logging to UI should be handled with another logger or handler
    def log(self, text, col):
        """Prints updates to GUI or python window."""
        if (self.gui_logger != None) or (self.options.screenprint_log == True and len(text) > 1):
            text = '%s%s'%(' '*len(inspect.stack()), str(text))
        
            if self.gui_logger:
                self.gui_logger.log(text, col)
                
            if self.options.screenprint_log == True and len(text) > 1:
                if col == 1:
                    logging.info(text)
                else:
                    logging.debug(text)
                sys.stdout.flush()
    
        
    def log_complete_job(self):
        """Writes total time elapsed at end of run."""
        (hours,mins,secs) = self.elapsed_time(self.state.start_time)
        if hours>0:
            self.log('Job took ' + str(hours) +' hours ' + str(mins) + ' minutes to complete.',2)
        else:
            self.log('Job took ' + str(mins) +' minutes ' + str(secs) + ' seconds to complete.',2)

        
    def enable_low_memory(self, restart):
        """Runs circuitscape in low memory mode.  Not incredibly helpful it seems."""  
        self.state.amg_hierarchy = None
        gc.collect()
        if self.options.low_memory_mode==True:
            if restart==False: #If this module has already been called
                raise MemoryError
        self.options.low_memory_mode = True
        print'\n**************\nMemory error reported.'        

        ex_type, value, tb = sys.exc_info()
        info = traceback.extract_tb(tb)
        print'Full traceback:'
        print info
        print'***************'
        filename, lineno, function, _text = info[-1] # last line only
        print"\n %s:%d: %s: %s (in %s)" %\
              (filename, lineno, ex_type.__name__, str(value), function)

        ex_type = value = tb = None # clean up
        print'\nWARNING: CIRCUITSCAPE IS RUNNING LOW ON MEMORY.'
        if restart==True:
            print'Restarting in low memory mode, which will take somewhat longer to complete.'
        else:
            print'Switching to low memory mode, which will take somewhat longer to complete.'            
        print'CLOSING OTHER PROGRAMS CAN HELP FREE MEMORY RESOURCES.'
        print'Please see the user guide for more information on memory requirements.\n'               
        if restart==True:
            print'***Restarting in low memory mode***\n'
        else:
            print'***Continuing in low memory mode***\n'
        return

    
    @staticmethod
    @print_timing
    def solve_linear_system(G, rhs, solver_type, ml):
        """Solves system of equations."""  
        gc.collect()
        # Solve G*x = rhs
        x = []
        if solver_type == 'cg+amg':
            G.psolve = ml.psolve
            (x, flag) = cg(G, rhs, tol = 1e-6, maxiter = 100000)
            if flag !=  0 or np.linalg.norm(G*x-rhs) > 1e-3:
                raise RuntimeError('CG did not converge. May need more iterations.') 

        if solver_type == 'amg':
            x = ml.solve(rhs, tol = 1e-6);

        return x 
 
         
    @staticmethod
    @print_timing
    def laplacian(G): 
        """Returns Laplacian of graph."""  
        n = G.shape[0]

        # FIXME: Potential for memory savings, if assignment is used
        G = G - sparse.spdiags(G.diagonal(), 0, n, n)
        G = -G + sparse.spdiags(G.sum(0), 0, n, n)

        return G

        
    @print_timing
    def create_amg_hierarchy(self, G): 
        """Creates AMG hierarchy."""  
        if self.options.solver == 'amg' or self.options.solver == 'cg+amg':
            self.state.amg_hierarchy = None
            # construct the MG hierarchy
            ml = []
            #  scipy.io.savemat('c:\\temp\\graph.mat',mdict={'d':G})
            ml = smoothed_aggregation_solver(G, max_coarse=10000, symmetry='symmetric', coarse_solver='splu')
            print ml
            self.state.amg_hierarchy = ml


    @staticmethod
    def grid_to_graph (x, y, node_map):
        """Returns node corresponding to x-y coordinates in input grid."""  
        return node_map[x, y] - 1
        
    
    @staticmethod
    def elapsed_time(startTime): 
        """Returns elapsed time given a start time."""    
        now = time.time()
        elapsed = now-startTime
        secs = int(elapsed)
        mins = int(elapsed/60)
        hours = int(mins/60)
        mins = mins - hours*60
        secs = secs - mins*60 - hours*3600
        return hours, mins, secs
    
    @staticmethod
    def deleterow(A, delrow):
        m = A.shape[0]
        n = A.shape[1]
        keeprows = np.delete(np.arange(0, m), delrow)
        keepcols = np.arange(0, n)
        return A[keeprows][:,keepcols]
            
    @staticmethod
    def deletecol(A, delcol):
        m = A.shape[0]
        n = A.shape[1]
        keeprows = np.arange(0, m)
        keepcols = np.delete(np.arange(0, n), delcol)
        return A[keeprows][:,keepcols]
    
    @staticmethod
    def deleterowcol(A, delrow, delcol):
        m = A.shape[0]
        n = A.shape[1]
    
        keeprows = np.delete(np.arange(0, m), delrow)
        keepcols = np.delete(np.arange(0, n), delcol)
    
        return A[keeprows][:,keepcols]
    
    @staticmethod
    def relabel(oldlabel, offset=0):
        newlabel = np.zeros(np.size(oldlabel), dtype='int32')
        s = np.sort(oldlabel)
        perm = np.argsort(oldlabel)
        f = np.where(np.diff(np.concatenate(([s[0]-1], s))))
        newlabel[f] = 1
        newlabel = np.cumsum(newlabel)
        newlabel[perm] = np.copy(newlabel)
        return newlabel-1+offset





class CSFocalPoints:
    """Represents a set of focal points and associate logic to work with them"""
    def __init__(self, points, included_pairs, is_network):
        self.included_pairs = included_pairs
        self.is_network = is_network
        if is_network:
            # network mode
            self.is_network = True
            self.points_rc = None
            self.point_ids = points
            self._prune_included_pairs()
        else:
            # raster mode
            self.is_network = False
            self.points_rc = points
            self._prune_included_pairs()
            self.point_ids = self._get_point_ids()            

    
    def _prune_included_pairs(self):
        """Remove excluded points from focal node list when using extra file that lists pairs to include/exclude."""
        
        if self.included_pairs == None:
            return
        
        include_list = list(self.included_pairs[0,:])
        point = 0
        _drop_flag = False
        
        if self.is_network:
            while point < self.point_ids.size: #Prune out any points not in includeList
                if self.point_ids[point] in include_list: #match
                    point = point+1
                else:
                    _drop_flag = True   
                    self.point_ids = np.delete(self.point_ids, point)
             
            include_list = list(self.point_ids[:])            
        else:
            while point < self.points_rc.shape[0]: #Prune out any points not in include_list
                if self.points_rc[point,0] in include_list: #match
                    point = point+1
                else:
                    _drop_flag = True   
                    self.points_rc = CSBase.deleterow(self.points_rc, point)  
             
            include_list = list(self.points_rc[:,0])
        
        num_connection_rows = self.included_pairs.shape[0]
        row = 1
        while row < num_connection_rows: #Prune out any entries in include_list that are not in points_rc
            if self.included_pairs[row,0] in include_list: #match
                row = row+1
            else:
                self.included_pairs = CSBase.deleterowcol(self.included_pairs, delrow=row, delcol=row)   
                _drop_flag = True
                num_connection_rows = num_connection_rows-1

        #if _drop_flag==True:
        #    logging.info('\nNOTE: Code to exclude pairwise calculations is activated and some entries did not match with focal node file. Some focal nodes may have been dropped.')      


    def _get_point_ids(self):
        """Return a list of unique focal node IDs"""
        return np.unique(np.asarray(self.points_rc[:,0]))

    def num_points(self):
        if self.is_network:
            return self.point_ids.size
        else:
            return self.points_rc.shape[0]
    
    def get_unique_coordinates(self):
        """Return a list of unique focal node IDs and x-y coordinates."""
        if self.is_network:
            raise RuntimeError('Not available in network mode')
          
        points_rc_unique = np.zeros((self.point_ids.size, 3), int)
        for i in range(0, self.point_ids.size):
            for j in range(0, self.points_rc.shape[0]):
                if self.points_rc[j,0] == self.point_ids[i]:
                    points_rc_unique[i,:] = self.points_rc[j,:] 
                    break                    
        return points_rc_unique          


    def get_coordinates(self, pt_idx=None):
        """Returns a list of focal node IDs and x-y coordinates or only x-y coordinates if an index or ID is specified"""
        if self.is_network:
            raise RuntimeError('Not available in network mode')
          
        if pt_idx != None:
            return (self.points_rc[pt_idx,1], self.points_rc[pt_idx,2])
            
        return self.points_rc

    def get_subset(self, idx_list):
        """Returns a subset of focal point coordinates for supplied indexes"""
        if self.is_network:
            raise RuntimeError('Not available in network mode')
        
        ncoords = len(idx_list)
        sub_coords = np.zeros((ncoords,3), int)
        for idx in range(0, ncoords):
            sub_coords[idx,:] = self.points_rc[idx_list[idx], :]
        
        return CSFocalPoints(sub_coords, self.included_pairs, self.is_network)

    @staticmethod
    def grid_to_graph(x, y, node_map):
        """Returns node corresponding to x-y coordinates in input grid."""  
        return node_map[x, y] - 1


    def exists_points_in_component(self, comp, habitat):
        """Checks to see if there are focal points in a given component.
        
        Last parameter can either be a habitat object or a tuple of components and node_map.
        In network mode, components and node_map both are vectors.
        In raster mode, components is a vector and node_map is a matrix.
        """
        if type(habitat) == tuple:
            components, node_map = habitat
        else:
            components = habitat.components
            node_map = habitat.node_map
        if self.is_network:
            indices = np.where(components == comp)
            nodes_in_component = node_map[indices]            
            include_list = nodes_in_component.tolist()
            for pt_id in self.point_ids:
                if pt_id in include_list:
                    return True
        else:
            numpoints = self.points_rc.shape[0]
            for pt1 in range(0, numpoints): 
                src = self.grid_to_graph(self.points_rc[pt1,1], self.points_rc[pt1,2], node_map)
                for pt2 in range(pt1+1, numpoints):
                    dst = self.grid_to_graph(self.points_rc[pt2,1], self.points_rc[pt2,2], node_map)
                    if (src >=  0 and components[src] == comp) and (dst >=  0 and components[dst] == comp):
                        return True
        return False
    
    
    def get_graph_node_idx(self, focal_point_idx, node_map):
        """Returns the index of the focal point node in the graph.
        
        In network mode, node_map is a vector. It can be a pruned node map representing only one component of the map.
        In raster mode, node_map is a matrix.
        """
        if self.is_network:
            return node_map.tolist().index(self.point_ids[focal_point_idx])
        else:
            return self.grid_to_graph(self.points_rc[focal_point_idx,1], self.points_rc[focal_point_idx,2], node_map)
    
    
    def point_id(self, idx):
        if self.is_network:
            return self.point_ids[idx]
        else:
            return self.points_rc[idx,0]    
    
    def point_pair_idxs(self):
        """Returns pairs of point indices across all components
        
        Returns (x, -1) to denote end of each first node number.
        """
        if self.is_network:
            numpoints = self.point_ids.size
            for n1_idx in range(0, numpoints-1):
                for n2_idx in range(n1_idx+1, numpoints):
                    yield (n1_idx, n2_idx)
                yield(n1_idx, -1)
        else:        
            numpoints = self.points_rc.shape[0]
            for pt1_idx in range(0, numpoints): 
                for pt2_idx in range(pt1_idx+1, numpoints):
                    # tan: is this check required? 
                    # after pruning focal points for included pairs, this should always point to a valid pair
                    if (None != self.included_pairs) and (self.included_pairs[pt1_idx+1, pt2_idx+1] != 1):
                        continue
                    yield (pt1_idx, pt2_idx)
                yield(pt1_idx, -1)
        
    def point_pair_idxs_in_component(self, comp, habitat):
        """Returns pairs of point indices that belong to the same component.
        
        Returns (x, -1) to denote end of each first node number.
        """
        if type(habitat) == tuple:
            components, node_map = habitat
        else:
            components = habitat.components
            node_map = habitat.node_map
        
        if self.is_network:
            indices = np.where(components == comp)
            nodes_in_component = node_map[indices]            
            include_list = list(nodes_in_component[:])
            
            numpoints = self.point_ids.size
            for n1_idx in range(0, numpoints-1):
                if self.point_ids[n1_idx] not in include_list:
                    continue
                for n2_idx in range(n1_idx+1, numpoints):
                    if self.point_ids[n2_idx] in include_list:
                        yield (n1_idx, n2_idx)
                yield(n1_idx, -1)
        else:        
            numpoints = self.points_rc.shape[0]
            for pt1_idx in range(0, numpoints): 
                dst = self.get_graph_node_idx(pt1_idx, node_map)
                if (dst <  0 or components[dst] != comp):
                    continue
                for pt2_idx in range(pt1_idx+1, numpoints):
                    # tan: is this check required? 
                    # after pruning focal points for included pairs, this should always point to a valid pair
                    if (None != self.included_pairs) and (self.included_pairs[pt1_idx+1, pt2_idx+1] != 1):
                        continue
                    src = self.get_graph_node_idx(pt2_idx, node_map)
                    if (src >=  0 and components[src] == comp):
                        yield (pt1_idx, pt2_idx)
                yield(pt1_idx, -1)




class CSHabitatGraph:
    def __init__(self, g_map=None, poly_map=None, connect_using_avg_resistances=False, connect_four_neighbors_only=False, g_graph=None, node_names=None):
        if None != g_map:
            self.is_network = False
            self.g_map = g_map
            self.poly_map = poly_map
            self.connect_using_avg_resistances = connect_using_avg_resistances
            self.connect_four_neighbors_only = connect_four_neighbors_only
            
            self.node_map = CSHabitatGraph._construct_node_map(g_map, poly_map)
            (component_map, components) = CSHabitatGraph._construct_component_map(g_map, self.node_map, connect_using_avg_resistances, connect_four_neighbors_only)
            self.component_map = component_map
            self.components = components
            
            self.num_components = components.max()
            self.num_nodes = self.node_map.max()
        else:
            self.is_network = True
            self.g_graph = g_graph          # is the sparse CSR matrix 
            self.node_map = node_names    # list of node names
            
            (_num_components, C) = connected_components(g_graph)
            C += 1
            self.components = C
            
            self.num_components = C.max()
            self.num_nodes = self.node_map.size
    
    def get_graph(self):
        return CSHabitatGraph._construct_g_graph(self.g_map, self.node_map, self.connect_using_avg_resistances, self.connect_four_neighbors_only)
    
    def prune_nodes_for_component(self, keep_component):
        """Removes nodes outside of component being operated on.
        
        Returns node map and adjacency matrix that only include nodes in keep_component.
        """
        if self.is_network:
            del_indices = np.where(self.components != keep_component)
            pruned_graph = CSBase.deleterowcol(self.g_graph, delrow=del_indices, delcol=del_indices)
            indices = np.where(self.components == keep_component)
            nodes_in_component = self.node_map[indices]
            return (pruned_graph, nodes_in_component)                
        else:
            selector = self.component_map == keep_component
            
            g_map_pruned = selector * self.g_map
            poly_map_pruned = []
            if self.poly_map !=  []:
                poly_map_pruned = selector * self.poly_map
    
            node_map_pruned = CSHabitatGraph._construct_node_map(g_map_pruned, poly_map_pruned)
            G_pruned = CSHabitatGraph._construct_g_graph(g_map_pruned, node_map_pruned, self.connect_using_avg_resistances, self.connect_four_neighbors_only)
             
            return (G_pruned, node_map_pruned)
            
    
    def unique_component_with_points(self, point_map):
        components_with_points = self.components_with_points(point_map)
        return None if (components_with_points.size > 1) else components_with_points[0]
        
    def components_with_points(self, point_map):
        if self.is_network:
            raise RuntimeError('Not available in network mode')
        
        sub_component_map = np.where(point_map, self.component_map, 0)
        sub_components = np.unique(sub_component_map)
        return sub_components if (sub_components[0] != 0) else sub_components[1:]

                  
    @staticmethod
    @print_timing
    def _construct_node_map(g_map, poly_map):
        """Creates a grid of node numbers corresponding to raster pixels with non-zero conductances."""  
        node_map = np.zeros(g_map.shape, dtype='int32')
        node_map[g_map.nonzero()] = np.arange(1, np.sum(g_map>0)+1, dtype='int32')

        if poly_map == []:
            return node_map

        # Remove extra points from poly_map that are not in g_map
        poly_map_pruned = np.zeros(g_map.shape, dtype='int32')
        poly_map_pruned[np.where(g_map)] = poly_map[np.where(g_map)]
        
        polynums = np.unique(poly_map)
   
        for i in range(0, polynums.size):
            polynum = polynums[i]
            if polynum !=  0:
                (pi, pj) = np.where(poly_map_pruned == polynum) #
                (pk, pl) = np.where(poly_map == polynum) #Added 040309 BHM                
                if len(pi) > 0:  
                    node_map[pk, pl] = node_map[pi[0], pj[0]] #Modified 040309 BHM  
        node_map[np.where(node_map)] = CSBase.relabel(node_map[np.where(node_map)], 1) #BHM 072409

        return node_map

    @staticmethod
    @print_timing
    def _construct_component_map(g_map, node_map, connect_using_avg_resistances, connect_four_neighbors_only):
        """Assigns component numbers to grid corresponding to pixels with non-zero conductances.
        
        Nodes with the same component number are in single, connected components.
        
        """  
        G = CSHabitatGraph._construct_g_graph(g_map, node_map, connect_using_avg_resistances, connect_four_neighbors_only) 
        (_num_components, C) = connected_components(G)
        C += 1 # Number components from 1

        (I, J) = np.where(node_map)
        nodes = node_map[I, J].flatten()

        component_map = np.zeros(node_map.shape, dtype = 'int32')
        component_map[I, J] = C[nodes-1]

        return (component_map, C)
    
    @staticmethod
    @print_timing
    def _construct_g_graph(g_map, node_map, connect_using_avg_resistances, connect_four_neighbors_only):
        """Construct sparse adjacency matrix given raster maps of conductances and nodes."""
        numnodes = node_map.max()
        (node1, node2, conductances) = CSHabitatGraph._get_conductances(g_map, node_map, connect_using_avg_resistances, connect_four_neighbors_only)
        return CSHabitatGraph._make_sparse_csr(node1, node2, conductances, numnodes)
        
    @staticmethod
    def _make_sparse_csr(node1, node2, conductances, numnodes):
        G = sparse.csr_matrix((conductances, (node1, node2)), shape = (numnodes, numnodes)) # Memory hogging operation?
        g_graph = G + G.T
        
        return g_graph


    @staticmethod
    def _neighbors_horiz(g_map):
        """Returns values of horizontal neighbors in conductance map."""  
        m = g_map.shape[0]
        n = g_map.shape[1]

        g_map_l = g_map[:, 0:(n-1)]
        g_map_r = g_map[:, 1:n]
        g_map_lr = np.double(np.logical_and(g_map_l, g_map_r))
        s_horiz = np.where(np.c_[g_map_lr, np.zeros((m,1), dtype='int32')].flatten())
        t_horiz = np.where(np.c_[np.zeros((m,1), dtype='int32'), g_map_lr].flatten())

        return (s_horiz, t_horiz)

        
    @staticmethod
    def _neighbors_vert(g_map):
        """Returns values of vertical neighbors in conductance map."""  
        m = g_map.shape[0]
        n = g_map.shape[1]

        g_map_u = g_map[0:(m-1), :]
        g_map_d = g_map[1:m    , :]
        g_map_ud = np.double(np.logical_and(g_map_u, g_map_d))
        s_vert = np.where(np.r_[g_map_ud, np.zeros((1,n), dtype='int32')].flatten())
        t_vert = np.where(np.r_[np.zeros((1,n), dtype='int32'), g_map_ud].flatten())
        
        return (s_vert, t_vert)

        
    @staticmethod
    def _neighbors_diag1(g_map):
        """Returns values of 1st diagonal neighbors in conductance map."""  
        m = g_map.shape[0]
        n = g_map.shape[1]

        z1 = np.zeros((m-1, 1), dtype='int32')
        z2 = np.zeros((1  , n), dtype='int32')
        
        g_map_ul  = g_map[0:m-1, 0:n-1]
        g_map_dr  = g_map[1:m  , 1:n  ]
        g_map_udr = np.double(np.logical_and(g_map_ul, g_map_dr)) 
        s_dr      = np.where(np.r_[np.c_[g_map_udr, z1], z2].flatten())
        t_dr      = np.where(np.r_[z2, np.c_[z1, g_map_udr]].flatten())
        
        return (s_dr, t_dr)

        
    @staticmethod
    def _neighbors_diag2(g_map):
        """Returns values of 2nd diagonal neighbors in conductance map."""  
        m = g_map.shape[0]
        n = g_map.shape[1]

        z1 = np.zeros((m-1, 1), dtype='int32')
        z2 = np.zeros((1  , n), dtype='int32')

        g_map_ur  = g_map[0:m-1, 1:n  ]
        g_map_dl  = g_map[1:m  , 0:n-1]
        g_map_udl = np.double(np.logical_and(g_map_ur, g_map_dl)) 
        s_dl      = np.where(np.r_[np.c_[z1, g_map_udl], z2].flatten())
        t_dl      = np.where(np.r_[z2, np.c_[g_map_udl, z1]].flatten())
                        
        return (s_dl, t_dl)
        
    @staticmethod
    def _get_conductances(g_map, node_map, connect_using_avg_resistances, connect_four_neighbors_only):
        """Calculates conductances between adjacent nodes given a raster conductance map.
        
        Returns an adjacency matrix with values representing node-to-node conductance values.
        
        """  
        (s_horiz, t_horiz) = CSHabitatGraph._neighbors_horiz(g_map)
        (s_vert,  t_vert)  = CSHabitatGraph._neighbors_vert(g_map)

        s = np.c_[s_horiz, s_vert].flatten()
        t = np.c_[t_horiz, t_vert].flatten()

        # Conductances
        g1 = g_map.flatten()[s]
        g2 = g_map.flatten()[t]

        if connect_using_avg_resistances == False:
            conductances = (g1+g2)/2
        else:
            conductances = 1 /((1/g1+1/g2)/2)

        if connect_four_neighbors_only == False:
            (s_dr, t_dr) = CSHabitatGraph._neighbors_diag1(g_map)
            (s_dl, t_dl) = CSHabitatGraph._neighbors_diag2(g_map)

            sd = np.c_[s_dr, s_dl].flatten()
            td = np.c_[t_dr, t_dl].flatten()

            # Conductances
            g1 = g_map.flatten()[sd]
            g2 = g_map.flatten()[td]

            if connect_using_avg_resistances == False:
                conductances_d = (g1+g2) / (2*np.sqrt(2))
            else:
                conductances_d =  1 / (np.sqrt(2)*(1/g1 + 1/g2) / 2)

            conductances = np.r_[conductances, conductances_d]

            s = np.r_[s, sd].flatten()
            t = np.r_[t, td].flatten()

        # Nodes in the g_graph. 
        # Subtract 1 for Python's 0-based indexing. Node numbers start from 1
        node1 = node_map.flatten()[s]-1
        node2 = node_map.flatten()[t]-1
        
        return (node1, node2, conductances)


class CSOutput:
    """Handles output of current and voltage maps"""
    def __init__(self, options, state, report_status, g_shape=None):
        self.options = options
        self.state = state
        self.report_status = report_status
        self.g_shape = g_shape
        
        self.is_network = (self.options.data_type == 'network')
        self.scenario = self.options.scenario
        self.voltage_maps = {}
        self.current_maps = {}


    def get_c_map(self, name, remove=False):
        """Get current map identified by name. Remove it from storage if remove is True."""
        ret = self.current_maps.get(name, None)
        if remove:
            self.rm_c_map(name)
        return ret
    
    def rm_c_map(self, name):
        """Remove current map identified by name if present"""
        if self.current_maps.has_key(name):
            del self.current_maps[name]

    def store_max_c_map(self, max_name, name, remove=False):
        """Store the maximum currents into map identified by max_name by comparing it with that identified by name.
        Implemented only for raster mode."""
        self.store_max_c_map_values(max_name, self.current_maps[name])
        if remove:
            self.rm_c_map(name)
            
    def store_max_c_map_values(self, max_name, values):
        self.current_maps[max_name] = np.maximum(self.current_maps[max_name], values)

    def accumulate_c_map_from(self, name, fromname):
        self.accumulate_c_map_with_values(name, self.current_maps[fromname])
    
    def accumulate_c_map_with_values(self, name, values):
        if self.is_network:
            _branch_currents, node_currents, branch_currents_array, node_map = values
            full_branch_currents, full_node_currents, _bca, _np = self.current_maps[name]
            full_node_currents[node_map] += node_currents            
            full_branch_currents = full_branch_currents + sparse.csr_matrix((branch_currents_array[:,2], (branch_currents_array[:,0], branch_currents_array[:,1])), shape=full_branch_currents.shape)
            self.current_maps[name] = (full_branch_currents, full_node_currents, branch_currents_array, node_map)
        else:
            self.current_maps[name] += values
            
    def accumulate_c_map(self, name, voltages, G, node_map, finitegrounds, local_src, local_dst):
        self._write_store_c_map(name, False, False, True, voltages, G, node_map, finitegrounds, local_src, local_dst)

    def store_c_map(self, name, voltages, G, node_map, finitegrounds, local_src, local_dst):
        self._write_store_c_map(name, False, False, False, voltages, G, node_map, finitegrounds, local_src, local_dst)
    
    def write_c_map(self, name, remove=False, voltages=None, G=None, node_map=None, finitegrounds=None, local_src=None, local_dst=None):
        self._write_store_c_map(name, remove, True, False, voltages, G, node_map, finitegrounds, local_src, local_dst)
        
    def _write_store_c_map(self, name, remove, write, accumulate, voltages, G, node_map, finitegrounds, local_src, local_dst):
        if self.is_network:
            if voltages != None:
                (node_currents, branch_currents) = self._create_current_maps(voltages, G, finitegrounds)
                branch_currents_array = CSOutput._convert_graph_to_3_col(branch_currents, node_map)
            else:
                branch_currents, node_currents, branch_currents_array, _node_map = self.current_maps[name]
            
            if write:                
                # Append node names and convert to array format
                node_currents_array = CSOutput._append_names_to_node_currents(node_currents, node_map)                
                CSIO.write_currents(self.options.output_file, branch_currents_array, node_currents_array, name)
                
            if remove:
                self.rm_c_map(name)
            elif accumulate:
                full_branch_currents, full_node_currents, _bca, _np = self.current_maps[name]
                full_node_currents[node_map] += node_currents            
                full_branch_currents = full_branch_currents + sparse.csr_matrix((branch_currents_array[:,2], (branch_currents_array[:,0], branch_currents_array[:,1])), shape=full_branch_currents.shape)
                self.current_maps[name] = (full_branch_currents, full_node_currents, branch_currents_array, node_map)
            else:
                self.current_maps[name] = (branch_currents, node_currents, branch_currents_array, node_map)
        else:
            if voltages != None:
                try:
                    current_map = self._create_current_maps(voltages, G, finitegrounds, node_map)   
                except MemoryError:
                    CSBase.enable_low_memory(False)
                    current_map = self._create_current_maps(voltages, G, finitegrounds, node_map)
            else:
                current_map = self.current_maps[name]                                                                                
    
            if self.options.set_focal_node_currents_to_zero==True:
                # set source and target node currents to zero
                focal_node_pair_map = np.where(node_map == local_src+1, 0, 1)
                focal_node_pair_map = np.where(node_map == local_dst+1, 0, focal_node_pair_map)                                                
                current_map = np.multiply(focal_node_pair_map, current_map)
                del focal_node_pair_map
            
            if write:
                fileadd = name if (name=='') else ('_'+name)
                CSIO.write_aaigrid('curmap', fileadd, self._log_transform(current_map), self.options, self.state)
            if remove:
                self.rm_c_map(name)
            elif accumulate:
                self.current_maps[name] += current_map
            else:
                self.current_maps[name] = current_map


    def alloc_c_map(self, name):
        """Allocate space to store current maps identified by name"""
        if self.is_network:
            branch_currents = sparse.csr_matrix(self.g_shape)
            node_currents = np.zeros((self.g_shape[0], 1), dtype='float64')
            self.current_maps[name] = (branch_currents, node_currents, None, None)
        else:
            self.current_maps[name] = np.zeros((self.state.nrows, self.state.ncols), dtype='float64')


    def _log_transform(self, map_to_transform):
        if self.options.log_transform_maps:
            map_to_transform = np.where(map_to_transform > 0, np.log10(map_to_transform), self.state.nodata)
        return map_to_transform

    def get_v_map(self, name, remove=False):
        """Get voltage map identified by name. Remove it from storage if remove is True."""
        ret = self.voltage_maps.get(name, None)
        if remove:
            self.rm_v_map(name)
        return ret
    
    def rm_v_map(self, name):
        """Delete voltage map allocated with name if present"""
        if self.voltage_maps.has_key(name):
            del self.voltage_maps[name]
        
    def write_v_map(self, name, remove=False, voltages=None, node_map=None):
        """Write voltage map identified by name. Remove the map after that if remove is True.
        If voltages and node_map are provided, create space for voltage map disregarding prior allocation.
        """
        if self.report_status==True:
            logging.info('writing voltage map ' + name)
        if self.is_network:
            if voltages == None:
                voltages, node_map = self.voltage_maps[name]
            CSIO.write_voltages(self.options.output_file, voltages, node_map, name)
        else:
            fileadd = name if (name=='') else ('_'+name)
            if voltages == None:
                vm = self.voltage_maps[name]
            else:
                vm = self._create_voltage_map(node_map, voltages)
            CSIO.write_aaigrid('voltmap', fileadd, vm, self.options, self.state)
            
        if remove:
            self.rm_v_map(name)
        elif voltages != None:
            if self.is_network:
                self.voltage_maps[name] = (voltages, node_map)
            else:
                self.voltage_maps[name] = vm

    def accumulate_v_map(self, name, voltages, node_map):
        """Create and accumulate voltage map into the space identified by name"""
        if self.is_network:
            self.voltage_maps[name] = (voltages, node_map)
        else:
            self.voltage_maps[name] +=  self._create_voltage_map(node_map, voltages)
            
    def alloc_v_map(self, name):
        """Allocate space for a new voltage map with the given name"""
        if self.is_network:
            self.voltage_maps[name] = None
        else:
            self.voltage_maps[name] = np.zeros((self.state.nrows, self.state.ncols), dtype='float64')
        

    @print_timing
    def _create_current_maps(self, voltages, G, finitegrounds, node_map=None):
        """In raster mode, returns raster current map given node voltage vector, adjacency matrix, etc.
        In network mode returns node and branch currents given voltages in arbitrary graphs.
        """  
        gc.collect()
        G =  G.tocoo()
        node_currents = CSOutput._get_node_currents(voltages, G, finitegrounds)
        
        if self.is_network:
            node_currents_col = np.zeros((node_currents.shape[0],1), dtype='float64')
            node_currents_col[:,0] = node_currents[:]
            branch_currents = CSOutput._get_branch_currents(G, voltages, True) 
            branch_currents = np.absolute(branch_currents) 
            return node_currents_col, branch_currents
        else:
            (rows, cols) = np.where(node_map)
            vals = node_map[rows, cols]-1
            current_map = np.zeros((self.state.nrows, self.state.ncols), dtype='float64')
            current_map[rows,cols] = node_currents[vals]    
            return current_map


    @staticmethod
    def _get_node_currents(voltages, G, finitegrounds):
        """Calculates currents at nodes."""  
        node_currents_pos = CSOutput._get_node_currents_posneg(G, voltages, finitegrounds, True) 
        node_currents_neg = CSOutput._get_node_currents_posneg(G, voltages, finitegrounds, False)
        node_currents = np.where(node_currents_neg > node_currents_pos, node_currents_neg, node_currents_pos)

        return np.asarray(node_currents)[0]

    
    @staticmethod
    def _get_node_currents_posneg(G, voltages, finitegrounds, pos):
        """Calculates positive or negative node currents based on pos flag."""  
        branch_currents = CSOutput._get_branch_currents(G, voltages, pos)
        branch_currents = branch_currents - branch_currents.T #Can cause memory error
        
        branch_currents = branch_currents.tocoo() #Can cause memory error, but this and code below more memory efficient than previous version.
        mask = branch_currents.data > 0
        row  = branch_currents.row[mask]
        col  = branch_currents.col[mask]
        data = branch_currents.data[mask]
        del mask
        n = G.shape[0]
        branch_currents = sparse.csr_matrix((data, (row, col)), shape = (n,n))
           
        if finitegrounds[0]!= -9999:  
            finiteground_currents = np.multiply(finitegrounds, voltages)
            if pos:
                finiteground_currents = np.where(finiteground_currents < 0, -finiteground_currents, 0)
            else:
                finiteground_currents = np.where(finiteground_currents > 0, finiteground_currents, 0)  
            n = G.shape[0]
            branch_currents = branch_currents + sparse.spdiags(finiteground_currents.T, 0, n, n)        

        return branch_currents.sum(0)
    
    
    @staticmethod
    def _get_branch_currents(G, voltages, pos):    
        """Calculates branch currents."""  
        branch_currents = CSOutput._get_branch_currents_posneg(G, voltages, pos)
        n = G.shape[0]
        mask = G.row < G.col
        branch_currents = sparse.csr_matrix((branch_currents, (G.row[mask], G.col[mask])), shape = (n,n)) #SQUARE MATRIX, SAME DIMENSIONS AS GRAPH
        return branch_currents


    @staticmethod
    def _get_branch_currents_posneg(G, voltages, pos):
        """Calculates positive or negative node currents based on pos flag."""  
        mask = G.row < G.col
        if pos:
            vdiff = voltages[G.row[mask]]              
            vdiff -=  voltages[G.col[mask]]             
        else:
            vdiff = voltages[G.col[mask]]              
            vdiff -=  voltages[G.row[mask]]             

        conductances = np.where(G.data[mask] < 0, -G.data[mask], 0)
        del mask
        
        branch_currents = np.asarray(np.multiply(conductances, vdiff.T)).flatten()
        maxcur = max(branch_currents)
        branch_currents = np.where(np.absolute(branch_currents/maxcur) < 1e-8, 0, branch_currents) #Delete very small branch currents to save memory
        return branch_currents

    @print_timing
    def _create_voltage_map(self, node_map, voltages):
        """Creates raster map of voltages given node voltage vector."""
        voltage_map = np.zeros((self.state.nrows, self.state.ncols), dtype = 'float64')
        ind = node_map > 0
        voltage_map[np.where(ind)] = np.asarray(voltages[node_map[ind]-1]).flatten()
        return voltage_map

    @staticmethod
    def _convert_graph_to_3_col(graph, node_names): 
        """Converts a sparse adjacency matrix to 3-column format."""  
        Gcoo =  graph.tocoo()
        mask = Gcoo.data > 0
        
        graph_n_col = np.zeros((Gcoo.row[mask].size, 3), dtype="float64") #Fixme: this may result in zero-current nodes being left out.  Needed to make change so dimensions would match Gcoo.data[mask]
        
        if node_names == None:
            graph_n_col[:,0] = Gcoo.row[mask]
            graph_n_col[:,1] = Gcoo.col[mask]
        else:
            graph_n_col[:,0] = node_names[Gcoo.row[mask]]
            graph_n_col[:,1] = node_names[Gcoo.col[mask]]
        graph_n_col[:,2] = Gcoo.data[mask]
        return graph_n_col


    @staticmethod
    def _append_names_to_node_currents(node_currents, node_names):
        """Adds names of focal nodes to node current lists."""    
        output_node_currents = np.zeros((len(node_currents),2), dtype='float64')
        output_node_currents[:,0] = node_names[:]
        try:
            output_node_currents[:,1] = node_currents[:,0]
        except:
            output_node_currents[:,1] = node_currents[:]
        return output_node_currents


