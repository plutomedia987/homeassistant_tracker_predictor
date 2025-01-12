from .neuron import neuron
from typing_extensions import Self
from .enums import activation_functions_enum


class layer:
    def __init__(
        self,
        num_neurons: int,
        layer_id: int,
        num_neurons_next_layer: int,
        prev_layer: Self,
    ):
        """Create layer and connected neurons."""

        self.layer_id: int = layer_id
        self.num_neurons_next_layer = num_neurons_next_layer
        self.neurons: tuple[neuron] = ()
        self.num_neurons: int = num_neurons

        for new_neuron_it in range(0, num_neurons, 1):
            connections_in = ()

            if prev_layer is not None:
                for old_neuron_it in range(0, prev_layer.get_num_neurons(), 1):
                    prev_neuron = prev_layer.get_neuron(old_neuron_it)
                    connections_in = (
                        *connections_in,
                        prev_neuron.get_output_connection(new_neuron_it),
                    )

            is_bias = False
            if new_neuron_it == num_neurons - 1:
                is_bias = True
                connections_in = ()

            self.neurons = (
                *self.neurons,
                neuron(
                    new_neuron_it,
                    layer_id,
                    num_neurons_next_layer,
                    connections_in,
                    is_bias,
                ),
            )

    def get_neuron(self, id: int) -> neuron:
        """Get a neuron."""
        return self.neurons[id]

    def get_num_neurons(self) -> int:
        """Get the number of neurons."""
        return self.num_neurons

    def get_layer_id(self) -> int:
        return self.layer_id

    def get_all_neurons(self) -> tuple[neuron]:
        return self.neurons

    def set_neuron_values(self, values: tuple[float]) -> bool:
        if len(values) > len(self.neurons) - 1:
            return False

        for i in range(0, len(values), 1):
            self.neurons[i].set_value(values[i])

        # Set bias
        self.neurons[-1].set_value(1)

        return True

    def get_neuron_values(self) -> tuple[float]:
        retVal = ()
        for neuron_each in self.neurons:
            retVal = (*retVal, neuron_each.get_value())

        return retVal

    def process_layer(self):
        for neuron_each in self.neurons:
            neuron_each.process_neuron()

    def update_neuron_properties(
        self,
        neuron_id: int,
        activation_function: activation_functions_enum,
        activation_steepness: float,
    ):
        self.neurons[neuron_id].update_properties(
            activation_function, activation_steepness
        )

    def update_neuron_connections(self, neuron_id: int, connections: tuple[float]):
        self.neurons[neuron_id].update_connections_properties_in(connections)
