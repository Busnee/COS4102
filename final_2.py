import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import sys
import math
from PIL import Image

theta_planet = 0.0
theta_view = 0.0
theta_light = 0.0
sign = 1.0
xe, ye, ze = 0.0, 0.0, 8.0
current_space = 0
light_enable = False

def load_image_to_texture(filename):
    img = Image.open(filename)
    img_data = img.tobytes("raw", "RGB", 0, -1)
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.size[0], img.size[1], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    return texture_id

def initGL():
    global list_texture_id_space, current_space
    global texture_id_venus, texture_id_world, texture_id_jupiter
    # gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    setup_lighting()

    list_texture_id_space = []
    list_texture_id_space.append(load_image_to_texture('./scales/universe.jpg'))
    list_texture_id_space.append(load_image_to_texture('./scales/galaxy.jpg'))
    # list_texture_id_space.append(load_image_to_texture('./scales/sky.jpg'))
    # list_texture_id_space.append(load_image_to_texture('./scales/colorful.jpg'))
    # list_texture_id_space.append(load_image_to_texture('./scales/nebula.jpg'))

    texture_id_venus = load_image_to_texture('./scales/venus.jpg')
    texture_id_world = load_image_to_texture('./scales/world.jpg')
    texture_id_jupiter = load_image_to_texture('./scales/jupiter.jpg')

    return
    
def on_keyboard(key, x, y):
    global light_enable
    while True:
        if key.lower() == b'l':
            if(light_enable):
                gl.glDisable(gl.GL_LIGHTING)
                light_enable = False
            else:
                gl.glEnable(gl.GL_LIGHTING)
                light_enable = True
        break
    glut.glutPostRedisplay()

    return

def setup_lighting():
    gl.glEnable(gl.GL_LIGHT0)
    gl.glLightfv(gl.GL_LIGHT0,gl.GL_DIFFUSE,[1.0, 1.0, 1.0, 0.8 ])  # สีของแสง
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE ,[0.8, 0.8, 0.8, 1.0 ])  # สีที่วัตถุสะท้อน
    
    return

def move_lighting():
    global theta_light
    gl.glPushMatrix()
    gl.glRotate(theta_light, 1, 0, 0)
    gl.glLightfv(gl.GL_LIGHT0,gl.GL_POSITION,[10.0, 5.0, 0.0, 0.0 ])
    gl.glPopMatrix()

def setView():
    global xe, ye, ze
    a = (theta_view * math.pi)/180
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    # gl.glOrtho(-4, 4, -4, 4, 4, 12)
    gl.glFrustum(-2, 2, -2, 2, 2, 15)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    # x = xe*math.cos(a) - ze*math.sin(a)
    # y = ye
    # z = xe*math.sin(a) + ze*math.cos(a)
    glu.gluLookAt(xe*math.cos(a) - ze*math.sin(a), ye, xe*math.sin(a) + ze*math.cos(a), 0, 0, 0, 0, 1, 0)

    return

def display():
    global theta_view, theta_planet
    global current_space
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    setView()
    move_lighting()

    # background
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, list_texture_id_space[current_space])
    gl.glPushMatrix()
    gl.glRotate(-theta_view, 0, 1, 0)   # องศา รอบแกน
    gl.glBegin(gl.GL_QUADS)
    gl.glTexCoord2f(0, 0);  gl.glVertex3f(-15, -15, -6)
    gl.glTexCoord2f(0, 1);  gl.glVertex3f(-15, 15, -6)
    gl.glTexCoord2f(1, 1);  gl.glVertex3f(15, 15, -6)
    gl.glTexCoord2f(1, 0);  gl.glVertex3f(15, -15, -6)
    gl.glEnd()
    gl.glPopMatrix()
    gl.glDisable(gl.GL_TEXTURE_2D)
    
    # venus
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id_venus)
    gl.glPushMatrix()
    gl.glTranslate(-3.0, -2.0, -3.0)
    gl.glRotate(theta_planet, 0, 1, 0)
    gl.glTranslate(0.0, 0.0, 0.0)
    quadric = glu.gluNewQuadric()
    glu.gluQuadricTexture(quadric, gl.GL_TRUE)
    glu.gluSphere(quadric, 0.75, 60, 60)
    gl.glPopMatrix()
    gl.glDisable(gl.GL_TEXTURE_2D)

    # world
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id_world)
    gl.glPushMatrix()
    # gl.glTranslate(0.0, 0.0, 0.0)
    gl.glRotatef(theta_planet, 0, 1, 0)
    quadric = glu.gluNewQuadric()
    glu.gluQuadricTexture(quadric, gl.GL_TRUE)
    glu.gluSphere(quadric, 1.0, 60, 60)
    gl.glPopMatrix()
    gl.glDisable(gl.GL_TEXTURE_2D)

    # jupiter
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id_jupiter)
    gl.glPushMatrix()
    gl.glTranslate(3.0, 2.0, 2.5)
    gl.glRotatef(theta_planet, 0, 1, 0)
    gl.glTranslate(0.0, 0.0, 0.0)
    quadric = glu.gluNewQuadric()
    glu.gluQuadricTexture(quadric, gl.GL_TRUE)
    glu.gluSphere(quadric, 1.25, 60, 60)
    gl.glPopMatrix()
    gl.glDisable(gl.GL_TEXTURE_2D)
    glut.glutSwapBuffers()

    return

def myIdel():
    global theta_planet, theta_view, theta_light, sign
    global list_texture_id_space, current_space

    # planet
    if theta_planet >= 360.0:
        theta_planet = 0
    theta_planet = theta_planet + 0.25

    # view
    # theta_view = theta_view + (0.07 * sign)
    theta_view = theta_view + 0.07
    if ((theta_view >= 360.0) | (theta_view<=0.0)):
        theta_view = 0.0
        if current_space < (list_texture_id_space.__len__() - 1):
            current_space = current_space + 1
        else:
            current_space = 0
    # print(current_space, list_texture_id_space.__len__())
            
    # light
    theta_light = theta_light + (0.04*sign)
    if ((theta_light >= 360.0) | (theta_light <= 0.0)):
        theta_light = 0.0
        sign = sign*(-1)

    glut.glutPostRedisplay()

    return

def main():
    global list_texture_id_space
    global texture_id_venus, texture_id_world, texture_id_jupiter

    glut.glutInit(sys.argv)
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(0, 0)
    glut.glutInitDisplayMode(glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutCreateWindow("Homework_2")
    initGL()
    glut.glutDisplayFunc(display)
    glut.glutIdleFunc(myIdel)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutMainLoop()

    return

if __name__ == "__main__":
    main()