import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import sys

xe, ye, ze = 0.0, 0.1, 10.0
light, blend = False, False
project = 1
y_ball = 2.0
step = 0.003
low, high = 2.0, 7.0

def on_keyboard(key, x, y):
    global project, light, blend
    while(True):
        print(key)
        # Lighting
        if key.lower() == b'l':
            light = not light
            break
        # Blending
        if key.lower() == b'b':
            blend = not blend
            break
        # Frustum
        if key.lower() == b'f':
            project = 1
            break
        # Perspective
        if key.lower() == b'p':
            project = 2
            break
        # Orthogonal
        if key.lower() == b'o':
            project = 3
            break
        break
    glut.glutPostRedisplay()

    return
def on_arrowKey(key, x, y):
    global ye
    # move camera
    while(True):
        if key == glut.GLUT_KEY_UP:
            ye = ye + 0.1
            break
        if key == glut.GLUT_KEY_DOWN:
            ye = ye - 0.1
            break
        break
    glut.glutPostRedisplay()

    return

def myIdel():
    global y_ball, step, low, high
    if y_ball >= high or y_ball < low:
        step = -step
    y_ball = y_ball + step    
    # print(y_ball)
    glut.glutPostRedisplay()

    return

def initGL():
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    setup_lighting()

    return

def set_view():
    global xe, ye, ze
    global project
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    if project == 1:
        gl.glFrustum(-4, 4, -4, 4, 4, 20)
    elif project == 2: 
        glu.gluPerspective(60.0, 1.0, 4., 20.)
    else:
        gl.glOrtho(-4, 4, -4, 4, 4, 20)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    glu.gluLookAt(xe, ye, ze, 0, 0, 0, 0, 1, 0)

    return

def set_blend():
    if blend:
        gl.glEnable(gl.GL_BLEND)
        gl.glDisable(gl.GL_DEPTH_TEST)
    else:
        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)

    return

def set_lighting():
    if light:
        gl.glEnable(gl.GL_LIGHTING)
    else:
        gl.glDisable(gl.GL_LIGHTING)

    return

def setup_lighting():
    gl.glEnable(gl.GL_LIGHT0)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE,[1.0, 1.0, 1.0, 0.8 ])
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.8, 0.8, 0.8, 0.6])
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1.0, 1.0, 1.0, 0])

    return

def display():
    global y_ball
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    set_view()
    set_blend()
    set_lighting()

    # glass plane
    gl.glPushMatrix()
    gl.glColor4f(1.0, 1.0, 1.0, 0.4)
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE ,[0.0, 0.0, 0.5, 0.4 ])
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [0.0, 0.1, 0.2, 0.3 ])
    gl.glBegin(gl.GL_POLYGON)
    gl.glVertex3f(-5, 0, -5)
    gl.glVertex3f(5, 0, -5)
    gl.glVertex3f(5, 0, 5)
    gl.glVertex3f(-5, 0, 5)
    gl.glEnd()
    gl.glPopMatrix()

    # red ball
    gl.glPushMatrix()
    gl.glTranslate(0.0, y_ball, 0.0)
    gl.glColor4f(1.0, 0.0, 0.0, 0.8)
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE ,[0.8, 0., 0., 0.8 ])
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [0.5, 0.0, 0.0, 0.5 ])
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [1.0, 1.0, 1.0, 1.0 ])
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 50.0)
    glut.glutSolidSphere(2.0, 60, 60)
    gl.glPopMatrix()

    # orange ball
    gl.glPushMatrix()
    gl.glTranslate(0.0, -y_ball, 0.0)
    gl.glColor4f(1.0, 0.7, 0.0, 0.7)
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE ,[0.7, 0.5, 0., 0.7 ])
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [0.3, 0.2, 0.0, 0.3 ])
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [1.0, 1.0, 1.0, 1.0 ])
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 60.0)
    glut.glutSolidSphere(2.0, 60, 60)
    gl.glPopMatrix()

    gl.glFlush()

    return

def main():
    glut.glutInit(sys.argv)
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(0, 0)
    glut.glutInitDisplayMode(glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutCreateWindow("Homework_3")
    initGL()
    glut.glutDisplayFunc(display)
    glut.glutIdleFunc(myIdel)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutSpecialFunc(on_arrowKey)
    glut.glutMainLoop()

    return

if __name__ == "__main__":
    main()