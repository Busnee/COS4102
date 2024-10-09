import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import sys

switch_order = False
def on_keyboard(key, x, y):
    global switch_order
    while(True):
        if key.lower() == b'a':
            switch_order = not switch_order
        break
    print(key)
    glut.glutPostRedisplay()

    return

def initGL():
    gl.glClearColor(1.0, 1.0, 1.0, 0.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    glu.gluLookAt(0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-4, 4, -4, 4, 4, 20)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_DST_ALPHA)

    return

def blend(source_color, destination_color, source_alpha, destination_alpha):
    blend_source = [ (source_alpha * c) for c in source_color]
    blend_destination =  [ (destination_alpha * c) for c in destination_color]
    blend_color = [ (s + d) for s, d in zip(blend_source, blend_destination)]
    for i in range(blend_color.__len__()):
        if (blend_color[i] > 1):
            blend_color[i] = 1
    print("source ", source_color)
    print("destination ", destination_color)
    print("blend ", blend_color) 

    return tuple(blend_color)

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT) 
    solidSphere_color = (0.8, 0.0, 0.0, 0.4)
    quads_color = (0.0, 0.0, 0.8, 0.7)
    if switch_order:
        print(1)
        blend_color = blend(solidSphere_color, quads_color, solidSphere_color[3], quads_color[3])
        # bule box
        gl.glPushMatrix()
        gl.glTranslate(-1.0, 1.0, 0.0)
        gl.glColor4f(quads_color[0], quads_color[1], quads_color[2], quads_color[3])
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(-2, 2)
        gl.glVertex2f(2, 2)
        gl.glVertex2f(2, -2)
        gl.glVertex2f(-2, -2)
        gl.glEnd()
        gl.glPopMatrix()
        # red ball
        gl.glPushMatrix()
        gl.glTranslate(1.0, 1.0, 0.8)
        gl.glColor4f(solidSphere_color[0], solidSphere_color[1], solidSphere_color[2], solidSphere_color[3])
        glut.glutSolidSphere(2.0, 60, 60)
        gl.glPopMatrix()
        # blend color obj.
        gl.glPushMatrix()
        gl.glTranslate(3.0, -2., 0.0)
        gl.glColor4f(blend_color[0], blend_color[1], blend_color[2], blend_color[3])
        glut.glutSolidSphere(0.75, 60, 60)
        gl.glPopMatrix()
    else:
        print(2)
        blend_color = blend(quads_color, solidSphere_color, quads_color[3], solidSphere_color[3])
        # red ball
        gl.glPushMatrix()
        gl.glTranslate(1.0, 1.0, 0.8)
        gl.glColor4f(solidSphere_color[0], solidSphere_color[1], solidSphere_color[2], solidSphere_color[3])
        glut.glutSolidSphere(2.0, 60, 60)
        gl.glPopMatrix()
        # bule box
        gl.glPushMatrix()
        gl.glTranslate(-1.0, 1.0, 0.0)
        gl.glColor4f(quads_color[0], quads_color[1], quads_color[2], quads_color[3])
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(-2, 2)
        gl.glVertex2f(2, 2)
        gl.glVertex2f(2, -2)
        gl.glVertex2f(-2, -2)
        gl.glEnd()
        gl.glPopMatrix()
        # blend color obj.
        gl.glPushMatrix()
        gl.glTranslate(3.0, -2., 0.0)
        gl.glColor4f(blend_color[0], blend_color[1], blend_color[2], blend_color[3])
        glut.glutSolidSphere(0.75, 60, 60)
        gl.glPopMatrix()

    gl.glFlush()

    return

def  main():
    glut.glutInit(sys.argv)
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(0, 0)
    glut.glutInitDisplayMode(glut.GLUT_SINGLE | glut.GLUT_RGB)
    glut.glutCreateWindow("Homework_5")
    initGL()
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutMainLoop()

    return

if __name__ == "__main__":
    main()