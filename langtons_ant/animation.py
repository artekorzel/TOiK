import pyglet
from pyage.core.inject import Inject

i = 1
ants = {}
first = True

with open('../config.txt') as f:
    content = f.read()
    args = content.split(' ')
    x = int(args[0])
    y = int(args[1])
    xAgents = int(args[2])

def next_step(dt):
    global i
    with open('../positions/langtons_ant_positions_' + str(i).zfill(5)+'.txt') as f:
        content = f.read().splitlines()
        for line in content:
            args = line.split(' ')
            agentNr = int(args[0].split('.')[0])
            xPos = int(args[1])
            yPos = int(args[2])
            color = int(args[3])
            direction = int(args[4])
            global ants
            if agentNr in ants.keys():
                ants[agentNr].append([xPos, yPos, color, direction])
            else:
                ants[agentNr] = [[xPos, yPos, color, direction]]
    i += 1


window = pyglet.window.Window(resizable=False)
window.set_size(xAgents*(x*13+x-1)+2*(xAgents)-1, y*13+y-1)
ant_imageN = pyglet.image.load('antN.png')
ant_imageS = pyglet.image.load('antS.png')
ant_imageW = pyglet.image.load('antW.png')
ant_imageE = pyglet.image.load('antE.png')


@window.event
def on_draw():
    # global first
    # if first:
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    for k in range(0, xAgents):
        draw_net(k*x*14+k*2, 0, x, y)
        # first = False
    for ant in ants:
        # print ant
        for i in range(0, len(ants[ant])-1):
        # for position in ants[ant]:
            set_color(ant, ants[ant][i][2])
            offset = (ants[ant][i][0]/x)*2
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,('v2i', (offset+ants[ant][i][0]*14,0+ants[ant][i][1]*14,offset+ants[ant][i][0]*14,13+ants[ant][i][1]*14,offset+13+ants[ant][i][0]*14,13+ants[ant][i][1]*14,offset+13+ants[ant][i][0]*14,0+ants[ant][i][1]*14)))
        position = ants[ant][len(ants[ant])-1]
        set_color(ant, position[2])
        offset = (position[0]/x)*2
        draw_rotated_ant(position[3]).blit(position[0]*14+offset, position[1]*14)

    # image.blit(0,0)

def draw_net(x, y, x_dim, y_dim):
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    for i in range(0, x_dim):
        for j in range(0, y_dim):
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,('v2i', (x+i*14,j*14,x+i*14,13+j*14,x+13+i*14,13+j*14,x+13+i*14,j*14)))

def set_color(color, on):
    if(on == 0):
        if(color == 1):
            pyglet.gl.glColor4f(1.0,0,0,1.0)
        elif(color == 2):
            pyglet.gl.glColor4f(0,1.0,0,1.0)
        elif(color == 4):
            pyglet.gl.glColor4f(0,0,1.0,1.0)
        elif(color == 5):
            pyglet.gl.glColor4f(0.5,1.0,0,1.0)
    else:
        pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

def draw_rotated_ant(direction):
    return {
        0:ant_imageE,
        1:ant_imageS,
        2:ant_imageW,
        3:ant_imageN
    }[direction]

pyglet.clock.schedule_interval(next_step, 1/600.0)
pyglet.app.run()
