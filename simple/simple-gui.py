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
    
    target = nengo.Node(0)
    
    error = nengo.Ensemble(n_neurons=100, dimensions=1)
    nengo.Connection(sensor, error, transform=-1)
    nengo.Connection(target, error)
    nengo.Connection(error, motor)
    
# for a lot of robotics applications, there's often some
#  sort of startup and initialization to do. If you
#  define these functions, they will be called at the
#  given times
def on_start(sim):
    # called just before running the model
    print('start')
    
def on_pause(sim):
    # called when pause is pressed (useful for turning off motors)
    print('pause')
    
def on_continue(sim):
    # called when continue from pause (turn motors back on)
    print('continue')
    
def on_step(sim):
    # called every time step (default=0.001 seconds simulation time)
    print('step')
    
def on_close(sim):
    # called when the GUI window is closed after being started
    #  (useful for disconnected whatever happened in on_start)
    print('close')
