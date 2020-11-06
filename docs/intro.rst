Introduction
============

``rwa_wdm`` implements some mainstream algorithms for both routing and
wavelength assignment subproblems as standalone packages, such as Dijkstra and
Yen, and first-fit, random-fit, and vertex-coloring, respectively.

Besides, a self-made genetic algorithms is also implemented to solve the RWA
problem.

.. contents::
   :local:


Features
--------

``rwa_wdm`` is supports the following algorithms for RWA:

* Routing algorithms

    * Dijkstra

    * Yen

* Wavelength assignment algorithms

    * First-fit

    * Random-fit

    * Vertex-coloring

* RWA as one

    * Genetic algorithm with GOF


Installation
------------

You can install ``rwa_wdm`` directly from Python Package Index via ``pip``::

  $ pip install rwa_wdm

Alternatively, you can build it from source::

  $ git clone https://github.com/cassiobatista/rwa-wdm-sim
  $ cd rwa-wdm-sim/
  $ python setup.py install --skip-build


Example usage and output
------------------------

``rwa_wdm`` offers the possibility to be execute as a Python module via ``-m``
flag. To run Dijkstra's algorithm for routing and first-fit heuristics for
wavelength assignment, just provide both ``-r`` and ``-w`` flags to ``rwa_wdm``
command line utility::

  $ python -m rwa_wdm -r dijkstra -w first-fit -s 5
  [2020-11-05 10:35:56] [__main__] INFO     Simulating 150 connection requests over nsf topology with 8 λ per link using dijkstra + first-fit combination as RWA algorithm
  Load:      1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30 
  Blocks: 0001 0000 0000 0004 0008 0022 0024 0034 0031 0057 0048 0055 0055 0057 0077 0098 0093 0082 0087 0092 0098 0097 0091 0111 0106 0128 0105 0118 0120 0115 
  BP (%):  0.7  0.0  0.0  2.7  5.3 14.7 16.0 22.7 20.7 38.0 32.0 36.7 36.7 38.0 51.3 65.3 62.0 54.7 58.0 61.3 65.3 64.7 60.7 74.0 70.7 85.3 70.0 78.7 80.0 76.7 [sim 1: 7.68 secs]
  [2020-11-05 10:36:04] [io] INFO     Creating result dir in /tmp/rwa_results
  [2020-11-05 10:36:04] [io] INFO     Writing blocking probability results to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.bp"
  Blocks: 0000 0000 0002 0000 0010 0024 0021 0041 0039 0061 0050 0070 0060 0066 0079 0081 0085 0083 0108 0087 0089 0117 0103 0108 0105 0103 0095 0098 0114 0113 
  BP (%):  0.0  0.0  1.3  0.0  6.7 16.0 14.0 27.3 26.0 40.7 33.3 46.7 40.0 44.0 52.7 54.0 56.7 55.3 72.0 58.0 59.3 78.0 68.7 72.0 70.0 68.7 63.3 65.3 76.0 75.3 [sim 2: 7.54 secs]
  [2020-11-05 10:36:11] [io] INFO     Writing blocking probability results to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.bp"
  Blocks: 0000 0000 0001 0000 0001 0016 0024 0031 0054 0056 0049 0071 0074 0080 0066 0089 0086 0085 0095 0092 0089 0103 0101 0104 0107 0105 0106 0104 0115 0119 
  BP (%):  0.0  0.0  0.7  0.0  0.7 10.7 16.0 20.7 36.0 37.3 32.7 47.3 49.3 53.3 44.0 59.3 57.3 56.7 63.3 61.3 59.3 68.7 67.3 69.3 71.3 70.0 70.7 69.3 76.7 79.3 [sim 3: 7.58 secs]
  [2020-11-05 10:36:19] [io] INFO     Writing blocking probability results to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.bp"
  Blocks: 0000 0000 0000 0011 0015 0015 0010 0022 0063 0055 0075 0064 0072 0088 0071 0081 0083 0085 0109 0094 0088 0100 0104 0103 0107 0097 0108 0108 0100 0100 
  BP (%):  0.0  0.0  0.0  7.3 10.0 10.0  6.7 14.7 42.0 36.7 50.0 42.7 48.0 58.7 47.3 54.0 55.3 56.7 72.7 62.7 58.7 66.7 69.3 68.7 71.3 64.7 72.0 72.0 66.7 66.7 [sim 4: 7.56 secs]
  [2020-11-05 10:36:26] [io] INFO     Writing blocking probability results to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.bp"
  Blocks: 0001 0000 0000 0007 0016 0015 0021 0032 0048 0040 0061 0064 0071 0068 0070 0082 0076 0100 0101 0093 0106 0116 0103 0103 0109 0109 0100 0120 0121 0108 
  BP (%):  0.7  0.0  0.0  4.7 10.7 10.0 14.0 21.3 32.0 26.7 40.7 42.7 47.3 45.3 46.7 54.7 50.7 66.7 67.3 62.0 70.7 77.3 68.7 68.7 72.7 72.7 66.7 80.0 80.7 72.0 [sim 5: 7.59 secs]
  [2020-11-05 10:36:34] [io] INFO     Writing blocking probability results to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.bp"
  [2020-11-05 10:37:13] [io] INFO     Writing simulation profiling times to file "/tmp/rwa_results/dijkstra_first-fit_8ch_150req_nsf.it"

A quick help list is also available on the command line interface::

  $ python -m rwa_wdm -h
  usage: python -m rwa_wdm [-h] [-r <alg> -w <alg> | --rwa <alg>] [options]
  
  RWA WDM Simulator: routing and wavelength assignment simulator for WDM networks
  
  optional arguments:
    -h, --help               show this help message and exit
  
  Network options:
    -t <topology>            network topology (default: nsf)
    -c <channels>            number of λ per link (default: 8)
  
  RWA algorithms options:
    -r <algorithm>           routing algorithm (default: None)
    -w <algorithm>           wavelength assignment algorithm (default: None)
    --rwa <algorithm>        routing *and* wavelength assigment algorithm (default: None)
    -y <yen-alt-paths>       number of routing alternate paths (Yen's) (default: 2)
  
  RWA simulator options:
    -l <max-load>            maximum network load, in Erlangs (default: 30)
    -k <conn-requests>       number of connection requests to arrive (default: 150)
    -d <result-dir>          dir to store blocking probability results (default: /tmp/rwa_results)
    -s <num-simulations>     number of times to run the simulation (default: 1)
    -p                       plot blocking probability graph after simulation? (default: False)
  
  Genetic algorithm options:
    --pop-size POP_SIZE      number of individuals in the population (default: 25)
    --num-gen NUM_GEN        number of generations for population to evolve (default: 25)
    --cross-rate CROSS_RATE  crossover rate (default: 0.4)
    --mut-rate MUT_RATE      mutation rate (default: 0.02)

