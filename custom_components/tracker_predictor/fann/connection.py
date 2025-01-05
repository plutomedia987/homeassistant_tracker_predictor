class connection:
    def __init__(self, from_neuron_id: int, from_layer_id: int, con_id: int):
        self.from_neuron_id: int = from_neuron_id
        self.from_layer_id: int = from_layer_id
        self.to_neuron_id: int = None
        self.to_layer_id: int = None
        self.weight: float = 0
        self.value: float = 0
        self.con_id: int = con_id

    def set_to_neuron(self, to_neuron_id: int, to_layer_id: int):
        self.to_neuron_id = to_neuron_id
        self.to_layer_id = to_layer_id

    def get_con_id(self) -> int:
        return self.con_id

    def get_from_neruon(self) -> dict[int, int]:
        return {"neuron_id": self.from_neuron_id, "layer_id": self.from_layer_id}

    def get_to_neruon(self) -> dict[int, int]:
        return {"neuron_id": self.to_neuron_id, "layer_id": self.to_layer_id}

    def process_value(self, value: float):
        self.value = value * self.weight

    def get_value(self) -> float:
        return self.value

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, weight: float):
        self.weight = weight
