import csv
import math
import sys

from ast import literal_eval
import pygame as pg

from classes import CoordinateSystem, Graph, ParametricGraph
from constants import *

pg.init()


def get_input():
    """Reads graphs from the CSV file, supporting both standard and parametric graphs."""
    try:
        with open("graphs.csv", mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            graphs = []
            for i, row in enumerate(reader):
                if row[0].startswith("#"):
                    continue
                if len(row) == 5:  # Parametric graph
                    x_func, y_func, color, t_range, dt = row
                    t_range = eval(t_range)
                    graphs.append(("parametric", x_func, y_func,
                                  color, t_range, float(dt)))
                elif len(row) == 3:  # Standard graph
                    graphs.append(
                        ("standard", row[0], row[1], literal_eval(row[2])))
            return graphs
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)


def create_graph_objects(zero, units):
    """Create graph objects from input."""
    inputs = get_input()
    graph_objects = []
    for graph_type, *params in inputs:
        if graph_type == "parametric":
            x_func, y_func, color, t_range, dt = params
            graph_objects.append(ParametricGraph(
                zero, units, x_func, y_func, color, t_range, dt))
        elif graph_type == "standard":
            functn, color, borders = params
            graph_objects.append(Graph(zero, units, functn, color, borders))
    return graph_objects


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


def draw_all(axes):
    my_graphs = create_graph_objects(axes.zero, axes.units)
    screen.fill(WHITE)
    axes.draw()
    draw_graph_objects(my_graphs)
    pg.display.update()


def redraw(axes):
    """Recalculate and redraw the axes and graphs."""
    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
    # Prevent extremely small or zero unit sizes
    axes.x_unit = max(1, axes.x_unit)
    axes.y_unit = max(1, axes.y_unit)
    draw_all(axes)


def reset(axes):
    axes.x_unit = 40
    axes.y_unit = 40
    axes.x_0 = WIDTH // 2
    axes.y_0 = HEIGHT // 2
    draw_all(axes)


def main():
    pg.display.set_caption("My Graph")
    axes = CoordinateSystem()
    reset(axes)

    running = True
    while running:
        clock.tick(15)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            axes.x_0 += axes.x_unit
            redraw(axes)
        if keys[pg.K_UP]:
            axes.y_0 -= axes.y_unit
            redraw(axes)
        if keys[pg.K_LEFT]:
            axes.x_0 -= axes.x_unit
            redraw(axes)
        if keys[pg.K_DOWN]:
            axes.y_0 += axes.y_unit
            redraw(axes)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_PLUS:  # Zoom in
                    axes.x_unit = max(1, axes.x_unit * 2)
                    axes.y_unit = max(1, axes.y_unit * 2)
                    redraw(axes)
                elif event.key == pg.K_KP_MINUS:  # Zoom out
                    axes.x_unit = max(20, axes.x_unit * 0.5)
                    axes.y_unit = max(20, axes.y_unit * 0.5)
                    redraw(axes)
                    redraw(axes)
                if event.key == pg.K_KP_0:
                    reset(axes)
                if event.key == pg.K_KP_DIVIDE:
                    screen.fill(WHITE)
                    axes.draw_extra_grid()
                    axes.draw()
                    my_graphs = create_graph_objects(axes.zero, axes.units)
                    draw_graph_objects(my_graphs)
                    pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                x_pos, y_pos = pg.mouse.get_pos()
                axes.x_0, axes.y_0 = get_new_center_mouse(
                    x_pos, y_pos, axes.units)
                draw_all(axes)


if __name__ == '__main__':
    main()
