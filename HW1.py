import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import sys

# not use in this program
INSIDE  = 0  # 0000 
LEFT    = 1    # 0001 
RIGHT   = 2   # 0010 
BOTTOM  = 4  # 0100 
TOP     = 8     # 1000 

# Object
p = []
p_temp = []
p_copy = []

# Frame
XMax = 250
YMax = 250
XMin = -XMax
YMin = -YMax

def setPoint():
    global p, p_copy
    p = [[-350., 200.], [-50., 350.], 
         [300., 200.], [150., 100.], 
         [370., -50.], [150., -300.], 
         [0., -100.], [-150., -300.],  
         [-370., -50.], [-70., 120.]]
    p_copy = p

    return

def ClipObj():
    global p, p_temp
    for s in range(4):
        p_temp = []
        m = len(p)
        for i in range(m):  # 10 times 0-9
            print(i)
            if i ==  m-1:
                ClipSide(p[i], p[0], s)
            else:
                ClipSide(p[i], p[i+1], s)
        p = p_temp
    
    print(p)

    return

def ClipSide(s, p, side):
    global p_temp
    sx, sy = s
    px, py = p

    # หาความชัน
    dy = py - sy    # ระยะห่าง
    dx = px - sx
    if dx == 0:
        dx = 0.000000001
    m = dy / dx     # ความชัน

    # left Side
    if side == 0:
        if px >= XMin:  # p inside
            if sx < XMin:   # s outside(หาi/จุดตัด)
                y = py - m*(px - XMin)
                x = XMin
                p_temp.append([x,y]) # เก็บ i
            p_temp.append(p) # เก็บ p
        else: # p outside
            if sx >= XMin: # s inside(หาi/จุดตัด)
                y = py - m*(px - XMin)
                x = XMin
                p_temp.append([x,y]) # เก็บ i
        # out ทั้งคู่ ไม่เก็บ

    # Right Side
    elif side == 1:           
        if px <= XMax:
            if sx > XMax:
                y = py - m*(px - XMax)
                x = XMax
                p_temp.append([x,y])
            p_temp.append(p)
        else:
            if sx <= XMax:
                y = py - m*(px - XMax)
                x = XMax
                p_temp.append([x,y])

    # Bottom Side
    elif side == 2:     
        if py >= YMin:
            if sy < YMin:
                x = px - (py - YMin)/m
                y = YMin
                p_temp.append([x,y])
            p_temp.append(p)
        else:
            if sy >= YMin:
                x = px - (py - YMin)/m
                y = YMin
                p_temp.append([x,y])

    # Top side
    elif side == 3:
        if py <= YMax:
            if sy > YMax:
                x = px - (py - YMax)/m
                y = YMax
                p_temp.append([x,y])
            p_temp.append(p)
        else:
            if sy <= YMax:
                x = px - (py - YMax)/m
                y = YMax
                p_temp.append([x,y])
        
    return


def initGL():
    gl.glClearColor(1.0, 1.0, 0.0, 0.0)
    # gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluOrtho2D(-400, 400, -400, 400)
    setPoint()

    return

def clip(): # draw and clip
    # Object
    gl.glPushMatrix()
    gl.glColor3f(0.0, 0.0, 1.0)
    gl.glBegin(gl.GL_POLYGON)
    for i in p:
        gl.glVertex2f(i[0],i[1])
    gl.glEnd()
    gl.glPopMatrix()

    #Frame
    gl.glPushMatrix()
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_POLYGON)
    gl.glVertex2f(XMin, YMax)
    gl.glVertex2f(XMax, YMax)
    gl.glVertex2f(XMax, YMin)
    gl.glVertex2f(XMin, YMin)
    gl.glEnd()
    ClipObj()

    return

def display():
    global p_copy
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Object before clip(blue)
    gl.glPushMatrix()
    gl.glColor3f(0.0, 0.0, 1.0)
    gl.glBegin(gl.GL_POLYGON)
    for i in p_copy:
        gl.glVertex2f(i[0],i[1])
    gl.glEnd()
    gl.glPopMatrix()

    # Object after clip(yellow)
    gl.glPushMatrix()
    gl.glColor3f(1.0, 1.0, 0.0)
    gl.glBegin(gl.GL_POLYGON)
    for i in p:
        gl.glVertex2f(i[0],i[1])
    gl.glEnd()
    gl.glPopMatrix()

    # #Frame(red)
    gl.glPushMatrix()
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_POLYGON)
    gl.glVertex2f(XMin, YMax)
    gl.glVertex2f(XMax, YMax)
    gl.glVertex2f(XMax, YMin)
    gl.glVertex2f(XMin, YMin)
    gl.glEnd()
    gl.glPopMatrix()

    gl.glFlush()

    return

def  main():
    glut.glutInit(sys.argv)
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(0, 0)
    glut.glutInitDisplayMode(glut.GLUT_SINGLE | glut.GLUT_RGB)
    glut.glutCreateWindow("Homework_1")
    initGL()
    clip()
    glut.glutDisplayFunc(display)
    glut.glutMainLoop()

    return

if __name__ == "__main__":
    main()