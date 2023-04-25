from math import floor

class Simulator():
    default_consumers = 2
    default_consumables = 16
    default_reproduction_rate = 0.5

    current_consumers = default_consumers
    current_consumables = default_consumables

    current_cap = current_consumables + current_consumers

    def input_consumer_consumed(self):
        self.current_consumers = int(input("Input base consumers: "))
        self.current_consumables = int(input("Input base consumables: "))
        self.current_cap = self.current_consumables + self.current_consumers

    def run_simulation(self, print_each_step = True):
        iteration_count = int(input("Iteration count: "))
        for i in range(iteration_count):
            consumables_eaten = min(self.current_consumables, self.current_consumers)
            self.current_consumables -= consumables_eaten
            self.current_consumers -= floor(self.current_consumers - consumables_eaten)
            self.current_consumers += floor(consumables_eaten * self.default_reproduction_rate)
            self.current_consumables = floor(self.current_cap - self.current_consumers)
            if print_each_step:
                print(f"Iteration {i}: {self.current_consumers} consumers, {self.current_consumables} consumables.")
        
        print(f"Iteration count ({iteration_count}) finished: {self.current_consumers} consumers, {self.current_consumables} consumables.")
    
    def __init__(self):
        self.input_consumer_consumed()
        while(True):
            self.run_simulation()


Simulator()