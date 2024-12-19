import math

import numpy as np
import pygame as pg

from constants import *


class CoordinateSystem:

    def __init__(self, x_0=WIDTH // 2, y_0=HEIGHT // 2, x_unit=40, y_unit=40):
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
        if self.x_unit < 40:
            self.x_unit = 20
        return [round(0 + k * self.x_unit, 1) for k in range(0, self.n_x + 1)]

    @property
    def y_axis_values(self):
        if self.y_unit < 40:
            self.y_unit = 20
        return [round(0 + k * self.y_unit, 1) for k in range(0, self.n_y + 1)]

    @property
    def dx_axis_values(self):
        return [round(0 + k * self.dx_unit, 1) for k in range(0, self.n_dx + 1)]

    @property
    def dy_axis_values(self):
        return [round(0 + k * self.dy_unit, 1) for k in range(0, self.n_dy + 1)]

    def draw_x_notch(self, x):
        size = self.notch_size(x, self.x_unit)
        pg.draw.line(screen, BLACK, (x, self.y_0 - size),
                     (x, self.y_0 + size), 1)

    def draw_y_notch(self, y):
        size = self.notch_size(y, self.y_unit)
        pg.draw.line(screen, BLACK, (self.x_0 - size, y),
                     (self.x_0 + size, y), 1)

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

    def draw_x_labels(self):
        """Draw labels for x-axis, excluding zero."""
        label_step = max(1, round(40 / self.x_unit))
        font = pg.font.Font(None, 24)
        for x in range(-self.n_x, self.n_x + 1):
            if x % label_step == 0 and x != 0:  # Skip zero
                pixel_x = self.x_0 + x * self.x_unit
                label = font.render(str(x), True, BLACK)
                screen.blit(
                    label, (pixel_x - label.get_width() // 2, self.y_0 + 10))

    def draw_y_labels(self):
        """Draw labels for y-axis, excluding zero."""
        label_step = max(1, round(40 / self.y_unit))
        font = pg.font.Font(None, 24)
        for y in range(-self.n_y, self.n_y + 1):
            if y % label_step == 0 and y != 0:  # Skip zero
                pixel_y = self.y_0 - y * self.y_unit
                label = font.render(str(y), True, BLACK)
                screen.blit(
                    label, (self.x_0 - 30, pixel_y - label.get_height() // 2))

    def draw_centered_zero(self):
        """Draw the zero in the specified centered cell."""
        font = pg.font.Font(None, 24)
        label = font.render("0", True, BLACK)
        pixel_x = self.x_0 - self.x_unit  # (-1) * x_unit
        pixel_y = self.y_0 + self.y_unit  # (-1) * y_unit
        screen.blit(label, (pixel_x + self.x_unit // 2 - label.get_width() // 2,
                            pixel_y - self.y_unit // 2 - label.get_height() // 2))

    def draw_labels(self):
        """Draw all axis labels."""
        self.draw_x_labels()
        self.draw_y_labels()
        self.draw_centered_zero()

    def draw(self):
        """Redraw the grid, notches, and labels."""
        self.draw_grid()
        pg.draw.line(screen, BLACK, (0, self.y_0), (WIDTH, self.y_0), 1)
        pg.draw.line(screen, BLACK, (self.x_0, 0), (self.x_0, HEIGHT), 1)
        self.draw_notches()
        self.draw_labels()


class Graph:

    def __init__(self, zero, units, functn, color, borders):
        self.A = borders[0]
        self.B = borders[1]

        n = int((self.B - self.A) // dx)

        original_x_values = [round(self.A + k * dx, 1)
                             for k in range(0, n + 2)]

        self.x_0 = zero[0]
        self.y_0 = zero[1]

        self.x_unit = units[0]
        self.y_unit = units[1]

        self.functn = functn
        self.color = color

        self.x_values = [x * self.x_unit + self.x_0 for x in original_x_values]
        self.y_values = [
            self.y_0 - (eval(self.functn)) * self.y_unit for x in original_x_values]

    def draw(self):
        for i in range(1, len(self.x_values)):
            pg.draw.line(screen, self.color, (self.x_values[i - 1], self.y_values[i - 1]),
                         (self.x_values[i], self.y_values[i]), 1)


class ParametricGraph(Graph):
    def __init__(self, zero, units, x_func, y_func, color, t_range, dt):
        """
        ParametricGraph calculates and stores coordinates for parametric equations.
        :param zero: (x_0, y_0) center of the coordinate system.
        :param units: (x_unit, y_unit) pixel-to-unit ratios for x and y.
        :param x_func: String defining x(t), e.g., "5 * math.cos(t)".
        :param y_func: String defining y(t), e.g., "3 * math.sin(t)".
        :param color: RGB tuple or predefined color name.
        :param t_range: (t0, tN) range for the parameter t.
        :param dt: Step size for t.
        """
        self.x_func = x_func
        self.y_func = y_func
        self.color = color
        self.t0, self.tN = t_range
        self.dt = dt
        self.x_0, self.y_0 = zero
        self.x_unit, self.y_unit = units

        self.x_values = []
        self.y_values = []

        self.calculate_coordinates()

    def calculate_coordinates(self):
        """Calculate x and y coordinates, ensuring the last point is included."""
        # Generate t_values with precise stepping
        t_values = np.linspace(self.t0, self.tN, int(
            (self.tN - self.t0) / self.dt) + 1)

        # Calculate x and y using list comprehensions
        self.x_values = [eval(self.x_func) * self.x_unit +
                         self.x_0 for t in t_values]
        self.y_values = [self.y_0 -
                         eval(self.y_func) * self.y_unit for t in t_values]

    def draw(self):
        """Draw the parametric graph."""
        for i in range(1, len(self.x_values)):
            pg.draw.line(screen, self.color,
                         (self.x_values[i - 1], self.y_values[i - 1]),
                         (self.x_values[i], self.y_values[i]), 1)
