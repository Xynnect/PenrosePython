import random
import threading

__author__ = 'zyan'
from kivy import args
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
import time
import math
import cmath
import cairo
import psutil
import os
from subprocess import Popen

#------ Configuration --------
IMAGE_SIZE = (1000, 1000)
NUM_SUBDIVISIONS = 8
#-----------------------------

goldenRatio = (1 + math.sqrt(5)) / 2

# RandomColoring
Color11 = random.random()
Color12 = random.random()
Color13 = random.random()
Color21 = random.random()
Color22 = random.random()
Color23 = random.random()
#-----------------------------

class Penrose():
    # Gtk.init(args)
    def subdivide(triangles):
        result = []
        for color, A, B, C in triangles:
            if color == 0:
                # Subdivide red triangle
                P = A + (B - A) / goldenRatio
                result += [(0, C, P, B), (1, P, C, A)]
            else:
                # Subdivide blue triangle
                Q = B + (A - B) / goldenRatio
                R = B + (C - B) / goldenRatio
                result += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
        return result

    # Create wheel of red triangles around the origin
    triangles = []
    for i in xrange(10):
        B = cmath.rect(1, (2*i - 1) * math.pi / 10)
        C = cmath.rect(1, (2*i + 1) * math.pi / 10)
        if i % 2 == 0:
            B, C = C, B  # Make sure to mirror every second triangle
        triangles.append((0, 0j, B, C))

    # Perform subdivisions
    for i in xrange(NUM_SUBDIVISIONS):
        triangles = subdivide(triangles)

    # Prepare cairo surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_SIZE[0], IMAGE_SIZE[1])
    cr = cairo.Context(surface)
    cr.translate(IMAGE_SIZE[0] / 2.0, IMAGE_SIZE[1] / 2.0)
    wheelRadius = 1.2 * math.sqrt((IMAGE_SIZE[0] / 2.0) ** 2 + (IMAGE_SIZE[1] / 2.0) ** 2)
    cr.scale(wheelRadius, wheelRadius)

    # Draw red triangles
    for color, A, B, C in triangles:
        if color == 0:
            cr.move_to(A.real, A.imag)
            cr.line_to(B.real, B.imag)
            cr.line_to(C.real, C.imag)
            cr.close_path()
    cr.set_source_rgb(Color11, Color12, Color13)
    cr.fill()

    # Draw blue triangles
    for color, A, B, C in triangles:
        if color == 1:
            cr.move_to(A.real, A.imag)
            cr.line_to(B.real, B.imag)
            cr.line_to(C.real, C.imag)
            cr.close_path()
    cr.set_source_rgb(Color21, Color22, Color23)
    cr.fill()

    # Determine line width from size of first triangle
    color, A, B, C = triangles[0]
    cr.set_line_width(abs(B - A) / 10.0)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)

    # Draw outlines
    for color, A, B, C in triangles:
        cr.move_to(C.real, C.imag)
        cr.line_to(A.real, A.imag)
        cr.line_to(B.real, B.imag)
    cr.set_source_rgb(0.2, 0.2, 0.2)
    cr.stroke()

    # Save to PNG
    surface.write_to_png('penrose.png')

Builder.load_string("""
<MyPaintApp>:
    Image:
        source: 'penrose.png'
        size_hint: None,None
        size: 1000,1000
""")


class MyPaintApp(App, StackLayout):
    def build(self):
        for process in psutil.process_iter():
            if process.cmdline == ['python', 'pythonPenroseServer.py']:
                print('Process found. Terminating it.')
                process.terminate()
            break
        else:
            print('Process not found: starting it.')
            Popen(['python', 'pythonPenroseServer.py'])
        # while 1 :
        return self

# if __name__ == '__main__':


if __name__ == '__main__':
    Penrose.run()

    # PeriodicExecutor().run()


    # time.sleep(10)
    # os.system("TASKKILL /F /IM /usr/bin/python2.7 /home/zyan/PycharmProjects/PenrosePython/pythonPenroseServer.py")
    # time.sleep(5)
    # MyPaintApp().stop()
    # threading.Timer(15.0, self.stop()).start()
