# from .neuron import neuron, connection
from .layer import layer

# from .connection import connection
from .enums import (
    activation_functions_enum,
    train_enum,
    error_func_enum,
    stop_func_enum,
    net_type_enum,
    errno_enum,
)

import string
from random import *

from typing_extensions import TextIO


class ann:
    def __init__(self):
        self.errno = errno_enum.E_NO_ERROR
        self.errstr = ""
        self.learning_rate = 0.7
        self.learning_momentum = 0.0
        self.network_type = net_type_enum.NETTYPE_LAYER
        self.total_neurons = 0
        self.num_input = 0
        self.num_output = 0
        self.weights = ()
        self.train_errors = ()
        self.training_algorithm = train_enum.TRAIN_RPROP
        self.total_connections = 0
        self.output = ()
        self.num_MSE = 0
        self.MSE_value = 0
        self.num_bit_fail = 0
        self.bit_fail_limit = 0.35

        self.layers: tuple[layer] = None

        self.output_file: string = "Network.txt"

    def create_standard(self, num_layers: int, layer_sizes: tuple[int]):
        self.create_standard_array(num_layers, layer_sizes)

    def create_standard_array(self, num_layers: int, layer_sizes: tuple[int]):
        self.create_sparse_array(1, num_layers, layer_sizes)

    def create_sparse(
        self, connection_rate: float, num_layers: int, layer_sizes: tuple[int]
    ):
        self.create_sparse_array(connection_rate, num_layers, layer_sizes)

    def create_sparse_array(
        self, connection_rate: float, num_layers: int, layer_sizes: tuple[int]
    ):
        self.connection_rate = min(connection_rate, 1)

        seed(None)

        self.layers = ()
        for i in range(0, num_layers, 1):
            if i == num_layers - 1:
                num_neurons_next_layer = 0
            else:
                num_neurons_next_layer = layer_sizes[i + 1] + 1

            if i == 0:
                prev_layer = None
            else:
                prev_layer = self.layers[i - 1]

            self.layers = (
                *self.layers,
                layer(layer_sizes[i] + 1, i, num_neurons_next_layer, prev_layer),
            )

            # print(self.layers)

        self.num_input = layer_sizes[0]
        self.num_output = layer_sizes[-1]

    def run(self, inputs: tuple[float]) -> tuple[float]:
        """Run the neural network"""
        if self.layers[0].set_neuron_values(inputs):
            # Don't update first layer
            for layer_it in range(1, len(self.layers), 1):
                self.layers[layer_it].process_layer()

            return self.layers[-1].get_neuron_values()
        else:
            raise Exception("Too many inputs provided")

    def set_output_file(self, file_path: string):
        """Set the file to print a readable network to"""
        self.output_file = file_path

    def print_network(self, file: string = None):
        """Print the network with connections and weights to a file"""

        output_file = self.output_file

        if file is not None:
            output_file = file

        with open(output_file, "w") as network_file:
            for layer_i in self.layers:
                network_file.write(f"Layer {layer_i.get_layer_id()}:\n")

                for neuron_i in layer_i.get_all_neurons():
                    network_file.write(
                        f"\tNeuron {neuron_i.get_neuron_id()} layer {neuron_i.get_layer_id()}:\n"
                    )
                    neuron_prop = neuron_i.get_properties()
                    network_file.write(
                        f"\t Act Function: {neuron_prop["act_func"]}\n\t Act Steepness: {neuron_prop["act_steep"]}\n"
                    )

                    for con_in in neuron_i.get_all_input_connections():
                        from_neuron = con_in.get_from_neruon()
                        network_file.write(
                            f"\t\tInput Connection {con_in.get_con_id()}: from neuron {from_neuron["neuron_id"]} in layer {from_neuron["layer_id"]} - Weight: {con_in.get_weight()}\n"
                        )

                    for con_out in neuron_i.get_all_output_connections():
                        to_neuron = con_out.get_to_neruon()
                        network_file.write(
                            f"\t\tOutput Connection {con_out.get_con_id()}: to neuron {to_neuron["neuron_id"]} in layer {to_neuron["layer_id"]} - Weight: {con_out.get_weight()}\n"
                        )

    def create_from_fann_file(self, input_file: string):
        """Create a network from a fann file."""

        try:
            nn_file = open(input_file)
        except FileNotFoundError:
            raise Exception("Neural network input file not found")
        else:
            with nn_file:
                match nn_file.readline().rstrip():
                    case "FANN_FIX_1.1" | "FANN_FIX_2.0" | "FANN_FIX_2.1":
                        raise Exception("Fixed point not supported")
                    case "FANN_FLO_1.1":
                        self._process_from_fann_file_v1_1(nn_file)
                    case "FANN_FLO_2.0" | "FANN_FLO_2.1":
                        self._process_from_fann_file_v2(nn_file)
                    case _:
                        raise Exception("Invalid file specified")

    def _process_from_fann_file_v1_1(self, file: TextIO):
        """Parse a verison 1.1 file."""
        raise Exception("v1.1 not implemented")

    def _process_from_fann_file_v2(self, file: TextIO):
        """Parse a verison 2.0/2.1 file."""
        num_layers = int(file.readline().rstrip().split("=")[1])
        self.learning_rate = float(file.readline().rstrip().split("=")[1])
        connection_rate = float(file.readline().rstrip().split("=")[1])
        self.network_type = net_type_enum(int(file.readline().rstrip().split("=")[1]))
        self.learning_momentum = float(file.readline().rstrip().split("=")[1])
        self.training_algorithm = train_enum(
            int(file.readline().rstrip().split("=")[1])
        )
        train_error_function = error_func_enum(
            int(file.readline().rstrip().split("=")[1])
        )
        train_stop_function = stop_func_enum(
            int(file.readline().rstrip().split("=")[1])
        )
        cascade_output_change = float(file.readline().rstrip().split("=")[1])
        quickprop_decay = float(file.readline().rstrip().split("=")[1])
        quickprop_mu = float(file.readline().rstrip().split("=")[1])
        rprop_increase_factor = float(file.readline().rstrip().split("=")[1])
        rprop_decrease_factor = float(file.readline().rstrip().split("=")[1])
        rprop_delta_min = float(file.readline().rstrip().split("=")[1])
        rprop_delta_max = float(file.readline().rstrip().split("=")[1])
        rprop_delta_zero = float(file.readline().rstrip().split("=")[1])
        cascade_output_stagnation_epochs = int(file.readline().rstrip().split("=")[1])
        cascade_candidate_change_fraction = float(
            file.readline().rstrip().split("=")[1]
        )
        cascade_candidate_stagnation_epochs = int(
            file.readline().rstrip().split("=")[1]
        )
        cascade_max_out_epochs = int(file.readline().rstrip().split("=")[1])
        cascade_min_out_epochs = int(file.readline().rstrip().split("=")[1])
        cascade_max_cand_epochs = int(file.readline().rstrip().split("=")[1])
        cascade_min_cand_epochs = int(file.readline().rstrip().split("=")[1])
        cascade_num_candidate_groups = int(file.readline().rstrip().split("=")[1])
        bit_fail_limit = float(
            file.readline().rstrip().split("=")[1]
        )  # scientific notation??
        cascade_candidate_limit = float(
            file.readline().rstrip().split("=")[1]
        )  # scientific notation
        cascade_weight_multiplier = float(
            file.readline().rstrip().split("=")[1]
        )  # scientific notation
        cascade_activation_functions_count = int(file.readline().rstrip().split("=")[1])
        cascade_activation_functions = int(file.readline().rstrip().split("=")[1])
        cascade_activation_steepness_count = int(file.readline().rstrip().split("=")[1])
        cascade_activation_steepness = float(file.readline().rstrip().split("=")[1])
        layer_sizes = tuple(
            [int(x) - 1 for x in file.readline().rstrip().split("=")[1].split(" ")]
        )
        scale_included = int(file.readline().rstrip().split("=")[1])
        neurons_str = file.readline().rstrip().split("=")[1]
        connections_str = file.readline().rstrip().split("=")[1]

        # Create a fully populated netowrk
        self.create_sparse_array(connection_rate, num_layers, layer_sizes)

        # Read neurons
        # neurons: tuple[dict[int, activation_functions_enum, float, tuple[float]]] = ()

        neurons_in = neurons_str.split(") ")
        connections_in = connections_str.split(") ")

        if sum(layer_sizes) + len(layer_sizes) != len(neurons_in):
            raise Exception("Number of layer neurons don't match number of neurons")

        neuron_it = 0
        layer_it = 0
        con_it = 0
        for neuron_each in neurons_in:
            vals = neuron_each.split(", ")

            vals[0] = vals[0].replace("(", "")
            vals[2] = vals[2].replace(")", "")

            self.layers[layer_it].update_neuron_properties(
                neuron_it, activation_functions_enum(int(vals[1])), float(vals[2])
            )

            # Update connections
            if layer_it != 0 and neuron_it != layer_sizes[layer_it]:
                connections: tuple[float] = ()
                num_con = layer_sizes[layer_it - 1] + 1
                for con_it in range(con_it, con_it + num_con, 1):
                    connections = (
                        *connections,
                        float(connections_in[con_it].split(", ")[1].replace(")", "")),
                    )

                self.layers[layer_it].update_neuron_connections(neuron_it, connections)

                con_it += 1

            if neuron_it == layer_sizes[layer_it]:
                neuron_it = 0
                layer_it += 1
            else:
                neuron_it += 1

            # neuron_setup = {
            #     "num_inputs": int(vals[0]),
            #     "activation_function": activation_functions_enum(int(vals[1])),
            #     "activation_steepness": float(vals[2]),
            #     "connections": (),
            # }

            # neurons = (*neurons, neuron_setup)

        # Read connections
        # for conn_each in connections_str.split(") "):
        #     vals = conn_each.split(", ")

        #     vals[0] = vals[0].replace("(", "")
        #     vals[1] = vals[1].replace(")", "")

        #     neurons[int(vals[0]) + layer_sizes[0]]["connections"] = (
        #         *neurons[int(vals[0]) + layer_sizes[0]]["connections"],
        #         float(vals[1]),
        #     )

        nuron_it = 0

        for layer in self.layers:
            for nuron_it in range(nuron_it, nuron_it + layer.get_num_neurons(), 1):
                pass
