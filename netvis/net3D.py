from support import *
from cam import *
from arc import *
from node import *
from net_visual import *


@window.event
def on_draw():
    
    window.clear()
    camera.update()
    batch.draw()

def update(dt):
    net1.next_step(dt)
    net2.next_step(dt)
    

def spark1(dt):
    r = np.random.randint(254,255,1)
    g = np.random.randint(254,255,1)
    b = np.random.randint(254,255,1)
    #rgba = np.append(rgb,255)
    net1.spark(np.asarray([r,g,b,250]),1)


def spark2(dt):
    net2.spark(np.asarray([255,255,255,250]),1)

if __name__ == "__main__":
   
    gl_active = gl_begin()
    camera = cam()
    net1 = net(100)
    net2 = net(200)
    net1.connection_rate = 0.075
    create_fog(20,200,0.2, 0.4, 1, 10,density = 0.4)
    net1.create_net_cluster(0,0,-40,20)
    net1.set_damping(0.96)
    net1.set_activation_rate(0.2)
    net2.set_node_dynamics([0.1,0.1,0],[0.2,0.0,0])
    net2.create_net_cluster(0,0,0,100)
    net2.set_activation_rate(0.1)
    clock.schedule_interval(update,0.0167)
    clock.schedule_interval(spark1,0.1)
    clock.schedule_interval(spark2,3)
    pyglet.app.run()
