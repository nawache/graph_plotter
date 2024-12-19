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
    for graph_object in graph_objects:
        graph_object.draw()


def get_new_center(zero: Tuple[int, int],
                   units: Tuple[int, int],
                   mouse_click: bool = False) -> Tuple[int, int]:
    """
    Calculate a new center position based on units,
    and optionally on mouse click.

    :param zero: Tuple containing the x and y coordinates of the origin.
    :param units: Tuple containing the pixel-to-unit ratios for the
                  x and y axes.
    :param mouse_click: Boolean flag to determine whether to calculate
                        based on mouse click (default is False).
    :return: The new center position as a tuple.
    """
    x_unit, y_unit = units
    x_pos, y_pos = zero

    if mouse_click:
        # For mouse click, adjust the center to align with the grid
        # based on the mouse position
        new_x_pos = x_pos - (x_pos % x_unit)
        new_y_pos = y_pos - (y_pos % y_unit) + y_unit
    else:
        # For normal update, adjust to the nearest grid multiple
        new_x_pos = x_pos - (x_pos % x_unit)
        new_y_pos = y_pos - (y_pos % y_unit)

    return new_x_pos, new_y_pos


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


def draw_extra_grid(axes: CoordinateSystem) -> None:
    """
    Function to draw the extra grid.

    :param axes: The CoordinateSystem object representing the current grid.
    """
    screen.fill(WHITE)
    axes.draw_extra_grid()
    axes.draw()
    my_graphs = create_graph_objects(axes.zero, axes.units)
    draw_graph_objects(my_graphs)
    pg.display.update()


def handle_movement(keys, axes: CoordinateSystem) -> None:
    """
    Handle key press events for zooming and panning.

    :param keys: Result of pg.key.get_pressed()
    :param axes: The CoordinateSystem object representing the current
                 grid and axes.
    """
    if keys[pg.K_LEFT]:
        axes.x_0 += axes.x_unit
        redraw(axes)
    if keys[pg.K_DOWN]:
        axes.y_0 -= axes.y_unit
        redraw(axes)
    if keys[pg.K_RIGHT]:
        axes.x_0 -= axes.x_unit
        redraw(axes)
    if keys[pg.K_UP]:
        axes.y_0 += axes.y_unit
        redraw(axes)


def handle_key_events(events: List[pg.event.Event],
                      axes: CoordinateSystem) -> None:
    """
    Handle key press events for zooming, panning,
    reseting and drawing extra grid.

    :param events: A list of events to process.
    :param axes: The CoordinateSystem object representing the current
                 grid and axes.
    """
    for event in events:
        if event.type == pg.KEYDOWN:

            # Zooming
            if event.key == pg.K_KP_PLUS:  # Zoom in
                axes.x_unit *= 2
                axes.y_unit *= 2
                redraw(axes)
            elif event.key == pg.K_KP_MINUS:  # Zoom out
                axes.x_unit = max(20, axes.x_unit * 0.5)
                axes.y_unit = max(20, axes.y_unit * 0.5)
                redraw(axes)

            # Reset
            if event.key == pg.K_KP_0:
                reset(axes)

            # Draw extra grid
            if event.key == pg.K_KP_DIVIDE:
                draw_extra_grid(axes)


def handle_mouse_events(events: List[pg.event.Event],
                        axes: CoordinateSystem) -> None:
    """
    Handle mouse button events (move origin on click).

    :param events: A list of events to process.
    :param axes: The CoordinateSystem object representing the current
                 grid and axes.
    """
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            x_pos, y_pos = pg.mouse.get_pos()
            axes.x_0, axes.y_0 = get_new_center((x_pos, y_pos),
                                                axes.units,
                                                mouse_click=True)


def handle_other_events(events: List[pg.event.Event],
                        axes: CoordinateSystem) -> None:
    """
    Handle other events like quitting, etc.

    :param events: A list of events to process.
    :param axes: The CoordinateSystem object representing the current
                 grid and axes.
    """
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


def main() -> None:
    """
    Main loop for the program, handling events and user input.
    """
    pg.display.set_caption("My Graph")
    axes = CoordinateSystem()
    reset(axes)

    running = True
    while running:
        clock.tick(10)
        # Get all keys and events once per frame
        keys = pg.key.get_pressed()
        events = pg.event.get()

        # Handle all events: key, mouse, and other
        handle_movement(keys, axes)
        handle_key_events(events, axes)
        handle_mouse_events(events, axes)
        handle_other_events(events, axes)


if __name__ == '__main__':
    main()
