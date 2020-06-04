# RWA simulator in C

This code was devloped to be a faster serial version to run in CPU, in order to
later be ported to NVIDIA GPUs via CUDA API.

However this code is not functional by any means. Valgrind accuses some memory
leaks of 5 kB per GA generation. Therefore use it at your own volition.
