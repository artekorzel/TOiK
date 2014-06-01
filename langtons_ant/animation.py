import random
import pyglet
import sys

i = 1
ants = {}
animation = True
moreFiles = True
first = True
second = False
third = False
tile_width = 13;
tile_height = 13;
nets_y = 0
nets_x = 0
display_iteration = 0
if len(sys.argv) == 2:
    display_iteration = int(sys.argv[1])
    animation = False


with open('../config.txt') as f:
    content = f.read()
    args = content.split(' ')
    x = int(args[0])
    y = int(args[1])
    agents_per_line = int(args[2])
    agents_count = int(args[3])
    nets_x = agents_per_line
    nets_y = agents_count/agents_per_line


def next_step(dt):
    global i, moreFiles
    try:
        if moreFiles:
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
    except IOError:
        moreFiles = False
        pass


window = pyglet.window.Window(resizable=False)
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
screen_height = screen.height
screen_width = screen.width

if (nets_y)*(y*tile_height+y-1)+2*(nets_y)-1 > screen_height:
    tile_height = (screen_height - (nets_y * y + 2 * (nets_y - 1)))/(nets_y * (y + 1))
if nets_x*(x*tile_width+x-1)+2*(nets_x)-1 > screen_width:
    tile_width = (screen_width - (nets_x * x + 2 * (nets_x -1)))/(nets_x * (x + 1))
ant_scale = min(tile_width, tile_height)* 1.0/13.0
print nets_x, x, tile_width
print nets_y, y, tile_height
print (nets_y)*(y*tile_height+y-1)+2*(nets_y)-1
window.set_size(nets_x*(x*tile_width+x-1)+2*(nets_x)-1, (nets_y)*(y*tile_height+y-1)+2*(nets_y-1))



ant_spriteN = pyglet.sprite.Sprite(pyglet.image.load('antN.png'))
ant_spriteS = pyglet.sprite.Sprite(pyglet.image.load('antS.png'))
ant_spriteW = pyglet.sprite.Sprite(pyglet.image.load('antW.png'))
ant_spriteE = pyglet.sprite.Sprite(pyglet.image.load('antE.png'))


@window.event
def on_draw():
    draw_one_step()


def draw_one_step():
    global display_iteration, i
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    draw_background()
    for ant in ants:
        min = 0
        max = len(ants[ant])-1
        if display_iteration == 0:
            if len(ants[ant]) > 3:
                min = len(ants[ant])-4
        else:
            max = display_iteration
        if max < i:
            for step in range(min, max):
                set_color(ant, ants[ant][step][2])
                x_offset = (ants[ant][step][0]/x)*2
                y_offset = (ants[ant][step][1]/y)*2
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,('v2i', (
                    x_offset+ants[ant][step][0]*(tile_width+1),
                    y_offset+ants[ant][step][1]*(tile_height+1),
                    x_offset+ants[ant][step][0]*(tile_width+1),
                    y_offset+tile_height+ants[ant][step][1]*(tile_height+1),
                    x_offset+tile_width+ants[ant][step][0]*(tile_width+1),
                    y_offset+tile_height+ants[ant][step][1]*(tile_height+1),
                    x_offset+tile_width+ants[ant][step][0]*(tile_width+1),
                    y_offset+ants[ant][step][1]*(tile_height+1))))
    for ant in ants:
        if display_iteration == 0:
            max = len(ants[ant])-1
        else:
            max = display_iteration
        if max < i:
            position = ants[ant][max-1]
            set_color(ant, position[2])
            x_offset = (position[0]/x)*2
            y_offset = (position[1]/y)*2
            ant_sprite = draw_rotated_ant(position[3])
            ant_sprite.set_position(position[0]*(tile_width+1)+x_offset, position[1]*(tile_height+1) + y_offset)
            ant_sprite.scale = ant_scale
            ant_sprite.draw()

    # image.blit(0,0)

def draw_background():
    global first, second, third, x, y
    if third:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        for k in range(0, agents_count):
            x_start = k % agents_per_line
            y_start = k / agents_per_line
            draw_net(x_start * x * (tile_width+1) + x_start * 2,
                     y_start * y * (tile_height+1) + y_start * 2,
                     x,
                     y)
        third = False
    if second:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        for k in range(0, agents_count):
            x_start = k % agents_per_line
            y_start = k / agents_per_line
            draw_net(x_start * x * (tile_width+1) + x_start * 2,
                     y_start * y * (tile_height+1) + y_start * 2,
                     x,
                     y)
        second = False
        third = True
    if first:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        for k in range(0, agents_count):
            x_start = k % agents_per_line
            y_start = k / agents_per_line
            draw_net(x_start * x * (tile_width+1) + x_start * 2,
                     y_start * y * (tile_height+1) + y_start * 2,
                     x,
                     y)
        first = False
        second = True

def draw_net(x, y, x_dim, y_dim):
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    for i in range(0, x_dim):
        for j in range(0, y_dim):
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,('v2i', (x+i*(tile_width+1),
                                                                y+j*(tile_height+1),
                                                                x+i*(tile_width+1),
                                                                y+tile_height+j*(tile_height+1),
                                                                x+tile_width+i*(tile_width+1),
                                                                y+tile_height+j*(tile_height+1),
                                                                x+tile_width+i*(tile_width+1),
                                                                y+j*(tile_height+1))))

def set_color(color, on):
    if(on == 0):
        random.seed(color)
        r = random.random()
        g = random.random()
        b = random.random()
        pyglet.gl.glColor4f(r,g,b,1.0)
    else:
        pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

def draw_rotated_ant(direction):
    return {
        0:ant_spriteW,
        1:ant_spriteS,
        2:ant_spriteE,
        3:ant_spriteN
    }[direction]

pyglet.clock.schedule_interval(next_step, 1/1000.0)
pyglet.app.run()
