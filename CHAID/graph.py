from graphviz import Digraph
import datetime
import time
import plotly.graph_objs as go
import plotly.io as pio
import colorlover as cl
import os

class Graph(object):
    """
    Visualisation of the tree

    Parameters
    ----------
    tree : iterable CHAID tree
    """

    def __init__(self, tree):
        self.tree = tree
        self.files = []

    def render(self, path, view):
        g = Digraph(format='png')
        for node in self.tree:
            m, p, score = node.members, None, None
            if node.p is not None and node.score is not None:
                p = str(round(node.p, 5))
                score = str(round(node.score, 2))
            g.node(str(node.node_id), '', {'shape': 'plaintext', 'image': self.bar_chart(
                m, node.is_terminal, node.node_id == 0, p, score, node.split.column), 'labelloc': 'b'})
            if node.parent is not None:
                edge_label = '   ( ' + ', '.join(node.choices) + ')'
                g.edge(str(node.parent), str(node.node_id), label=edge_label)
        g.graph_attr['splines'] = 'ortho'
        g.render(
            'trees/' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.gv'
            if path is None
            else path,
            view=view
        )
        self.remove_tmp_files()

    def bar_chart(self, members, is_terminal, is_root, p, score, split):
        fig = {
            "data": [
              {
                  "values": [v for v in members.values()],
                  "labels": [k for k in members.keys()],
                  "domain": {"x": [0, 1], "y":[0.4, 1.0]},
                  "hole": .4,
                  "type": "pie",
                  'showlegend': True if is_root else False,
                  'marker': {'colors': cl.scales['5']['qual']['Set1']}
              }],
            "layout": {
                "margin": dict(t=50),
                "annotations": [
                    {
                        "y": {'domain': [0, 0.2]},
                        "font": {
                            "size": 18
                        },
                        "showarrow": False,
                        "text": '',
                        "x": 0.5,
                        "y": 0.5
                    },
                    {
                        "y": {'domain': [0, 0.2]},
                    }
                ]
            }
        }
        if is_terminal is False: self.append_table(fig, [p, score, split])
        file = '/tmp/' + ("%.20f" % time.time()).replace('.', '') + '.png'
        pio.write_image(fig, file=file, format='png')
        self.files.append(file)
        return file

    def append_table(self, fig, table_scores):
        table = go.Table(
            domain=dict(x=[0.3, 0.7], y=[0, 0.37]),
            header=dict(height=0, line = dict(color = 'white'),
                        fill = dict(color = 'white')),
            cells=dict(values=[['<i>p</i>', 'score', 'splitting on'], table_scores],
                       line=dict(color='#FFF'), align=['left'] * 5,
                       font=dict(color=['rgb(40, 40, 40)'] * 5, size=12), height=27,
                       fill=dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
        )
        fig['data'].append(table)

    def remove_tmp_files(self):
        [os.remove(file) for file in self.files]
