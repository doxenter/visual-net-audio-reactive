from support import *
from cam import *
from arc import *
from node import *
from net_visual import *
import sounddevice as sd

fs = 44100                      # frames per sec
sd.default.samplerate = fs
sd.default.channels = 2

duration = 0.009                  # Aufnahmezeit
net_multiplier = [100,50]

def record_and_set(dt,nets):
    recording = sd.rec( int( duration * fs) )
    sd.wait()
    rms = np.sqrt(40*np.mean(recording**2))
    for i,net in enumerate(nets):
        net1.move_intensity(np.ndarray.max(recording))
        net.set_intensity(rms*net_multiplier[i])


calm = np.asarray([80,160,220,255])

neutral = np.asarray([150,150,150,230])

anger = np.asarray([255,60,20,255])

deep_think = np.asarray([255,255,255,255])

happyness = np.asarray([160,210,100,255])

emotional = np.asarray([220,50,200,255])

def deep_feel(feel_array):
    r = np.random.normal(1,0.5,6)
    c,n,a,d,h,e = feel_array
    c = np.random.normal(c,0.1,1)
    n = np.random.normal(n,0.1,1)
    a = np.random.normal(a,0.1,1)
    d = np.random.normal(d*1.2,0.1,1)
    e = np.random.normal(e,0.1,1)
    color = (c * calm + n* neutral + a * anger +d * deep_think + h *happyness + e* emotional)
    reactivity = 0.1 * c + 0.2 * n + 0.9 * a + 0.4 * d + 0.7 * h + 0.3 * e
    return color,reactivity

@window.event
def on_draw():
    
    window.clear()
    camera.update()
    batch.draw()

def update(dt):
    net1.next_step(dt)
    net2.next_step(dt)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)  

def spark1(dt):
    color , reactivity = deep_feel([0.8,0,0.0,0.0,0.2,0])
    
    net1.spark(color)

def spark2(dt):
    #net2.move_intensity(10)

    net2.spark(np.asarray([220,255,255,230]))



if __name__ == "__main__":
   
    gl_active = gl_begin()
    #glEnable(GL_LIGHTING)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glShadeModel(GL_SMOOTH)
    camera = cam()
    net1 = net(200)
    net2 = net(100)
    net1.connection_rate = 0.04
    net2.connection_rate = 0.2
    create_fog(20,300,0, 0.2, 0.3, 10,density = 0.2)
    net1.create_net_cluster(0,0,-40,10)
    net1.set_damping(0.98)
    net1.set_activation_rate(0.2)
    net2.set_node_color_dynamics([0.1,0.1,0],[0.2,0.0,0])
    net2.create_net_cluster(0,0,-40,50)
    net2.set_activation_rate(0.01)
    net2.set_damping(0.6)
    net1.sphere_reshape(0,0,-10,30)
    net2.parallelepipeidal_reshape(0,0,-50,150,70,40)
    net2.move_intensity(10)
    net2.set_pos_pid(0.05,0.1,0.5)
    net1.set_pos_pid(0.3,0.01,0.9)
    net2.set_intensity(0.02)
    clock.schedule_interval(update,0.0167)
    clock.schedule_interval(spark1,0.01)
    clock.schedule_interval(spark2,2)
    clock.schedule_interval(record_and_set,0.01,[net1,net2])

    pyglet.app.run()
