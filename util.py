import rls
import peripherals
import sys

def get_reversible_set(ls_u, ls_v):
    ''' ([[]], [[]],) -> [set]
    Returns the intersection between ls_u and ls_v that forms
    the reversible set R(u,v).
    R(u,v) is the set of vertices which lie on a shortest path
    between u and v.
    '''
    h_u = len(ls_u)
    
    return [ set(ls_v[i]).intersection(ls_u[h_u - i - 1])
           for i in range(h_u) ]


def get_min_degree_node(m):
    ''' ([[]]) -> int '''

    dimension = m.get_dimension()

    import numpy
    min_degree_node = 0
    min_degree = m.get_degree(0)

    for i in range(dimension):
        degree = m.get_degree(i)
        if degree < min_degree:
            #print '{} < {}'.format(degree, min_degree)
            min_degree = degree
            min_degree_node = i
    
    #print 'min degree node: {}'.format(min_degree_node)
    return min_degree_node




def min_degree_node_from_set (mat, set):
    dimension = mat.get_dimension()
    min_degree = dimension
    min_degree_node = 0

    for n in set:
        degree = mat.get_degree(n)
        if degree < min_degree:
            min_degree = degree
            min_degree_node = n

    return min_degree_node
    

def grow_set_and_check_peripherals(m, set, min_width = False, initial_p = None):
    ''' ([[]], list or set, bool) -> Peripheral '''

    p = peripherals.Peripherals(0, 0, 0) if not initial_p else initial_p
    
    width_limit = m.get_dimension()
  
    set_size = len(set)
    print 'growing set size', len(set)

    iter = 0
    if min_width:
        for x in set:
            rls_x = rls.buildRLS(m, x, max_w = width_limit)
            #print (rls_x.levelsArray if rls_x else "a")
            if rls_x:
                width_limit = rls_x.width()
                p_x = peripherals.Peripherals(x,
                                             rls_x.lastLevel()[0], 
                                             rls_x.numLevels() - 1)
                if p_x.diameter >= p.diameter:
                    #print 'min_width:', width_limit 
                    p.copy(p_x) 

            iter += 1
            percentage = 100 * float(iter)/set_size
            sys.stdout.write("\r{} / {} - {:0.2f}%".format(iter,set_size,percentage))
            sys.stdout.flush()
    else: 
        for x in set:
            rls_x = rls.buildRLS(m, x)
            p_x = peripherals.Peripherals(x, rls_x.lastLevel()[0], rls_x.numLevels() - 1)

            if p_x.diameter > p.diameter:
                p.copy(p_x)
    
    return p


def return_most_peripheral(u, rls_u, v, rls_v):
    p_u = peripherals.Peripherals(u, rls_u.lastLevel()[0], rls_u.numLevels() - 1)
    p_v = peripherals.Peripherals(u, rls_v.lastLevel()[0], rls_v.numLevels() - 1)

    if p_u.diameter > p_v:
        return p_u
    return p_v



