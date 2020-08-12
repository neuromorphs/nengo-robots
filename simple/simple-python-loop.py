import nengo
import numpy as np

# this is a dummy environment with a simple sensor and motor
class ExampleIO:
    def __init__(self):
        self.data = 0.0
        
    def sensor(self):
        return self.data + np.random.normal(0, 0.1)
        
    def motor(self, x):
        self.data += x * 0.001

io = ExampleIO()

model = nengo.Network()
with model:
    sensor = nengo.Node(lambda t: io.sensor())
    
    motor = nengo.Node(lambda t, x: io.motor(x), size_in=1)
    
    target = nengo.Node(0.5)
    
    error = nengo.Ensemble(n_neurons=100, dimensions=1)
    nengo.Connection(sensor, error, transform=-1)
    nengo.Connection(target, error)
    nengo.Connection(error, motor)
    
sim = nengo.Simulator(model, dt=0.001)


sensor_data = []
for i in range(10000):
    sim.step()
    sensor_data.append(io.sensor())
sim.close()

import matplotlib.pyplot as plt
plt.plot(sensor_data)
plt.show()