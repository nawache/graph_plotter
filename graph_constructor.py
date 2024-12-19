import csv
import math
import sys
from ast import literal_eval
from typing import List, Tuple, Union

import pygame as pg

from classes import CoordinateSystem, Graph, ParametricGraph
from constants import WIDTH, HEIGHT, WHITE, clock, screen

pg.init()


def get_input() -> List[Union[Tuple[str, str, str, str, float],
                              Tuple[str, str, str]]]:
    """
    Reads graphs from the CSV file, supporting both standard and
    parametric graphs.

    :return: A list of tuples containing graph definitions. Each tuple includes
             the graph type and its parameters. For parametric graphs,
             the tuple includes ("parametric", x_func, y_func, color,
                                 t_range, dt).
             For standard graphs, it includes ("standard", functn,
                                               color, borders).
    """
    try:
        with open("graphs.csv", mode="r") as file:
            reader = csv.reader(file, delimiter=";")
            graphs = []
            for row in reader:
                if row[0].startswith("#"):  # Skip comments
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


def create_graph_objects(
        zero: Tuple[int, int],
        units: Tuple[int, int]
) -> List[Union[Graph, ParametricGraph]]:
    """
    Create graph objects from input data.

    :param zero: Tuple containing the x and y coordinates of the origin.
    :param units: Tuple containing the pixel-to-unit ratios
                  for the x and y axes.
    :return: A list of Graph and ParametricGraph objects.
    """
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


def draw_graph_objects(
    graph_objects: List[Union[Graph, ParametricGraph]]
) -> None:
    """
    Draw the graph objects on the screen.

    :param graph_objects: A list of Graph and ParametricGraph objects to draw.
    """
    [graph_object.draw() for graph_object in graph_objects]


def get_new_center(zero: Tuple[int, int],
                   units: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculate a new center position based on units.

    :param zero: Tuple containing the x and y coordinates of the origin.
    :param units: Tuple containing the pixel-to-unit
                  ratios for the x and y axes.
    :return: The new center position as a tuple.
    """
    x_unit, y_unit = units
    x_pos, y_pos = zero
    new_x_pos_1 = x_pos - (x_pos % x_unit)
    new_y_pos_1 = y_pos - (y_pos % y_unit)
    return new_x_pos_1, new_y_pos_1


def get_new_center_mouse(x_pos: int,
                         y_pos: int,
                         units: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculate a new center position based on a mouse click.

    :param x_pos: The x-coordinate of the mouse click.
    :param y_pos: The y-coordinate of the mouse click.
    :param units: Tuple containing the pixel-to-unit
                  ratios for the x and y axes.
    :return: The new center position as a tuple.
    """
    x_unit, y_unit = units
    new_x_pos_1 = x_pos - (x_pos % x_unit)
    new_y_pos_1 = y_pos - (y_pos % y_unit) + y_unit
    return new_x_pos_1, new_y_pos_1


def draw_all(axes: CoordinateSystem) -> None:
    """
    Redraw all elements on the screen.

    :param axes: The CoordinateSystem object
                 representing the current grid and axes.
    """
    my_graphs = create_graph_objects(axes.zero, axes.units)
    screen.fill(WHITE)
    axes.draw()
    draw_graph_objects(my_graphs)
    pg.display.update()


def redraw(axes: CoordinateSystem) -> None:
    """
    Recalculate and redraw the axes and graphs.

    :param axes: The CoordinateSystem object
                 representing the current grid and axes.
    """
    axes.x_0, axes.y_0 = get_new_center(axes.zero, axes.units)
    draw_all(axes)


def reset(axes: CoordinateSystem) -> None:
    """
    Reset the axes to their default state.

    :param axes: The CoordinateSystem object
                 representing the current grid and axes.
    """
    axes.x_unit = 40
    axes.y_unit = 40
    axes.x_0 = WIDTH // 2
    axes.y_0 = HEIGHT // 2
    draw_all(axes)


def main() -> None:
    """
    Main loop for the program, handling events and user input.
    """
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
                    axes.x_unit *= 2
                    axes.y_unit *= 2
                    redraw(axes)
                elif event.key == pg.K_KP_MINUS:  # Zoom out
                    axes.x_unit = max(20, axes.x_unit * 0.5)
                    axes.y_unit = max(20, axes.y_unit * 0.5)
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
