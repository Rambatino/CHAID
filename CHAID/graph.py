import os
from datetime import datetime

import plotly.graph_objs as go
import plotly.io as pio
import colorlover as cl
from graphviz import Digraph

try:
    # Python 3.2 and newer
    from tempfile import TemporaryDirectory
except ImportError:
    # minimal backport of TemporaryDirectory for Python 2.7, sufficient
    # for use with this module.
    import shutil
    from tempfile import mkdtemp
    class TemporaryDirectory(object):
        def __init__(self):
            self.name = mkdtemp()
        def __enter__(self):
            return self.name
        def __exit__(self, *args):
            shutil.rmtree(self.name, ignore_errors=True)

FIG_BASE = {
    "layout": {
        "margin_t": 50,
        "annotations": [{"font_size": 18, "x": 0.5, "y": 0.5}, {"y": [0, 0.2]}],
    },
}
FIG_BASE_DATA = {
    "domain": {"x": [0, 1], "y": [0.4, 1.0]},
    "hole": 0.4,
    "type": "pie",
    "marker_colors": cl.scales["5"]["qual"]["Set1"],
}
TABLE_HEADER = ["<i>p</i>", "score", "splitting on"]
TABLE_CONFIG = {
    "domain": {"x": [0.3, 0.7], "y": [0, 0.37]},
    "header": {"fill_color": "#FFF"},
}
TABLE_CELLS_CONFIG = {
    "line_color": "#FFF",
    "align": "left",
    "font_color": "#282828",
    "height": 27,
    "fill_color": ["#EBC1EE", "#EDEAFB"],
}

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
        if path is None:
            path = os.path.join("trees", "{:%Y-%m-%d %H:%M:%S}.gv".format(datetime.now()))
        with TemporaryDirectory() as self.tempdir:
            g = Digraph(
                format="png",
                graph_attr={"splines": "ortho"},
                node_attr={"shape": "plaintext", "labelloc": "b"},
            )
            for node in self.tree:
                image = self.bar_chart(node)
                g.node(str(node.node_id), image=image)
                if node.parent is not None:
                    edge_label = "     ({})     \n ".format(', '.join(map(str, node.choices)))
                    g.edge(str(node.parent), str(node.node_id), xlabel=edge_label)
            g.render(path, view=view)

    def bar_chart(self, node):
        fig = dict(
            data=[
                dict(
                    values=list(node.members.values()),
                    labels=list(node.members),
                    showlegend=(node.node_id == 0),
                    **FIG_BASE_DATA
                )
            ],
            **FIG_BASE
        )

        if not node.is_terminal:
            fig["data"].append(self._table(node))

        filename = os.path.join(self.tempdir, "node-{}.png".format(node.node_id))
        pio.write_image(fig, file=filename, format="png")
        return filename

    def _table(self, node):
        p = None if node.p is None else format(node.p, ".5f")
        score = None if node.score is None else format(node.score, ".2f")
        values = [p, score, node.split.column]
        return go.Table(
            cells=dict(values=[TABLE_HEADER, values], **TABLE_CELLS_CONFIG),
            **TABLE_CONFIG
        )
