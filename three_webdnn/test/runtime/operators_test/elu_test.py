import numpy as np

from test.util import generate_kernel_test_case, wrap_template
from webdnn.graph.graph import Graph
from webdnn.graph.operators.elu import Elu
from webdnn.graph.order import OrderNHWC, OrderNCHW
from webdnn.graph.variable import Variable


@wrap_template
def template(x_order=OrderNHWC, y_order=OrderNHWC, description: str = ""):
    vx = np.random.rand(2, 3, 4, 5) - 0.5
    vy = vx.copy()
    vy[vx < 0] = np.exp(vy[vx < 0]) - 1

    x = Variable(vx.shape, order=OrderNHWC)
    y, = Elu(None)(x)

    x.change_order(x_order)
    y.change_order(y_order)

    generate_kernel_test_case(
        description=f"Elu {description}",
        graph=Graph([x], [y]),
        inputs={x: np.transpose(vx, [OrderNHWC.axes_dict[a] for a in x.order.axes])},
        expected={y: np.transpose(vy, [OrderNHWC.axes_dict[a] for a in y.order.axes])},
        EPS=1e-2
    )


def test():
    template()


def test_different_order():
    template(x_order=OrderNCHW)
