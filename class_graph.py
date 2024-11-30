import csv
import math
import sys
from ast import literal_eval
import pygame as pg


WIDTH = 1200
HEIGHT = 800
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (211, 248, 211)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
FORESTGREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
GREY = (244, 240, 236)

dx = 0.1

h1 = 2
h2 = 4
h3 = 6

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HIDDEN)


class CoordinateSystem:

    def __init__(self, x_0, y_0, x_unit=40, y_unit=40):
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.x_0 = x_0
        self.y_0 = y_0

    @property
    def zero(self):
        return self.x_0, self.y_0
    
    @property
    def units(self):
        return self.x_unit, self.y_unit
    
    @property
    def dx_unit(self):
        return self.x_unit // 10

    @property
    def dy_unit(self):
        return self.y_unit // 10
    
    @property
    def n_x(self):
        return int(WIDTH // self.x_unit)
    
    @property
    def n_y(self):
        return int(HEIGHT // self.y_unit)
    
    @property
    def n_dx(self):
        return int(WIDTH // self.dx_unit)

    @property
    def n_dy(self):
        return int(HEIGHT // self.dy_unit)
    
    
    def notch_size(self, axis, axis_unit):
        if axis % axis_unit == 0:   
            notch_size = h3
        elif axis % axis_unit == 0.5 * axis_unit:   
            notch_size = h2
        else:
            notch_size = h1
        return notch_size
    
    @property
    def x_axis_values(self):
        if self.x_unit < 20:
            self.x_unit = 20
        return [round(0 + k * self.x_unit, 1) for k in range(0, self.n_x + 1)]
    
    @property
    def y_axis_values(self):
        if self.y_unit < 20:
            self.y_unit = 20
        return [round(0 + k * self.y_unit, 1) for k in range(0, self.n_y + 1)]

    @property
    def dx_axis_values(self):
        return [round(0 + k * self.dx_unit, 1) for k in range(0, self.n_dx + 1)]

    @property
    def dy_axis_values(self):
        return[round(0 + k * self.dy_unit, 1) for k in range(0, self.n_dy + 1)]

    def draw_x_notch(self, x):
        size = self.notch_size(x, self.x_unit)
        pg.draw.line(screen, BLACK, (x, self.y_0 - size), (x, self.y_0 + size), 1) 

    def draw_y_notch(self, y):
        size = self.notch_size(y, self.y_unit)
        pg.draw.line(screen, BLACK, (self.x_0 - size, y), (self.x_0 + size, y), 1)

    def draw_notches(self):
        [self.draw_x_notch(x) for x in self.dx_axis_values]
        [self.draw_y_notch(y) for y in self.dy_axis_values]

    def draw_x_grid(self, x, grid_color):
        pg.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1) 

    def draw_y_grid(self, y, grid_color):
        pg.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1) 

    def draw_grid(self):
        [self.draw_x_grid(x, LIGHT_GREEN) for x in self.x_axis_values]
        [self.draw_y_grid(y, LIGHT_GREEN) for y in self.y_axis_values]

    def draw_extra_grid(self):
        [self.draw_x_grid(x, GREY) for x in self.dx_axis_values]
        [self.draw_y_grid(y, GREY) for y in self.dy_axis_values]
    
    def draw(self):
        self.draw_grid()
        pg.draw.line(screen, BLACK, (0, self.y_0), (WIDTH, self.y_0), 1)
        pg.draw.line(screen, BLACK, (self.x_0, 0), (self.x_0, HEIGHT), 1)
        self.draw_notches()


class Graph:

    def __init__(self, zero, units, functn, color, borders):
        self.A = borders[0]
        self.B = borders[1]

        n = int((self.B - self.A) // dx)

        original_x_values = [round(self.A + k * dx, 1) for k in range(0, n + 2)]

        self.x_0 = zero[0]
        self.y_0 = zero[1]

        self.x_unit = units[0]
        self.y_unit = units[1]

        self.functn = functn
        self.color = color

        self.x_values = [x * self.x_unit + self.x_0 for x in original_x_values]
        self.y_values = [self.y_0 - (eval(self.functn)) * self.y_unit for x in original_x_values]

    def draw(self):
        for i in range(1, len(self.x_values)):
            pg.draw.line(screen, self.color, (self.x_values[i - 1], self.y_values[i - 1]), 
                          (self.x_values[i], self.y_values[i]), 1)


def get_input():
    with open("graphs.csv", mode = 'r') as file:
        reader = csv.reader(file, delimiter = ";")
        graphs = []
        colors = []
        borders = []
        count = 0
        for i, row in enumerate(reader):
                if i == 0:
                    continue
                else:
                    if row[0][0] == '#':
                        continue
                    else:
                        graphs.append(row[0])
                        colors.append(row[1])
                        borders.append(literal_eval(row[2]))

    return graphs, colors, borders

def create_graph_objects(zero, units):
    graphs, colors, borders = get_input()
    return [Graph(zero, units, graphs[i], colors[i], borders[i]) for i in range(len(graphs))]

def draw_graph_objects(graph_objects):
    [graph_object.draw() for graph_object in graph_objects]

def get_new_center(zero, units):
    x_unit, y_unit = units
    x_pos, y_pos = zero
    new_x_pos_1 = x_pos - (x_pos % x_unit)
    new_y_pos_1 = y_pos - (y_pos % y_unit)
    return new_x_pos_1, new_y_pos_1

def get_new_center_mouse(x_pos, y_pos, units):
    x_unit, y_unit = units
    new_x_pos_1 = x_pos - (x_pos % x_unit)
    new_y_pos_1 = y_pos - (y_pos % y_unit) + y_unit
    return new_x_pos_1, new_y_pos_1

def main():
    global x_unit, y_unit
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SHOWN)
    pg.display.set_caption("My Graph")

    screen.fill(WHITE)
    axes = CoordinateSystem(WIDTH // 2, HEIGHT // 2)
    my_graphs = create_graph_objects(axes.zero, axes.units)
    axes.draw()
    draw_graph_objects(my_graphs)
    pg.display.update()

    running = True
    while running:
        clock.tick(15)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            axes.x_0 += axes.x_unit
            axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
            my_graphs = create_graph_objects(axes.zero, axes.units)
            screen.fill(WHITE)
            axes.draw()
            draw_graph_objects(my_graphs)
            pg.display.update()
        if keys[pg.K_UP]:
            axes.y_0 -= axes.y_unit
            axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
            my_graphs = create_graph_objects(axes.zero, axes.units)
            screen.fill(WHITE)
            axes.draw()
            draw_graph_objects(my_graphs)
            pg.display.update()
        if keys[pg.K_LEFT]:
            axes.x_0 -= axes.x_unit
            axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
            my_graphs = create_graph_objects(axes.zero, axes.units)
            screen.fill(WHITE)
            axes.draw()
            draw_graph_objects(my_graphs)
            pg.display.update()
        if keys[pg.K_DOWN]:
            axes.y_0 += axes.y_unit
            axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
            my_graphs = create_graph_objects(axes.zero, axes.units)
            screen.fill(WHITE)
            axes.draw()
            draw_graph_objects(my_graphs)
            pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_8:
                    axes.y_unit *= 2
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_2:
                    axes.y_unit *= 0.5
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_6:
                    axes.x_unit *= 2
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_4:
                    axes.x_unit *= 0.5
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()

                if event.key == pg.K_KP_MINUS:
                    axes.x_unit *= 0.5
                    axes.y_unit *= 0.5
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_PLUS:
                    axes.x_unit *= 2
                    axes.y_unit *= 2
                    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_0:    
                    axes.x_unit = 40
                    axes.y_unit = 40
                    axes.x_0 = WIDTH // 2
                    axes.y_0 = HEIGHT // 2
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    screen.fill(WHITE)
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
                if event.key == pg.K_KP_DIVIDE:
                    screen.fill(WHITE)
                    axes.draw_extra_grid()
                    axes.draw()
                    draw_graph_objects(my_graphs)
                    pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                x_pos, y_pos = pg.mouse.get_pos()
                axes.x_0, axes.y_0 = get_new_center_mouse(x_pos, y_pos, axes.units)
                my_graphs = create_graph_objects(axes.zero, axes.units)
                screen.fill(WHITE)
                axes.draw()
                draw_graph_objects(my_graphs)
                pg.display.update()


if __name__ == '__main__':
    main()