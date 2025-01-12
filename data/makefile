all:
	gcc -L ./fann/src -I ./fann/src/include -o electric_train electric_train.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o electric_test electric_test.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o gas_train gas_train.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o gas_test gas_test.c -lfann -lm
	
electric:
	gcc -L ./fann/src -I ./fann/src/include -o electric_train electric_train.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o electric_test electric_test.c -lfann -lm	   
	
gas:
	gcc -L ./fann/src -I ./fann/src/include -o gas_train gas_train.c -lfann -lm
	gcc -L ./fann/src -I ./fann/src/include -o gas_test gas_test.c -lfann -lm

fann_lib:
	cc -fPIC -shared -o fann.so -L ./fann/src -I ./fann/src/include ./fann/src/fann.c -lfann -lm