all:
	gcc -L ./fann/src -I ./fann/src/include -o train main.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o test test.c -lfann -lm

fann_lib:
	cc -fPIC -shared -o fann.so -L ./fann/src -I ./fann/src/include ./fann/src/fann.c -lfann -lm