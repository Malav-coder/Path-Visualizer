import pygame
import sys
from grid import Grid
from algorithms import Pathfinder

print("Pathfinding Visualizer - All Algorithms successfully integrated!")

pygame.init()

WIDTH, HEIGHT = 600, 700
ROWS, COLS = 20, 20

Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (100, 200, 255)  # For frontier nodes

FONT = pygame.font.SysFont('arial', 20)
TITLE_FONT = pygame.font.SysFont('arial', 24, bold=True)

# Algorithm constants
ALGO_DIJKSTRA = "Dijkstra"
ALGO_ASTAR = "A*"
ALGO_BFS = "BFS"
ALGO_DFS = "DFS"

ALGORITHMS = {
    pygame.K_1: ALGO_BFS,
    pygame.K_2: ALGO_DIJKSTRA,
    pygame.K_3: ALGO_ASTAR,
    pygame.K_4: ALGO_DFS
}


def draw_info_panel(win, current_algo, algorithm_running):
    """Draw information panel at the bottom"""
    panel_height = 120
    pygame.draw.rect(win, DARK_GREY, (0, HEIGHT -
                     panel_height, WIDTH, panel_height))

    # Title
    title = TITLE_FONT.render("Pathfinding Visualizer", True, ORANGE)
    win.blit(title, (WIDTH // 2 - title.get_width() //
             2, HEIGHT - panel_height + 10))

    # Status
    status_color = YELLOW if algorithm_running else GREEN
    status_text = f"RUNNING: {current_algo}" if algorithm_running else "READY"
    status = FONT.render(f"Status: {status_text}", True, status_color)
    win.blit(status, (10, HEIGHT - panel_height + 40))

    # Instructions
    instructions = [
        "Left Click: Place Start → End → Walls",
        "Right Click: Remove Node",
        "1-4: Select Algorithm (1:BFS, 2:Dijkstra, 3:A*, 4:DFS)",
        "Space: Start Algorithm | R: Reset Grid | C: Clear Path"
    ]

    for i, text in enumerate(instructions):
        text_surface = FONT.render(text, True, WHITE)
        win.blit(text_surface, (10, HEIGHT - panel_height + 60 + i * 20))

    # Legend
    legend_items = [
        (GREEN, "Start"),
        (RED, "End"),
        (BLACK, "Wall"),
        (BLUE, "Visited"),
        (YELLOW, "Path")
    ]

    for i, (color, label) in enumerate(legend_items):
        pygame.draw.rect(win, color, (WIDTH - 200, HEIGHT -
                         panel_height + 65 + i * 25, 20, 20))
        label_surface = FONT.render(label, True, WHITE)
        win.blit(label_surface, (WIDTH - 175,
                 HEIGHT - panel_height + 65 + i * 25))


def draw(win, grid, algorithm_name, algorithm_running=False):
    win.fill(WHITE)
    grid.draw(win)
    draw_info_panel(win, algorithm_name, algorithm_running)

    # Algorithm status text at top
    if algorithm_running:
        # Red when running
        text = FONT.render(f"Running: {algorithm_name}", True, (255, 0, 0))
    elif algorithm_name:
        # Black when selected
        text = FONT.render(f"Selected: {algorithm_name}", True, (0, 0, 0))
        win.blit(text, (10, 10))

    pygame.display.update()


