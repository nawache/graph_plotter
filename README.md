# Parametric Graph Plotter

A Python-based **graph plotting application** built using **Pygame** that supports **parametric equations** and **standard Cartesian functions**. This tool provides a dynamic and interactive way to visualize graphs defined by mathematical expressions.

---

## Features

1. **Parametric Graphs**:
   - Define `x(t)` and `y(t)` with respect to a parameter `t`.
   - Example: `x = 5 * cos(t), y = 3 * sin(t)`.

2. **Standard Cartesian Graphs**:
   - Plot `y = f(x)` with defined ranges for `x`.

3. **Customizable Appearance**:
   - Define graph colors, ranges, and step sizes.

---

## Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python 3.8+**
- **Pygame**:
  ```bash
  pip install pygame
  ```
- **Numpy**:
  ```bash
  pip install numpy
  ```

---

### File Structure

```
project/
├── classes.py          # Core classes for CoordinateSystem and Graphs
├── constants.py        # Constants for screen dimensions, colors, etc.
├── graph_constructor.py # Main application logic
├── graphs.csv          # CSV file defining graphs
├── README.md           # Project documentation
├── requirements.txt    # Dependencies for the project
```

---

### Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Define Graphs**:
   Edit `graphs.csv` to define the graphs you want to plot. Example:
   ```csv
   # Parametric: x(t); y(t); color; t_range; dt
   5 * math.cos(t); 3 * math.sin(t); RED; (0, 2 * math.pi); 0.1

   # Cartesian: f(x); color; range
   x**2; GREEN; (-10, 10)
   ```

4. **Run the Application**:
   ```bash
   python graph_constructor.py
   ```

---

### Controls

- **Arrow Keys**: Pan the view in the respective direction.
- **`NUM+` / `NUM-`**: Zoom in or out.
- **`NUM0`**: Reset the view to the default state.
- **Mouse**:
  - **Left Click**: Recenter the coordinate system.

---

### Examples


#### Parametric Graph: Ellipse
```csv
5 * math.cos(t); 3 * math.sin(t); RED; (0, 2 * math.pi); 0.1
```

#### Cartesian Graph: Parabola
```csv
x**2; YELLOW; (-10, 10)
```

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, please submit a pull request or open an issue.

---

## License

This project is licensed under the **MIT License**.
