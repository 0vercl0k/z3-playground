#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygraphviz as pgv
from z3 import *
import sys

def min_dom_set(graph):
    """Try to dominate the graph with the least number of verticies possible"""
    s = Optimize()
    nodes_colors = dict((node_name, Int('k%r' % node_name)) for node_name in graph.nodes())
    for node in graph.nodes():
           s.add(And(nodes_colors[node] >= 0, nodes_colors[node] <= 1))
           dom_neighbor  = Sum ([ (nodes_colors[j]) for j in graph.neighbors(node) ])
           s.add(Sum(nodes_colors[node], dom_neighbor ) >=1)
    s.minimize( Sum([ nodes_colors[y] for y in graph.nodes()]) )

    if s.check() == unsat:
        pass
    else:
        m = s.model()
        return dict((name, m[color].as_long()) for name, color in nodes_colors.iteritems())

    raise Exception('Could not find a solution.')

def build_peternson_3_coloring_graph():
    """Build http://en.wikipedia.org/wiki/File:Petersen_graph_3-coloring.svg"""
    G = pgv.AGraph()
    G.node_attr['style'] = 'filled'
    # Hum, the attribute 'directed' (in AGraph constructor) doesn't seem to work, so that's my workaround.
    G.edge_attr['dir'] = 'none'

    edges = [
        (0, 2), (0, 1), (0, 5), (0, 4), (1, 6), (1, 7),
        (2, 3), (2, 8), (3, 4), (3, 7), (4, 5), (4, 6),
        (5, 9), (6, 8), (7, 9), (8, 9), (9, 3)
    ]

    for i in range(10):
        G.add_node(i)

    for src, dst in edges:
        G.add_edge(src, dst)

    return (G, 'peternson_3_coloring_graph', 'circo')

def build_fat_graph():
    """Build http://www.graphviz.org/content/twopi2"""
    G = pgv.AGraph('graph_coloring_z3_example_fat_graph.gv')
    return (G, 'twopi2_fat_graph', 'twopi')

def main(argc, argv):
    print 'Building the graph..'

    Gs = [
        build_peternson_3_coloring_graph(),
        build_fat_graph()
    ]

    for G, name, layout in Gs:
        print 'Trying to min dom set  %s now (%d nodes, %d edges)..' % (repr(name), G.number_of_nodes(), G.number_of_edges())
        t1 = time.time()
        s = min_dom_set(G)
        t2 = time.time()
        print 'OK, found a solution with %d dominators' % sum( s.values())
        print 'Here is the solution (in %ds):' % (t2 - t1)
        if len(s) < 20:
            print s
        else:
            print 'Too long, see the .png!'

        print 'Setting the dominating nodes..'
        color_available = [
            'red',
            'blue',
            'green',
            'pink'
        ]

        for node in G.nodes_iter():
            n = G.get_node(node)
            n.attr['color'] = color_available[s[node]]

        print 'Saving it in the current directory with the layout %s..' % repr(layout)
        G.layout(layout)
        G.draw('./min_dom_set_z3_%s_dominated.png' % name)
        print '---'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
