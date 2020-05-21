all:
	gcc -g -o sim_rwa sim_rwa.c list.c nsf.c rwa_ga.c -lm

gdb:
	make all
	gdb ./sim_rwa

clean:
	rm sim_rwa

val:
	make all
	valgrind -v ./sim_rwa
