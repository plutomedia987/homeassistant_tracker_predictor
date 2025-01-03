#include "fann.h"

#define MAX_WIND    30000
#define MIN_WIND    0
#define MAX_SOLAR   15000
#define MIN_SOLAR   0
#define MAX_DEMAND  60000
#define MIN_DEMAND  10000
#define MAX_PRICE   100
#define MIN_PRICE   -20

/***************************************************
 Normalise between +1/-0
***************************************************/
void normalise_wind(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = ((arr[i] - MIN_WIND)/(MAX_WIND - MIN_WIND));
    }
}

/***************************************************
 Normalise between +1/-0
***************************************************/
void normalise_solar(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = ((arr[i] - MIN_SOLAR)/(MAX_SOLAR - MIN_SOLAR));
    }
}

/***************************************************
 Normalise between +1/-0
***************************************************/
void normalise_demand(fann_type *arr, int num_inputs){
    for(int i=0; i<num_inputs; i++){
        arr[i] = ((arr[i] - MIN_DEMAND)/(MAX_DEMAND - MIN_DEMAND));
    }
}

/***************************************************
 Normalise between ±1
***************************************************/
void normalise_price(fann_type *arr){
    *arr = (((*arr - MIN_PRICE)/(MAX_PRICE - MIN_PRICE)) * 2) - 1;
}

/***************************************************
 Denormalise Price
***************************************************/
void denormalise_price(fann_type *arr){
    // *arr = (((*arr - MIN_PRICE)/(MAX_PRICE - MIN_PRICE)) * 2) - 1;
    
    *arr = ((*arr + 1) / 2) * (MAX_PRICE - MIN_PRICE) + MIN_PRICE;
}

int main(){
    const unsigned int num_input = 36;
    const unsigned int num_output = 1;
    const unsigned int num_layers = 3;
    const unsigned int num_hidden = 100;
	enum fann_activationfunc_enum activation[3];
	fann_type steepness[10];
    struct fann *ann;
    struct fann_train_data *train_data, *test_data_2023, *test_data_2024;
	unsigned int bit_fail_train, bit_fail_test;
	float mse_train, mse_test;
    
    const float predict[36] = {9044, 8593, 8777, 9680, 9808, 9985, 10206, 10418, 10538, 10837, 11672, 12468, 0, 0, 0, 0, 0, 2160, 4608, 3066, 121, 0, 0, 0, 23200, 22306, 21071, 24358, 31899, 33039, 32720, 33902, 36939, 39194, 37067, 31167};

    // struct fann *ann = fann_create_standard(num_layers, num_input, 20, num_output);
    
    // fann_set_activation_function_hidden(ann, FANN_SIGMOID);
    // fann_set_activation_function_output(ann, FANN_SIGMOID);

    // fann_train_on_file(ann, "train.data", 10000, 500000, 0.001);

    train_data = fann_read_train_from_file("train.data");
    test_data_2023 = fann_read_train_from_file("test_2023.data");
    test_data_2024 = fann_read_train_from_file("test_2024.data");
    
    // Normalise the training data
    for(int i=0; i<train_data->num_data; i++){
        normalise_wind(&(train_data->input[i][0]),12);
        normalise_solar(&(train_data->input[i][12]),12);
        normalise_demand(&(train_data->input[i][24]),12);
        
        normalise_price(&(train_data->output[i][0]));
    }
    
    // Normalise the test data
    for(int i=0; i<test_data_2023->num_data; i++){
        normalise_wind(&(test_data_2023->input[i][0]),12);
        normalise_solar(&(test_data_2023->input[i][12]),12);
        normalise_demand(&(test_data_2023->input[i][24]),12);
        
        normalise_price(&(test_data_2023->output[i][0]));
    }
    
    // Normalise the test data
    for(int i=0; i<test_data_2024->num_data; i++){
        normalise_wind(&(test_data_2024->input[i][0]),12);
        normalise_solar(&(test_data_2024->input[i][12]),12);
        normalise_demand(&(test_data_2024->input[i][24]),12);
        
        normalise_price(&(test_data_2024->output[i][0]));
    }
    
    normalise_wind((fann_type*)&(predict[0]),12);
    normalise_solar((fann_type*)&(predict[12]),12);
    normalise_demand((fann_type*)&(predict[24]),12);
    
    // fann_save_train(train_data, "train_normalise.data");
    // fann_save_train(test_data, "test_normalise.data");
    
	// ann = fann_create_shortcut(2, fann_num_input_train_data(train_data), fann_num_output_train_data(train_data));
    ann = fann_create_standard(5, num_input, 100,50,25, num_output);

    fann_set_training_algorithm(ann, FANN_TRAIN_RPROP);
    fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC);
    fann_set_activation_function_output(ann, FANN_LINEAR);
    fann_set_train_error_function(ann, FANN_ERRORFUNC_LINEAR);
    
    /*steepness = 0.5;*/
    steepness[0] = 1;
    steepness[1] = 0.25;
    steepness[2] = 0.1;
    fann_set_cascade_activation_steepnesses(ann, &(steepness[2]), 1);
    activation[0] = FANN_SIGMOID_SYMMETRIC;
    activation[1] = FANN_COS_SYMMETRIC;
    activation[2] = FANN_SIN_SYMMETRIC;

    fann_set_cascade_activation_functions(ann, &(activation[0]), 1);		
    // fann_set_cascade_num_candidate_groups(ann, 8);
	
	fann_set_bit_fail_limit(ann, (fann_type)0.01);
	fann_set_train_stop_function(ann, FANN_STOPFUNC_BIT);
	fann_print_parameters(ann);
	
	printf("Training network.\n");

	// fann_cascadetrain_on_data(ann, train_data, 300, 1, 0.001);
    fann_train_on_data(ann, train_data, 10000, 500, 0.001);
	
	mse_train = fann_test_data(ann, train_data);
	bit_fail_train = fann_get_bit_fail(ann);
	mse_test = fann_test_data(ann, test_data_2023);
	bit_fail_test = fann_get_bit_fail(ann);
	
	printf("\nTrain error: %f, Train bit-fail: %d, Test error: %f, Test bit-fail: %d\n\n", 
		   mse_train, bit_fail_train, mse_test, bit_fail_test);
           
	mse_test = fann_test_data(ann, test_data_2024);
	bit_fail_test = fann_get_bit_fail(ann);
	
	printf("\nTrain error: %f, Train bit-fail: %d, Test error: %f, Test bit-fail: %d\n\n", 
		   mse_train, bit_fail_train, mse_test, bit_fail_test);
	
	// fann_print_connections(ann);

    fann_save(ann, "trained.net");
    
    fann_type *calc_out = fann_run(ann, (fann_type*)&(predict[0]));
    
    denormalise_price(calc_out);
    
    printf("Predict: %f\n", *calc_out);

    fann_destroy(ann);

    return 0;
}
