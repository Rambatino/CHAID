from graphviz import Digraph
import datetime

class Graph(object):
    """
    Visualisation of the tree

    Parameters
    ----------
    tree : iterable CHAID tree
    """
    def __init__(self, tree):
        self.tree = tree

    def render(self, path, view):
        g = Digraph()
        for node in self.tree:
            m = node.members
            node_info = '\n'.join([ "{}: {}".format(x, int(m[x])) for x in m ])
            node_info += '\n--------\n'
            if node.p is not None and node.score is not None:
                node_info += "p={}\nscore={}\n".format(round(node.p, 5), round(node.score, 2))
            if node.split.column is not None:
                node_info += '--------\n'
                node_info += node.split.column
            g.node(str(node.node_id), node_info)
            if node.parent is not None:
                edge_label = ' ' + '\n'.join(node.choices)
                g.edge(str(node.parent), str(node.node_id), label=edge_label, )

        g.node_attr['shape'] = 'rectangle'

        g.render(
            'trees/' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.gv'
            if path is None
            else path,
            view=view
        )
