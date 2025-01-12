#include "fann.h"

#define MAX_TEMP    50
#define MIN_TEMP    -20
#define MAX_PRICE   20
#define MIN_PRICE   -20

/***************************************************
 Normalise between +1/-0
***************************************************/
void normalise_temperature(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = (((arr[i] - MIN_TEMP)/(MAX_TEMP - MIN_TEMP)) * 2) - 1;
    }
}

/***************************************************
 Normalise between ±1
***************************************************/
void normalise_price(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = (((arr[i] - MIN_PRICE)/(MAX_PRICE - MIN_PRICE)) * 2) - 1;
    }
}

/***************************************************
 Denormalise Price
***************************************************/
void denormalise_price(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = ((arr[i] + 1) / 2) * (MAX_PRICE - MIN_PRICE) + MIN_PRICE;
    }
}

int main(){
    unsigned int num_input = 7;
    unsigned int num_output = 7;
	enum fann_activationfunc_enum activation[3];
	fann_type steepness[10];
    struct fann *ann;
    struct fann_train_data *train_data, *test_data_2023, *test_data_2024;
	unsigned int bit_fail_train, bit_fail_test;
	float mse_train, mse_test;
    
    fann_type predict[7] = {(-1+3.3)/2,(-1.8+2)/2,(-1.5+4.4)/2,(0.4+5.4)/2,(1.2+6.5)/2,(2.4+4.5)/2,(0.2+4.)/2};
    normalise_temperature(&(predict[0]), 7);
    
    train_data = fann_read_train_from_file("gas_train_2024.data");
    
    num_input = train_data->num_input;
    num_output = train_data->num_output;
    
    // Normalise the training data
    for(int i=0; i<train_data->num_data; i++){
        normalise_temperature(&(train_data->input[i][0]),num_input);
        
        normalise_price(&(train_data->output[i][0]), num_output);
    }
    
    // ann = fann_create_shortcut(2, fann_num_input_train_data(train_data), fann_num_output_train_data(train_data));
    ann = fann_create_standard(4, num_input, 64,32, num_output);
    
    // fann_init_weights(ann, train_data);

    // fann_set_training_algorithm(ann, FANN_TRAIN_RPROP);
    fann_set_training_algorithm(ann, FANN_TRAIN_INCREMENTAL);
    fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC);
    fann_set_activation_function_output(ann, FANN_SIGMOID_SYMMETRIC);
    // fann_set_train_error_function(ann, FANN_ERRORFUNC_LINEAR);
    
    fann_set_activation_steepness_hidden(ann,0.25);
	fann_set_learning_momentum(ann, 0.4);
	
	fann_set_bit_fail_limit(ann, (fann_type)0.01);
	fann_set_train_stop_function(ann, FANN_STOPFUNC_BIT);
	fann_print_parameters(ann);
	
	printf("Training network.\n");

	// fann_cascadetrain_on_data(ann, train_data, 300, 1, 0.0001);
    fann_train_on_data(ann, train_data, 1000000, 1, 0.001);
	
	mse_train = fann_test_data(ann, train_data);
	bit_fail_train = fann_get_bit_fail(ann);
	mse_test = fann_test_data(ann, train_data);
	bit_fail_test = fann_get_bit_fail(ann);
	
	printf("\nTrain error: %f, Train bit-fail: %d, Test error: %f, Test bit-fail: %d\n\n", 
		   mse_train, bit_fail_train, mse_test, bit_fail_test);
           
	// mse_test = fann_test_data(ann, test_data_2024);
	// bit_fail_test = fann_get_bit_fail(ann);
	
	// printf("\nTrain error: %f, Train bit-fail: %d, Test error: %f, Test bit-fail: %d\n\n", 
		   // mse_train, bit_fail_train, mse_test, bit_fail_test);
	
	// fann_print_connections(ann);

    fann_save(ann, "gas_trained.net");
    
    fann_type *calc_out = fann_run(ann, (fann_type*)&(predict[0]));
    
    denormalise_price(calc_out,num_output);
    
    printf("Predict Tod: %f (%f)\n", *(calc_out+0), *(calc_out+0)+ 1.3167);
    printf("Predict Tom: %f (%f)\n", *(calc_out+1), *(calc_out+1)+ 1.3167);
    printf("Predict +2d: %f (%f)\n", *(calc_out+2), *(calc_out+2)+ 1.3167);
    printf("Predict +3d: %f (%f)\n", *(calc_out+3), *(calc_out+3)+ 1.3167);
    printf("Predict +4d: %f (%f)\n", *(calc_out+4), *(calc_out+4)+ 1.3167);
    printf("Predict +5d: %f (%f)\n", *(calc_out+5), *(calc_out+5)+ 1.3167);
    printf("Predict : %f (%f)\n", *(calc_out+6), *(calc_out+6)+ 1.3167);

    fann_destroy(ann);

    return 0;
}