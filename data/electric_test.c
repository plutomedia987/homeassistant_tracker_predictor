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
    struct fann *ann;
    
    const float predict[13][36] = {
        {7954,6040,5101,3928,3235,2660,2162,2096,2407,2563,2494,2383,0,0,0,0,0,1456,3365,2410,90,0,0,0,30280,29275,28200,32584,42668,42798,42300,41400,43003,44796,40887,34975},
        {2317,2294,2336,2448,2470,2456,2237,2451,2900,3345,3634,3822,0,0,0,0,0,1366,3418,2583,159,0,0,0,30180,29239,27954,27909,32655,37758,37222,36562,38442,42441,39750,35326},
        {3978,4369,5002,5972,7244,8435,9440,10409,11559,12869,13865,14632,0,0,0,0,0,1476,3834,2891,219,0,0,0,29637,28808,27236,26619,28824,33640,33546,35347,37359,41037,36850,31775},
        {15239,15681,16166,16430,16523,16559,16581,16501,16463,16472,16315,16048,0,0,0,0,0,1114,2647,2192,152,0,0,0,25142,25283,23979,25059,35799,38832,37813,37352,38148,41844,38845,32471},
        {15619,15145,14516,13668,13070,12669,12310,11766,11357,11062,11196,11352,0,0,0,0,0,781,2024,1644,112,0,0,0,25393,25431,24181,25354,34852,38985,37841,36910,38052,41604,38897,32425},
        {11490,11550,11562,11545,11568,11568,11538,11437,11285,10884,10829,10716,0,0,0,0,0,1057,2409,1922,147,0,0,0,25970,25547,24165,24686,35051,37106,35446,35673,36984,41293,38561,31761},
        {10534,10256,9905,9562,9488,9369,9212,9057,8845,8622,8578,8509,0,0,0,0,0,1282,2823,2116,179,0,0,0,25993,25710,24099,25032,34606,37579,35979,36207,37322,41413,39218,33418},
        {8431,8461,8476,8491,8714,8863,8936,9052,9132,9189,9502,9768,0,0,0,0,0,1092,1969,1567,128,0,0,0,26547,26000,24483,25689,34816,38320,36541,35968,37205,40658,37604,31796},
        {9986,10212,10347,10420,10657,10685,10643,10900,10994,11021,11212,11194,0,0,0,0,0,944,1696,1371,98,0,0,0,26162,25016,23198,22705,27152,30350,31458,31816,33025,37538,34550,30212},
        {11046,11341,11434,11322,11429,11327,11103,11169,10963,10702,10972,11086,0,0,0,0,0,1345,2469,2078,176,0,0,0,24993,24341,22093,21448,23809,28031,29660,31381,34322,38367,34784,30013},
        {11116,11246,11218,11172,11596,11776,11826,12199,12307,12206,12456,12477,0,0,0,0,0,1138,2012,1541,137,0,0,0,24347,24618,22773,24817,34881,37427,36094,36107,38081,42003,39588,32874},
        {12390,12539,12540,12416,12530,12478,12321,12310,12110,11822,11746,11485,0,0,0,0,0,1085,2676,2738,1090,0,0,0,26081,25739,23960,25403,35725,37420,36098,36071,37673,41855,38993,32620},
        {11203,11324,11170,11033,11307,11398,11419,11784,11977,12093,12516,12810,0,0,0,0,0,1085,2676,2738,1090,0,0,0,26226,25721,24216,25022,35231,36555,35532,35329,37468,41676,39254,32871}
    };
 
    ann = fann_create_from_file("electric_trained.net");
    
    for(int i=0; i<13; i++){
        normalise_wind((fann_type*)&(predict[i][0]),12);
        normalise_solar((fann_type*)&(predict[i][12]),12);
        normalise_demand((fann_type*)&(predict[i][24]),12);
    
        fann_type *calc_out = fann_run(ann, (fann_type*)&(predict[i][0]));
    
        denormalise_price(calc_out);
    
        printf("Predict: %f\n", *calc_out);
        printf("Octo Predict: %f\n", (*calc_out * 1.2012) + 10.3059);
    }

    fann_destroy(ann);

    return 0;
}