def show_no_path_message(grid):
    """Show 'No Path Exists' message on grid"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((grid.width, grid.width), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    Window.blit(overlay, (0, 0))

    # Display message
    font = pygame.font.SysFont('arial', 36, bold=True)
    message = font.render("NO PATH EXISTS!", True, (255, 50, 50))
    Window.blit(message, (grid.width//2 - message.get_width()//2,
                          grid.width//2 - message.get_height()//2 - 30))

    font2 = pygame.font.SysFont('arial', 24)
    message2 = font2.render(
        "Press any key to continue...", True, (255, 255, 255))
    Window.blit(message2, (grid.width//2 - message2.get_width()//2,
                           grid.width//2 + 20))

    pygame.display.update()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def validate_grid_setup(grid):
    """Validate that grid is properly set up before running algorithm"""
    if grid.start is None:
        print("Error: Please set a START point (green)")
        return False

    if grid.end is None:
        print("Error: Please set an END point (red)")
        return False

    if grid.start == grid.end:
        print("Error: Start and End cannot be the same")
        return False

    return True


def main():
    grid_width = min(WIDTH, HEIGHT - 120)
    grid = Grid(ROWS, COLS, grid_width)

    # State variables
    algorithm_running = False
    current_algorithm = ALGO_BFS  # Default algorithm
    mouse_down = False
    mouse_button = None
    last_node_pos = None

    run = True
    while run:
        clock.tick(60)
        draw(Window, grid, current_algorithm, algorithm_running)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                mouse_button = event.button
                last_node_pos = None

                if event.button in (1, 3):  # Left or Right click
                    pos = pygame.mouse.get_pos()
                    if pos[1] < grid_width:  # Only interact with grid area
                        node = grid.get_node_from_pos(pos)

                        if node is None:
                            continue

                        handle_mouse_click(node, mouse_button, grid)
                        last_node_pos = (node.row, node.col)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                mouse_button = None
                last_node_pos = None

            elif event.type == pygame.MOUSEMOTION and mouse_down and mouse_button == 1:
                pos = pygame.mouse.get_pos()
                if pos[1] < grid_width:
                    node = grid.get_node_from_pos(pos)

                    if node is None or last_node_pos == (node.row, node.col):
                        continue

                    if grid.start and grid.end:
                        handle_mouse_drag(node, grid)
                        last_node_pos = (node.row, node.col)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset grid
                    grid.reset_grid()
                    algorithm_running = False
                    current_algorithm = ALGO_BFS
                    print("Grid reset")

                elif event.key == pygame.K_c:  # Clear path only
                    if not algorithm_running:
                        grid.clear_path()
                        algorithm_running = False
                        print("Cleared path")

                elif event.key == pygame.K_SPACE and not algorithm_running:
                    # Validate grid setup before running algorithm
                    if not validate_grid_setup(grid):
                        continue

                    # Start algorithm
                    algorithm_running = True
                    draw(Window, grid, current_algorithm, algorithm_running)

                    # Run selected algorithm
                    path = run_algorithm(grid, current_algorithm)

                    # Handle results
                    if path == "NO_PATH":
                        show_no_path_message(grid)
                    elif path:
                        # Color the path
                        for node in path:
                            if node != grid.start and node != grid.end:
                                node.make_path()
                        print(f"✓ Path found with {len(path)} steps")

                    algorithm_running = False
                    draw(Window, grid, current_algorithm, algorithm_running)

                # Algorithm selection
                elif event.key in ALGORITHMS and not algorithm_running:
                    current_algorithm = ALGORITHMS[event.key]
                    print(f"Selected algorithm: {current_algorithm}")

    pygame.quit()


def handle_mouse_click(node, button, grid):
    """Handle single mouse click"""
    if button == 1:  # Left click
        if not grid.start:
            grid.set_start(node)
            print(f"Start set at: ({node.row}, {node.col})")
        elif not grid.end and node != grid.start:
            grid.set_end(node)
            print(f"End set at: ({node.row}, {node.col})")
        elif node != grid.start and node != grid.end:
            if not (node.is_start or node.is_end or node.is_visited or node.is_path):
                node.make_wall()
                grid.update_all_neighbors()

    elif button == 3:  # Right click - remove node
        if node == grid.start:
            grid.start = None
            print("Start removed")
        elif node == grid.end:
            grid.end = None
            print("End removed")

        node.reset()
        grid.update_all_neighbors()


def handle_mouse_drag(node, grid):
    """Handle mouse drag for wall placement"""
    if node != grid.start and node != grid.end:
        if not (node.is_start or node.is_end or node.is_visited or node.is_path):
            if not node.is_wall:
                node.make_wall()
                grid.update_all_neighbors()


def run_algorithm(grid, algorithm_name):
    """Run the selected pathfinding algorithm"""
    print(f"Running {algorithm_name}...")

    # Update neighbors before running algorithm
    grid.update_all_neighbors()

    # Clear any previous path/visited nodes
    grid.clear_path()

    # Run the selected algorithm
    if algorithm_name == ALGO_BFS:
        return Pathfinder.bfs(grid, Window,
                              lambda: draw(Window, grid, algorithm_name, True))

    elif algorithm_name == ALGO_DIJKSTRA:
        return Pathfinder.dijkstra(grid, Window,
                                   lambda: draw(Window, grid, algorithm_name, True))

    elif algorithm_name == ALGO_ASTAR:
        return Pathfinder.a_star(grid, Window,
                                 lambda: draw(Window, grid, algorithm_name, True))

    elif algorithm_name == ALGO_DFS:
        return Pathfinder.dfs(grid, Window,
                              lambda: draw(Window, grid, algorithm_name, True))

    return None


if __name__ == "__main__":
    main()
