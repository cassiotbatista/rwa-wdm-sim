all:
	gcc -g -O3 -o sim_rwa sim_rwa.c list.c nsf.c rwa_ga.c -lm
debug:
	valgrind ./sim_rwa
