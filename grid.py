import pygame


class Node:
    def __init__(self, row, col, size) -> None:
        self.row = row
        self.col = col
        self.size = size

        self.x = col * size
        self.y = row * size

        self.color = (255, 255, 255)  # white
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False  # ✅ Used by algorithms to track visited state
        self.is_path = False
        self.neighbors = []
        self.previous = None  # For path reconstruction

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.size, self.size))

    def make_wall(self):
        self.color = (0, 0, 0)  # black
        self.is_wall = True
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.previous = None
        self.neighbors = []  # Walls have no valid neighbors

    def make_start(self):
        self.color = (0, 255, 0)  # green
        self.is_start = True
        self.is_wall = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.previous = None

    def make_end(self):
        self.color = (255, 0, 0)  # red
        self.is_end = True
        self.is_wall = False
        self.is_start = False
        self.is_visited = False
        self.is_path = False
        self.previous = None

    def make_visited(self):
        if not self.is_start and not self.is_end and not self.is_wall:
            self.color = (0, 120, 255)  # blue
            self.is_visited = True  # ✅ Set visited flag when coloring

    def make_path(self):
        if not self.is_start and not self.is_end:
            self.color = (255, 255, 0)  # yellow
            self.is_path = True
            self.is_visited = False

    def reset(self):
        self.color = (255, 255, 255)  # white
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False  # ✅ Reset visited flag
        self.is_path = False
        self.neighbors = []
        self.previous = None

    def update_neighbors(self, grid):
        self.neighbors = []
        rows = len(grid)
        cols = len(grid[0])

        # Check all 4 directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_wall:
                    self.neighbors.append(neighbor)


class Grid:
    def __init__(self, rows, cols, width) -> None:
        self.rows = rows
        self.cols = cols
        self.width = width
        self.cell_size = width // rows

        self.grid = []
        self.start = None
        self.end = None

        self.create_grid()

    def create_grid(self):
        self.grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                node = Node(r, c, self.cell_size)
                row.append(node)
            self.grid.append(row)

    def set_start(self, node):
        if self.start:
            self.start.reset()
        self.start = node
        node.make_start()
        self.update_all_neighbors()

    def set_end(self, node):
        if self.end:
            self.end.reset()
        self.end = node
        node.make_end()
        self.update_all_neighbors()

    def draw(self, win):
        for row in self.grid:
            for node in row:
                node.draw(win)

        self.draw_grid_lines(win)

    def draw_grid_lines(self, win):
        color = (220, 220, 220)

        # Horizontal lines
        for i in range(self.rows + 1):
            pygame.draw.line(
                win, color,
                (0, i * self.cell_size),
                (self.width, i * self.cell_size),
                1
            )

        # Vertical lines
        for j in range(self.cols + 1):
            pygame.draw.line(
                win, color,
                (j * self.cell_size, 0),
                (j * self.cell_size, self.width),
                1
            )

    def get_node_from_pos(self, pos):
        x, y = pos

        # Check if click is within grid bounds
        if x < 0 or x >= self.width or y < 0 or y >= self.width:
            return None

        row = y // self.cell_size
        col = x // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]

        return None

    def reset_grid(self):
        self.start = None
        self.end = None
        self.create_grid()

    def clear_path(self):
        for row in self.grid:
            for node in row:
                # ✅ Reset visited flags and path flags but keep walls, start, end
                if node.is_visited or node.is_path:
                    node.reset()
                elif node.is_start:
                    node.make_start()
                elif node.is_end:
                    node.make_end()
                # Walls remain as walls

        self.update_all_neighbors()

    def update_all_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def color_path(self, path):
        if path:
            for node in path:
                node.make_path()
