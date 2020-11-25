import pyglet
from pyglet.window import key
from pyglet.gl import *
import numpy as np
from pyglet import clock
import math
import time
import random
import multiprocessing as mp
from functools import partial
import numba 
from numba import jit
import timeit
import threading 
from scipy.spatial import KDTree

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def get_screen():
    display = pyglet.canvas.Display()
    screen = display.get_default_screen()
    screen_width = screen.width
    screen_height = screen.height

    return screen_width,screen_height

def create_window():
    display = pyglet.canvas.get_display()
    w,h = get_screen()
    config = pyglet.gl.Config(sample_buffers=1, samples=8)
    window = pyglet.window.Window(config=config,height = h , width = w, resizable = True) #,style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    window.set_fullscreen(False)

    return window

def create_batch():
    batch = pyglet.graphics.Batch()
    return batch

def create_fog(start,end,r,g,b,a,density= 0.1):
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(r,g,b,a))
    glFogf (GL_FOG_DENSITY, density);
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, start)
    glFogf(GL_FOG_END, end)


def gl_begin():
    pyglet.options['debug_gl'] = False
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    #glEnableClientState
    glDepthFunc(GL_LEQUAL)  
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    #pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)  
    glEnable(GL_ALPHA_TEST)
    glEnable(GL_DEPTH_TEST) #Makes it so you can't see faces through other faces.
    glEnable(GL_CULL_FACE) #Enables culling, doesn't render the faces you can't see. Increases performance.
    glEnable (GL_FOG);
    glHint (GL_FOG_HINT, GL_NICEST);
    return True

window = create_window()
batch = create_batch()


def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    return vec