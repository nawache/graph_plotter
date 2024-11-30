import math
import sys
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

# x_unit = 40
# y_unit = 40

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

    def draw_x_grid(self, x):
        pg.draw.line(screen, LIGHT_GREEN, (x, 0), (x, HEIGHT), 1) 

    def draw_y_grid(self, y):
        pg.draw.line(screen, LIGHT_GREEN, (0, y), (WIDTH, y), 1) 

    def draw_grid(self):
        [self.draw_x_grid(x) for x in self.x_axis_values]
        [self.draw_y_grid(y) for y in self.y_axis_values]

    def draw(self):
        self.draw_grid()
        pg.draw.line(screen, BLACK, (0, self.y_0), (WIDTH, self.y_0), 1)
        pg.draw.line(screen, BLACK, (self.x_0, 0), (self.x_0, HEIGHT), 1)
        self.draw_notches()


class Graph:

    def __init__(self, zero, units, functn, color, A, B):
        n = int((B - A) // dx)
        original_x_values = [round(A + k * dx, 1) for k in range(0, n + 2)]
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


# def get_input():
#     graphs = []
#     colors = []
#     borders = []
#     while True:
#         graph_input = input("Введите выражение (переменная - x) и цвет графика через запятую:\n").strip().split(", ")
#         graph_func, color = graph_input
#         graphs.append(graph_func)
#         colors.append(color)

#         borders_input = input("Введите границы для участка графика через запятую:\n")
#         if not borders_input:
#             borders.append(DEFAULT_BORDERS)
#         else:
#             borders.append([float(element) for element in borders_input.strip().split(", ")])

#         response = input("Добавить ещё выражение? y/n\n")
#         if response.strip().lower() in ("y", "yes"):
#             continue
#         break

#     return graphs, colors, borders

def draw_graph_objects(graph_objects):
    [graph_object.draw() for graph_object in graph_objects]

def create_graph_objects(zero, units):
    # graphs, colors, borders = get_input()
    # return [Graph(graphs[i], colors[i], *borders[i]) for i in range(len(graphs))]
    expression0 = Graph(zero, units, "(1 / math.sqrt(2 * math.pi) * 1) * math.exp(-0.5 * ((x - 0) / 1)**2)", BLUE, -8, 9.2)
    expression1 = Graph(zero, units, "x**3 - 2*x**2 + 6",RED, -6, 6)
    expression2 = Graph(zero, units, "3*x**2 - 4*x", GREEN, -6, 6)
    expression3 = Graph(zero, units, "math.sin(x)", PURPLE, -20, 20)
    return (expression0, expression1, expression2, expression3)

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
                    print(axes.n_x, axes.n_y)
                    print(axes.n_dx, axes.n_dy)
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
