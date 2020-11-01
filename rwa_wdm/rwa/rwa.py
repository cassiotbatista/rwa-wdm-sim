from typing import Union

import numpy as np

from ..net import Lightpath, Network
from .routing import dijkstra, yen
from .wlassignment import vertex_coloring, first_fit


def dijkstra_vertex_coloring(net: Network, k: int) -> Union[Lightpath, None]:
    route = dijkstra(net.a, net.s, net.d)
    wavelength = vertex_coloring(net, Lightpath(route, None))
    if wavelength is not None and wavelength < net._num_channels:  # FIXME
        return Lightpath(route, wavelength)
    return None


def dijkstra_first_fit(net: Network, k: int) -> Union[Lightpath, None]:
    route = dijkstra(net.a, net.s, net.d)
    wavelength = first_fit(net, route)
    if wavelength is not None and wavelength < net._num_channels:  # FIXME
        return Lightpath(route, wavelength)
    return None


def yen_vertex_coloring(net: Network, k: int) -> Union[Lightpath, None]:
    routes = yen(net.a, net.s, net.d, k)
    for route in routes:
        wavelength = vertex_coloring(net, Lightpath(route, None))
        if wavelength is not None and wavelength < net._num_channels:  # FIXME
            return Lightpath(route, wavelength)
    return None


def yen_first_fit(net: Network, k: int) -> Union[Lightpath, None]:
    routes = yen(net.a, net.s, net.d, k)
    for route in routes:
        wavelength = first_fit(net, route)
        if wavelength is not None and wavelength < net._num_channels:  # FIXME
            return Lightpath(route, wavelength)
    return None
