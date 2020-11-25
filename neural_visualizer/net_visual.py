from support import * 
from node import *
from arc import * 
from sklearn.neighbors import NearestNeighbors

class net():
    def __init__(self,N):
        self.N = N
        self.nodes = []
        self.color = np.asarray((50,50,50,10),dtype = np.int)
        self.acc = np.zeros(shape = (N,3), dtype = np.float64)
        self.arcs = []
        self.connection_rate = 0.1
        self.intensity = 10



    def set_intensity(self,I):
        self.intensity = I

    def set_color(self,r,g,b,a,delta = 0):
        N = self.N
        r_rand = np.random.uniform(r-delta,r+delta,N)
        g_rand = np.random.uniform(g-delta,g+delta,N)
        b_rand = np.random.uniform(b-delta,b+delta,N)
        a_rand = np.random.uniform(a-delta,a+delta,N)
        
        i = 0
        for p in self.nodes:
            p.setcolor(r_rand[i],g_rand[i],b_rand[i],a_rand[i])
            i += 1

    def spike_color(self,a,delta = 20):
        a_rand = np.random.uniform(a-delta,a+delta,self.N)

        i = 0
        for p in self.nodes:
            p.set_alpha(a_rand[i])
            i += 1

    def create_net_cluster(self,x,y,z,d):
        nodes = []
        N = self.N
        xrand = np.random.uniform(x-d,x+d,N)
        yrand = np.random.uniform(y-d,y+d,N)
        zrand = np.random.uniform(z-d,z+d,N)

        for i in range(0,N):
            rand = np.asarray([xrand[i],yrand[i],zrand[i]], dtype = np.float64)
            p = node(rand,[0,0,0])
            p.setcolor(50,50,50,10)
            self.nodes.append(p)
        
        self.create_arc()

    def create_arc(self):
        N = len(self.nodes)
        nodes = self.nodes
        arcs = []
        for node in nodes:
            for i in range(0,math.ceil(random.uniform(0,N * self.connection_rate))):
                p = math.ceil(random.uniform(0,N-1))
                twin_node = self.nodes[p]
                pos_a = node.position
                pos_b = twin_node.position
                arc_c = arc(pos_a,pos_b)
                node.parent_arcs.append(arc_c)
                arc_c.previus_node = node
                arc_c.next_node = twin_node
                arcs.append(arc_c)
        self.arcs = arcs
    
    def rand_reshape(self,x,y,z,d):
        N = len(self.nodes)
        xrand = np.random.uniform(x-d,x+d,N)
        yrand = np.random.uniform(y-d,y+d,N)
        zrand = np.random.uniform(z-d,z+d,N)
        for i in range(0,N):
            rand = np.asarray([xrand[i],yrand[i],zrand[i]], dtype = np.float64)
            self.nodes[i].position_goal = rand

    def parallelepipeidal_reshape(self,x,y,z,lx,ly,lz):
        N = len(self.nodes)
        xrand = np.random.uniform(x-lx,x+lx,N)
        yrand = np.random.uniform(y-ly,y+ly,N)
        zrand = np.random.uniform(z-lz,z+lz,N)
        for i in range(0,N):
            rand = np.asarray([xrand[i],yrand[i],zrand[i]], dtype = np.float64)
            self.nodes[i].position_goal = rand

    def eye_reshape(self,x,y,z,readius):
        N = len(self.nodes)
        circ = 2 * math.pi * readius
        circ_step = circ /( 2 * 3.14)
        for i in range(0,N):
            pos_x = x + readius * math.sin(circ_step * i)
            pos_y = y + readius * math.cos(circ_step * i)
            pos_z = z #+ readius
            pos = np.asarray([pos_x,pos_y,pos_z], dtype = np.float64)
            self.nodes[i].position_goal = pos

    def sphere_reshape(self,x,y,z,readius):
        N = len(self.nodes)
        xi, yi, zi = readius/(math.pi) * sample_spherical(N)
        for i in range(0,N):
            self.nodes[i].position_goal = xi[i]+x, yi[i]+y, zi[i]+z

    @staticmethod
    def get_p_pos(node):
        return node.position

    def set_pos_pid(self,kp,kd,ki):
        for node in self.nodes:
            node.pid_pos = [kp,kd,ki]

    def get_pos_list(self):
        p_pos = self.get_p_pos
        part = self.nodes
        return map(p_pos,part)

    def update_nodes_acc(self):
        acc = self.acc

        i = 0
        for p in self.nodes:
            p.acc = acc[i,:]
            i += 1
  
    def next_step(self,dt):
        nodes = self.nodes
        arcs = self.arcs
        for n in nodes:
            n.next_step(dt)
        for a in arcs:
            a.next_step(dt)

    def spark(self,rgba):
        I = int(np.ceil(self.intensity))
        nodes = self.nodes
        if I > self.N:
            I = self.N
        for i in range(0,I):
            neurospark = np.random.randint(0,self.N)
            nodes[neurospark].spark(rgba)

    def set_node_color_dynamics(self,pid_h,pid_c):
        for node in self.nodes:
            node.pid_hot_col = pid_h
            node.pid_cool_col = pid_c

    def set_activation_rate(self,rate):
        for node in self.nodes:
            node.activation_rate = rate

    def set_node_position_dynamics(pid):
        for node in self.nodes:
            node.pid_pos = pid

    def set_damping(self,damp):
        for n in self.nodes:
            n.damping= damp
        for a in self.arcs:
            a.damping = damp

    def set_Kacc(self,value):
        for arc in self.arcs:
            arc.K_acc = value

    @staticmethod
    def find_nearest_neighbour(points,node_point):
        sample = node_point
        neigh = NearestNeighbors(n_neighbors=2, radius=0.4)

    def move_intensity(self,value):
        for i in range(0,len(self.arcs)):
            self.arcs[i].K_acc = value
    