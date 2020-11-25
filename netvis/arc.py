from support import *

class arc():
    def __init__(self,pos_a,pos_b):
        self.pos_a = np.asarray(pos_a,dtype = np.float64)
        self.pos_b = np.asarray(pos_b,dtype = np.float64)
        self.col_a = np.asarray((50,50,50,10),dtype = np.int)
        self.col_b = np.asarray((50,50,50,10),dtype = np.int)
        self.color_sleep = np.asarray((50,50,50,10),dtype = np.int)
        self.vertex_list = None
        self.size = 0.1
        self.pid_hot_col = 0.2,0.2,0
        self.pid_cool_col = 0.05,0.2,0
        self.update_vertex()
        self.previus_node = None
        self.next_node = None
        self.vertex_list = None
        self.update_vertex()
        self.dt = 0.01
        self.damping = 0.97
        self.pid_col = 0,0,0
        self.K_acc = 0.5
        self.color = np.asarray((50,50,50,10),dtype = np.int)
        self.color_error = np.asarray((0,0,0,0),dtype = np.int)
        self.color_goal = np.asarray((50,50,50,10),dtype = np.int)

    def update_vertex(self):
        pos_a = self.pos_a
        pos_b = self.pos_b
        pos = np.append(pos_a,pos_b)
        col_a = self.col_a
        col_b = self.col_b
        col = np.append(col_a,col_b)

        self.vertex_list = batch.add(
                            2,pyglet.gl.GL_LINES,None,
                            ('v3f/dynamic', (pos)),
                            ('c4B/dynamic', (col))
                            )

    def update_vertexcolor(self):
        col = np.append(self.col_a,(self.col_a+self.col_b)/2)
        self.vertex_list.colors = np.asarray(col,dtype = np.int)

    def update_vertexpos(self):
        self.pos_a = self.previus_node.position
        self.pos_b = self.next_node.position
        pos = np.append(self.pos_a,self.pos_b)
        self.vertex_list.vertices = np.asarray(pos,dtype = np.float)

    def spark(self,rgba):
        self.color = rgba
        self.color_dynamics()
        self.spark_next()
        
    def spark_next(self):
        next_rgba = np.floor(self.color * self.damping )
        if self.previus_node.color_goal[3] > 15 :
            threading.Timer(0.05,self.next_node.spark,[next_rgba]).start()
            self.acc = self.K_acc * 200 * np.asarray(next_rgba[3]/255,dtype = np.float64) * normalize(self.pos_b-self.pos_a) #* random.randint(-1,1)
            self.next_node.acc += np.array(self.acc,dtype = np.float64) 

    def color_dynamics(self):
        if self.previus_node.color[3] > 10 and self.next_node.color[3] > 10:
            self.col_a = self.previus_node.color
        else:
            self.col_a = self.color_sleep
        if self.next_node.color_goal[3] > 10:
            self.col_b = self.next_node.color
        else:
            self.col_b = self.color_sleep

    def next_step(self,dt):
        self.dt = dt
        self.color_dynamics()
        self.update_vertexcolor()
        self.update_vertexpos()