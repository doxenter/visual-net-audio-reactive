from support import *


class node():
    def __init__(self,position,velocity):
        self.position = np.asarray(position,dtype = np.float64)
        self.velocity = np.asarray(velocity,dtype = np.float64)
        self.acc = np.asarray((0,0,0),dtype = np.float64)
        self.size = 8
        self.color = np.asarray((50,50,50,10),dtype = np.int)
        self.color_goal = np.asarray((0,0,0,0),dtype = np.int)
        self.color_sleep = np.asarray((50,50,50,10),dtype = np.int)
        self.color_error = np.asarray((0,0,0,0),dtype = np.int)
        self.position_goal = np.asarray(position,dtype = np.float64)
        self.position_error = np.asarray((0,0,0),dtype = np.float64)
        self.vertex_list = None
        self.pid_hot_col = 0.1,0,0
        self.pid_cool_col = 0.06,0,0
        self.pid_pos = 0.2,0.01,0.5
        self.update_vertex()
        self.parent_arcs= []
        self.dt = 0.01
        self.damping = 0.8
        self.activation_rate = 0.5
    
    def update_vertex(self):
        pos = self.position
        col = self.color
        
        self.vertex_list = batch.add(
                            1,pyglet.gl.GL_POINTS,None,
                            ('v3f/stream', (pos)),
                            ('c4B/stream', (col)))            
        glPointSize(self.size)

    def move(self,d_pos):
        self.position += d_pos
        self.vertex_list.vertices = self.position
    
    def set_pos(self,x,y,z,color = None):
        self.pos = x,y,z
        self.vertex_list.vertices = self.pos 
    
    def setcolor(self,r,g,b,a):
        self.color = np.asarray((r,g,b,a),dtype = np.int)
        self.vertex_list.colors = self.color
    
    def update_vertexcolor(self):
        self.vertex_list.colors = np.asarray(self.color,dtype = np.int)

    def spark(self,rgba):
        self.color_goal = rgba
        self.color_dynamics()
        if self.color_goal[3] > 15:
            self.spark_next()

    def spark_next(self):
        next_rgba = np.floor(self.color_goal * self.damping )
        K = np.random.randint(0,len(self.parent_arcs),size = math.ceil(len(self.parent_arcs)*self.activation_rate))
        for i in range(0,len(K)):
            threading.Timer(0.05, self.parent_arcs[K[i]].spark,[next_rgba]).start()
        
    def turn_hot(self):
        dt = self.dt
        Kp_col,Kd_col,Ki_col = self.pid_hot_col 
        previus_error = self.color_error
        self.color_error = self.color_goal - self.color
        color_error_dot = self.color_error - previus_error
        self.color = np.floor(self.color + self.color_error * Kp_col + Kd_col * color_error_dot * dt + Ki_col*( (previus_error + self.color_error)  / (2 * dt) ) )
        self.acc = np.asarray((0,0,0),dtype = np.float64)

    def cool_down(self):
        dt = self.dt
        Kp_col,Kd_col,Ki_col = self.pid_cool_col 
        previus_error = self.color_error
        self.color_error = self.color_goal - self.color
        color_error_dot = self.color_error - previus_error
        self.color = np.floor(self.color + self.color_error * Kp_col + Kd_col * color_error_dot * dt + Ki_col*( (previus_error + self.color_error)  / (2 * dt) ) )
        
    def color_dynamics(self):
        if self.color_goal[3] > 10:
            self.turn_hot()
            if self.color_error[3] < 10:
                self.color_goal = self.color_sleep
        else:
            self.cool_down()

    def update_vertexpos(self):
        pos = self.position
        self.vertex_list.vertices = np.asarray(pos,dtype = np.float64)

    def position_dynamics(self):
        Kp,Kd,Ki = self.pid_pos
        self.velocity = self.acc * self.dt + self.velocity * 0.95
        pos_n = self.velocity * self.dt + self.position
        previus_error = self.position_error
        self.position_error = self.position_goal - pos_n
        position_error_dot =  (-previus_error + self.position_error)/2
        self.position = pos_n + self.position_error * Kp + Kd * position_error_dot/self.dt + Ki * self.position_error * self.dt
        self.acc = np.asarray((0,0,0),dtype = np.float64)
        
    def next_step(self,dt):
        self.dt = dt
        self.color_dynamics()
        self.position_dynamics()
        self.update_vertexcolor()
        self.update_vertexpos()
