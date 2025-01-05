from enum import Enum, auto


class activation_functions_enum(Enum):
    ACTFUNC_LINEAR = 0
    ACTFUNC_THRESHOLD = auto()
    ACTFUNC_THRESHOLD_SYMETRIC = auto()
    ACTFUNC_SIGMOID = auto()
    ACTFUNC_SIGMOID_STEPWISE = auto()
    ACTFUNC_SIGMOID_SYMETRIC = auto()
    ACTFUNC_SIGMOID_SYMETRIC_STEPWISE = auto()
    ACTFUNC_GAUSSIAN = auto()
    ACTFUNC_GAUSIAN_SYMETRIC = auto()
    ACTFUNC_GAUSSIAN_STEPWISE = auto()
    ACTFUNC_ELLIOT = auto()
    ACTFUNC_ELLIOT_SYMMETRIC = auto()
    ACTFUNC_LINEAR_PIECE = auto()
    ACTFUNC_LINEAR_PIECE_SYMMETRIC = auto()
    ACTFUNC_SIN_SYMMETRIC = auto()
    ACTFUNC_COS_SYMMETRIC = auto()
    ACTFUNC_SIN = auto()
    ACTFUNC_COS = auto()
    ACTFUNC_LINEAR_PIECE_RECT = auto()
    ACTFUNC_LINEAR_PIECE_RECT_LEAKY = auto()


class train_enum(Enum):
    TRAIN_INCREMENTAL = 0
    TRAIN_BATCH = auto()
    TRAIN_RPROP = auto()
    TRAIN_QUICKPROP = auto()
    TRAIN_SARPROP = auto()


class error_func_enum(Enum):
    ERRORFUNC_LINEAR = 0
    ERRORFUNC_TANH = auto()


class stop_func_enum(Enum):
    STOPFUNC_MSE = 0
    STOPFUNC_BIT = auto()


class net_type_enum(Enum):
    NETTYPE_LAYER = 0
    NETTYPE_SHORTCUT = auto()


class errno_enum(Enum):
    E_NO_ERROR = 0
    E_CANT_OPEN_CONFIG_R = auto()
    E_CANT_OPEN_CONFIG_W = auto()
    E_WRONG_CONFIG_VERSION = auto()
    E_CANT_READ_CONFIG = auto()
    E_CANT_READ_NEURON = auto()
    E_CANT_READ_CONNECTIONS = auto()
    E_WRONG_NUM_CONNECTIONS = auto()
    E_CANT_OPEN_TD_W = auto()
    E_CANT_OPEN_TD_R = auto()
    E_CANT_READ_TD = auto()
    E_CANT_ALLOCATE_MEM = auto()
    E_CANT_TRAIN_ACTIVATION = auto()
    E_CANT_USE_ACTIVATION = auto()
    E_TRAIN_DATA_MISMATCH = auto()
    E_CANT_USE_TRAIN_ALG = auto()
    E_TRAIN_DATA_SUBSET = auto()
    E_INDEX_OUT_OF_BOUND = auto()
    E_SCALE_NOT_PRESENT = auto()
    E_INPUT_NO_MATCH = auto()
    E_OUTPUT_NO_MATCH = auto()
    E_WRONG_PARAMETERS_FOR_CREATE = auto()
