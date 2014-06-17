import random
from pyage.core.inject import Inject
import pyglet
import sys
from pyage.core import inject

inject.config = 'langtons_ant.conf'


class AnimationParams(object):
    @Inject("net_dimensions", "net_agents_per_line", "net_agents_per_host", "number_of_hosts")
    def __init__(self):
        pass

    def get_parameters(self):
        return self.net_agents_per_line, self.number_of_hosts, self.net_dimensions.x, self.net_dimensions.y


i = 1
ants = {}
animation = True
moreFiles = True
first = True
second = False
third = False
tile_width = 13
tile_height = 13
display_iteration = 0
if len(sys.argv) == 2:
    display_iteration = int(sys.argv[1])
    animation = False

animation_params = AnimationParams().get_parameters()

agents_per_line = animation_params[0]
agents_count = animation_params[1]
x = animation_params[2]
y = animation_params[3]
nets_x = agents_per_line
nets_y = agents_count / agents_per_line


def next_step(dt):
    global i, moreFiles
    try:
        if moreFiles:
            with open('../positions/langtons_ant_positions_' + str(i).zfill(5) + '.txt') as f:
                content = f.read().splitlines()
                for line in content:
                    args = line.split(' ')
                    agent_number = args[0]
                    x_pos = int(args[1])
                    y_pos = int(args[2])
                    color = int(args[3])
                    direction = int(args[4])
                    global ants
                    if agent_number in ants.keys():
                        ants[agent_number].append([x_pos, y_pos, color, direction])
                    else:
                        ants[agent_number] = [[x_pos, y_pos, color, direction]]
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

net_height_px = nets_y * (y * tile_height + y - 1) + 2 * nets_y - 1
net_width_px = nets_x * (x * tile_width + x - 1) + 2 * nets_x - 1

if net_height_px > screen_height:
    tile_height = (screen_height - (nets_y * y + 2 * (nets_y - 1))) / (nets_y * (y + 1))
if net_width_px > screen_width:
    tile_width = (screen_width - (nets_x * x + 2 * (nets_x - 1))) / (nets_x * (x + 1))
ant_scale = min(tile_width, tile_height) * 1.0 / 13.0

window.set_size(nets_x * (x * tile_width + x - 1) + 2 * (nets_x - 1),
                nets_y * (y * tile_height + y - 1) + 2 * (nets_y - 1))

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
    draw_ants_path()
    draw_ants_image()


def draw_ants_path():
    for ant in ants:
        min_step = 0
        max_step = len(ants[ant]) - 1
        if display_iteration == 0:
            if len(ants[ant]) > 3:
                min_step = len(ants[ant]) - 4
        else:
            max_step = display_iteration
        if max_step < i:
            max_step = max_step if display_iteration == 0 else min(display_iteration, len(ants[ant]))
            for step in range(min_step, max_step):
                set_color(ant, ants[ant][step][2])
                x_offset = (ants[ant][step][0] / x) * 2
                y_offset = (ants[ant][step][1] / y) * 2
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (
                    x_offset + ants[ant][step][0] * (tile_width + 1),
                    y_offset + ants[ant][step][1] * (tile_height + 1),
                    x_offset + ants[ant][step][0] * (tile_width + 1),
                    y_offset + tile_height + ants[ant][step][1] * (tile_height + 1),
                    x_offset + tile_width + ants[ant][step][0] * (tile_width + 1),
                    y_offset + tile_height + ants[ant][step][1] * (tile_height + 1),
                    x_offset + tile_width + ants[ant][step][0] * (tile_width + 1),
                    y_offset + ants[ant][step][1] * (tile_height + 1))))


def draw_ants_image():
    global i, display_iteration
    for ant in ants:
        if display_iteration == 0:
            max_step = len(ants[ant]) - 1
        else:
            max_step = display_iteration
        if max_step < i:
            max_step = max_step if display_iteration == 0 else min(display_iteration, len(ants[ant]))
            position = ants[ant][max_step - 1]
            set_color(ant, position[2])
            x_offset = (position[0] / x) * 2
            y_offset = (position[1] / y) * 2
            ant_sprite = draw_rotated_ant(position[3])
            ant_sprite.set_position(position[0] * (tile_width + 1) + x_offset,
                                    position[1] * (tile_height + 1) + y_offset)
            ant_sprite.scale = ant_scale
            ant_sprite.draw()


def draw_background():
    global first, second, third
    if third:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        draw_nets()
        third = False
    if second:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        draw_nets()
        second = False
        third = True
    if first:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        draw_nets()
        first = False
        second = True


def draw_nets():
    global x, y
    for k in range(0, agents_count):
        x_start = k % agents_per_line
        y_start = k / agents_per_line
        draw_net(x_start * x * (tile_width + 1) + x_start * 2,
                 y_start * y * (tile_height + 1) + y_start * 2,
                 x,
                 y)


def draw_net(x, y, x_dim, y_dim):
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    for i in range(0, x_dim):
        for j in range(0, y_dim):
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (x + i * (tile_width + 1),
                                                                 y + j * (tile_height + 1),
                                                                 x + i * (tile_width + 1),
                                                                 y + tile_height + j * (tile_height + 1),
                                                                 x + tile_width + i * (tile_width + 1),
                                                                 y + tile_height + j * (tile_height + 1),
                                                                 x + tile_width + i * (tile_width + 1),
                                                                 y + j * (tile_height + 1))))


def set_color(color, on):
    if on == 0:
        random.seed(color)
        r = random.random()
        g = random.random()
        b = random.random()
        pyglet.gl.glColor4f(r, g, b, 1.0)
    else:
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)


def draw_rotated_ant(direction):
    return {
        0: ant_spriteW,
        1: ant_spriteS,
        2: ant_spriteE,
        3: ant_spriteN
    }[direction]


pyglet.clock.schedule_interval(next_step, 1 / 1000.0)
pyglet.app.run()
