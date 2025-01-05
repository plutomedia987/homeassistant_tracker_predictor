from .enums import activation_functions_enum

from .connection import connection
# from .layer import layer

import math


class neuron:
    def __init__(
        self,
        neuron_id,
        layer_id,
        num_connections_out: int,
        conections_in: tuple[connection],
        is_bias: bool,
    ):
        self.sum: float = 0
        self.value: float = 0
        self.activation_steepness: float = 0.5
        self.activation_function: activation_functions_enum = (
            activation_functions_enum.ACTFUNC_LINEAR
        )
        self.connections_in: tuple[connection] = ()
        self.connections_out: tuple[connection] = ()

        self.neuron_id: int = neuron_id
        self.layer_id: int = layer_id

        self.is_bias = is_bias

        if is_bias == 1:
            self.value = 1

        self.connections_in = conections_in

        for conn_in in conections_in:
            conn_in.set_to_neuron(self.neuron_id, self.layer_id)

        for i in range(0, num_connections_out, 1):
            self.connections_out = (
                *self.connections_out,
                connection(self.neuron_id, self.layer_id, i),
            )

    def get_output_connection(self, id: int) -> connection:
        return self.connections_out[id]

    def get_neuron_id(self) -> int:
        return self.neuron_id

    def get_layer_id(self) -> int:
        return self.layer_id

    def get_all_output_connections(self) -> tuple[connection]:
        return self.connections_out

    def get_all_input_connections(self) -> tuple[connection]:
        return self.connections_in

    def set_value(self, value: float):
        self.value = value
        for conn_out in self.connections_out:
            conn_out.process_value(value)

    def get_value(self) -> float:
        return self.value

    def update_properties(
        self,
        activation_function: activation_functions_enum,
        activation_steepness: float,
    ):
        self.activation_function = activation_function
        self.activation_steepness = activation_steepness

        # print(f"Updating properties of neuron {self.neuron_id}, layer {self.layer_id}")

    def get_properties(self) -> dict[activation_functions_enum, float]:
        return {
            "act_func": self.activation_function,
            "act_steep": self.activation_steepness,
        }

    def update_connections_out(self):
        for conn_out in self.connections_out:
            conn_out.process_value(self.value)

    def update_connections_properties_in(self, weights: tuple[float]):
        for conn_it in range(0, len(self.connections_in), 1):
            self.connections_in[conn_it].set_weight(weights[conn_it])

    def process_neuron(self):
        if not self.is_bias:
            neuron_sum = 0

            for conn_in in self.connections_in:
                neuron_sum += conn_in.get_value()

            neuron_sum *= self.activation_steepness

            if self.activation_steepness == 0:
                pass

            max_sum = 150 / self.activation_steepness
            if neuron_sum > max_sum:
                neuron_sum = max_sum
            elif neuron_sum < -max_sum:
                neuron_sum = -max_sum

            self.sum = neuron_sum

            self.set_value(
                self._activation_switch(self.activation_function, neuron_sum)
            )

        self.update_connections_out()

    def _activation_switch(
        self, activation_func: activation_functions_enum, neuron_sum: float
    ) -> float:
        match activation_func:
            case activation_functions_enum.ACTFUNC_LINEAR:
                return neuron_sum

            case activation_functions_enum.ACTFUNC_LINEAR_PIECE:
                if neuron_sum < 0:
                    return 0
                elif neuron_sum > 1:
                    return 1
                else:
                    return neuron_sum
            case activation_functions_enum.ACTFUNC_LINEAR_PIECE_SYMMETRIC:
                if neuron_sum < -1:
                    return -1
                elif neuron_sum > 1:
                    return 1
                else:
                    return neuron_sum
            case activation_functions_enum.ACTFUNC_SIGMOID:
                return 1.0 / (1.0 + math.exp(-2.0 * neuron_sum))
            case activation_functions_enum.ACTFUNC_SIGMOID_SYMETRIC:
                return 2.0 / (1.0 + math.exp(-2.0 * neuron_sum)) - 1.0
            case activation_functions_enum.ACTFUNC_SIGMOID_SYMETRIC_STEPWISE:
                return self._stepwise(
                    -2.64665293693542480469e00,
                    -1.47221934795379638672e00,
                    -5.49306154251098632812e-01,
                    5.49306154251098632812e-01,
                    1.47221934795379638672e00,
                    2.64665293693542480469e00,
                    -9.90000009536743164062e-01,
                    -8.99999976158142089844e-01,
                    -5.00000000000000000000e-01,
                    5.00000000000000000000e-01,
                    8.99999976158142089844e-01,
                    9.90000009536743164062e-01,
                    -1,
                    1,
                    neuron_sum,
                )
            case activation_functions_enum.ACTFUNC_SIGMOID_STEPWISE:
                return self._stepwise(
                    -2.64665246009826660156e00,
                    -1.47221946716308593750e00,
                    -5.49306154251098632812e-01,
                    5.49306154251098632812e-01,
                    1.47221934795379638672e00,
                    2.64665293693542480469e00,
                    4.99999988824129104614e-03,
                    5.00000007450580596924e-02,
                    2.50000000000000000000e-01,
                    7.50000000000000000000e-01,
                    9.49999988079071044922e-01,
                    9.95000004768371582031e-01,
                    0,
                    1,
                    neuron_sum,
                )
            case activation_functions_enum.ACTFUNC_THRESHOLD:
                if neuron_sum < 0:
                    return 0
                else:
                    return 1
            case activation_functions_enum.ACTFUNC_THRESHOLD_SYMETRIC:
                if neuron_sum < 0:
                    return -1
                else:
                    return 1
            case activation_functions_enum.ACTFUNC_GAUSSIAN:
                return math.exp(-neuron_sum * neuron_sum)
            case activation_functions_enum.ACTFUNC_GAUSIAN_SYMETRIC:
                return (math.exp(-neuron_sum * neuron_sum) * 2.0) - 1.0
            case activation_functions_enum.ACTFUNC_ELLIOT:
                return (neuron_sum / 2.0) / (1.0 + math.abs(neuron_sum)) + 0.5
            case activation_functions_enum.ACTFUNC_ELLIOT_SYMMETRIC:
                return neuron_sum / (1.0 + math.abs(neuron_sum))
            case activation_functions_enum.ACTFUNC_SIN_SYMMETRIC:
                return math.sin(neuron_sum)
            case activation_functions_enum.ACTFUNC_COS_SYMMETRIC:
                return math.cos(neuron_sum)
            case activation_functions_enum.ACTFUNC_SIN:
                return math.sin(neuron_sum) / 2.0 + 0.5
            case activation_functions_enum.ACTFUNC_COS:
                return math.cos(neuron_sum) / 2.0 + 0.5
            case activation_functions_enum.ACTFUNC_GAUSSIAN_STEPWISE:
                return 0
            case activation_functions_enum.ACTFUNC_LINEAR_PIECE_RECT:
                if neuron_sum < 0:
                    return 0
                else:
                    return neuron_sum
            case activation_functions_enum.ACTFUNC_LINEAR_PIECE_RECT_LEAKY:
                if neuron_sum < 0:
                    return neuron_sum * 0.01
                else:
                    return neuron_sum

    def _stepwise(
        self,
        v1: float,
        v2: float,
        v3: float,
        v4: float,
        v5: float,
        v6: float,
        r1: float,
        r2: float,
        r3: float,
        r4: float,
        r5: float,
        r6: float,
        min: float,
        max: float,
        sum: float,
    ) -> float:
        if sum < v5:
            if sum < v3:
                if sum < v2:
                    if sum < v1:
                        return min
                    else:
                        return self._linear(v1, r1, v2, r2, sum)
                else:
                    return self._linear(v2, r2, v3, r3, sum)
            else:
                if sum < v4:
                    return self._linear(v3, r3, v4, r4, sum)
                else:
                    return self._linear(v4, r4, v5, r5, sum)
        else:
            if sum < v6:
                return self._linear(v5, r5, v6, r6, sum)
            else:
                return max

    def _linear(self, v1: float, r1: float, v2: float, r2: float, sum: float) -> float:
        return (((r2 - r1) * (sum - v1)) / (v2 - v1)) + r1
