from typing import Callable, Union

import numpy as np

from ..net import Lightpath, Network
from .routing import dijkstra, yen
from .wlassignment import vertex_coloring, first_fit
from .ga import GeneticAlgorithm

# genetic algorithm object (globa)
ga = None  # FIXME this seems bad. perhaps this rwa script should be a class


def dijkstra_vertex_coloring(net: Network, k: int) -> Union[Lightpath, None]:
    route = dijkstra(net.a, net.s, net.d)
    wavelength = vertex_coloring(net, Lightpath(route, None))
    if wavelength is not None and wavelength < net.nchannels:
        return Lightpath(route, wavelength)
    return None


def dijkstra_first_fit(net: Network, k: int) -> Union[Lightpath, None]:
    route = dijkstra(net.a, net.s, net.d)
    wavelength = first_fit(net, route)
    if wavelength is not None and wavelength < net.nchannels:
        return Lightpath(route, wavelength)
    return None


def yen_vertex_coloring(net: Network, k: int) -> Union[Lightpath, None]:
    routes = yen(net.a, net.s, net.d, k)
    for route in routes:
        wavelength = vertex_coloring(net, Lightpath(route, None))
        if wavelength is not None and wavelength < net.nchannels:
            return Lightpath(route, wavelength)
    return None


def yen_first_fit(net: Network, k: int) -> Union[Lightpath, None]:
    routes = yen(net.a, net.s, net.d, k)
    for route in routes:
        wavelength = first_fit(net, route)
        if wavelength is not None and wavelength < net.nchannels:
            return Lightpath(route, wavelength)
    return None


def genetic_algorithm_callback(net: Network, k: int) -> Union[Lightpath, None]:
    global ga
    route, wavelength = ga.run(net, k)
    if wavelength is not None and wavelength < net.nchannels:
        return Lightpath(route, wavelength)
    return None


def genetic_algorithm(pop_size: int, num_gen: int,
                      cross_rate: float, mut_rate: float) -> Callable:
    global ga
    ga = GeneticAlgorithm(pop_size, num_gen, cross_rate, mut_rate)
    return genetic_algorithm_callback
