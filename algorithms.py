import pygame
import time
import sys
import heapq
from collections import deque


class Pathfinder:
    @staticmethod
    def reconstruct_path(end_node):
        """Reconstruct path from end node to start using previous pointers"""
        if end_node is None:
            return []

        path = []
        current = end_node

        while current is not None:
            path.append(current)
            current = current.previous

        path.reverse()  # Start to end

        # Exclude start and end nodes from path coloring
        if len(path) > 2:
            return path[1:-1]
        return []

    @staticmethod
    def bfs(grid, win, draw_func, delay=0.02):
        """
        Breadth-First Search Algorithm
        Returns: path if found, "NO_PATH" if no path exists
        """
        print("Starting BFS algorithm...")

        start = grid.start
        end = grid.end

        # Basic validation
        if start is None or end is None:
            print("Start or end node not set!")
            return "NO_PATH"

        if start == end:
            print("Start and end are the same!")
            return []

        # ✅ FIX 2: Clear visited flags before starting
        for row in grid.grid:
            for node in row:
                node.is_visited = False

        # Setup BFS
        queue = deque([start])
        visited = set([start])  # Still use set for fast lookup
        start.previous = None
        start.is_visited = True  # ✅ Mark start as visited

        step = 0
        max_steps = 10000  # Safety limit

        while queue:
            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current = queue.popleft()
            step += 1

            # Visualize current node
            if current != start and current != end:
                current.make_visited()

            # Check if we reached the end
            if current == end:
                print(f"✓ BFS found path in {step} steps!")
                return Pathfinder.reconstruct_path(current)

            # Explore neighbors
            for neighbor in current.neighbors:
                # ✅ FIX 2: Check both visited set AND node.is_visited flag
                if neighbor not in visited and not neighbor.is_visited:
                    visited.add(neighbor)
                    neighbor.is_visited = True  # ✅ Mark node as visited
                    neighbor.previous = current
                    queue.append(neighbor)

            # Update visualization
            draw_func()
            pygame.display.update()
            time.sleep(delay)

            # Safety check
            if step > max_steps:
                print("⚠️ BFS step limit reached")
                break

        print("✗ BFS: No path exists!")
        return "NO_PATH"

    @staticmethod
    def dijkstra(grid, win, draw_func, delay=0.02):
        """
        Dijkstra's Algorithm
        Returns: path if found, "NO_PATH" if no path exists
        """
        print("Starting Dijkstra's algorithm...")

        start = grid.start
        end = grid.end

        # Basic validation
        if start is None or end is None:
            print("Start or end node not set!")
            return "NO_PATH"

        if start == end:
            print("Start and end are the same!")
            return []

        # ✅ FIX 2: Clear visited flags before starting
        for row in grid.grid:
            for node in row:
                node.is_visited = False

        # Initialize distances
        distances = {}
        for row in grid.grid:
            for node in row:
                distances[node] = float('inf')
        distances[start] = 0

        # ✅ FIX 1: Add tiebreaker counter to prevent heapq comparison crash
        counter = 0
        pq = [(0, counter, start)]  # (distance, tiebreaker, node)
        counter += 1

        start.previous = None
        start.is_visited = True  # ✅ Mark start as visited

        visited_nodes = set()
        step = 0
        max_steps = 10000

        while pq:
            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ✅ FIX 1: Unpack with tiebreaker
            current_dist, _, current = heapq.heappop(pq)

            # Skip if already processed with shorter distance
            if current in visited_nodes:
                continue

            visited_nodes.add(current)
            current.is_visited = True  # ✅ Mark as visited
            step += 1

            # Visualize current node
            if current != start and current != end:
                current.make_visited()

            # Check if we reached the end
            if current == end:
                print(f"✓ Dijkstra found path in {step} steps!")
                return Pathfinder.reconstruct_path(current)

            # Explore neighbors
            for neighbor in current.neighbors:
                new_dist = current_dist + 1  # All edges weight = 1

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    neighbor.previous = current
                    heapq.heappush(pq, (new_dist, counter, neighbor))
                    counter += 1  # ✅ FIX 1: Increment counter for next node

            # Update visualization
            draw_func()
            pygame.display.update()
            time.sleep(delay)

            # Safety check
            if step > max_steps:
                print("⚠️ Dijkstra step limit reached")
                break

        print("✗ Dijkstra: No path exists!")
        return "NO_PATH"

    @staticmethod
    def a_star(grid, win, draw_func, delay=0.02):
        """
        A* Algorithm with Manhattan distance heuristic
        Returns: path if found, "NO_PATH" if no path exists
        """
        print("Starting A* algorithm...")

        start = grid.start
        end = grid.end

        # Basic validation
        if start is None or end is None:
            print("Start or end node not set!")
            return "NO_PATH"

        if start == end:
            print("Start and end are the same!")
            return []

        # ✅ FIX 2: Clear visited flags before starting
        for row in grid.grid:
            for node in row:
                node.is_visited = False

        # Heuristic function (Manhattan distance)
        def heuristic(node):
            return abs(node.row - end.row) + abs(node.col - end.col)

        # ✅ FIX 1: Add tiebreaker counter
        tiebreaker = 0

        # Initialize
        open_set = []
        heapq.heappush(open_set, (0, tiebreaker, start))
        tiebreaker += 1

        g_score = {node: float('inf') for row in grid.grid for node in row}
        g_score[start] = 0

        f_score = {node: float('inf') for row in grid.grid for node in row}
        f_score[start] = heuristic(start)

        start.previous = None
        start.is_visited = True  # ✅ Mark start as visited

        # Track which nodes are in open_set for faster lookup
        in_open_set = {start}

        visited_nodes = set()
        step = 0
        max_steps = 10000

        while open_set:
            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ✅ FIX 1: Unpack with tiebreaker
            _, _, current = heapq.heappop(open_set)
            in_open_set.remove(current)
            step += 1

            # Visualize current node
            if current != start and current != end:
                current.make_visited()
                current.is_visited = True  # ✅ Mark as visited

            # Check if we reached the end
            if current == end:
                print(f"✓ A* found path in {step} steps!")
                return Pathfinder.reconstruct_path(current)

            visited_nodes.add(current)
            current.is_visited = True  # ✅ Mark as visited

            # Explore neighbors
            for neighbor in current.neighbors:
                if neighbor in visited_nodes:
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    neighbor.previous = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor)

                    # Add to open set if not already there
                    if neighbor not in in_open_set:
                        heapq.heappush(
                            open_set, (f_score[neighbor], tiebreaker, neighbor))
                        tiebreaker += 1  # ✅ FIX 1: Increment counter
                        in_open_set.add(neighbor)

            # Update visualization
            draw_func()
            pygame.display.update()
            time.sleep(delay)

            # Safety check
            if step > max_steps:
                print("⚠️ A* step limit reached")
                break

        print("✗ A*: No path exists!")
        return "NO_PATH"

    @staticmethod
    def dfs(grid, win, draw_func, delay=0.03):
        """
        Depth-First Search Algorithm with backtracking visualization
        Returns: path if found, "NO_PATH" if no path exists
        """
        print("Starting DFS algorithm...")

        start = grid.start
        end = grid.end

        # Basic validation
        if start is None or end is None:
            print("Start or end node not set!")
            return "NO_PATH"

        if start == end:
            print("Start and end are the same!")
            return []

        # ✅ FIX 2: Clear visited flags before starting
        for row in grid.grid:
            for node in row:
                node.is_visited = False

        # Setup DFS
        stack = [start]
        visited = set([start])
        start.previous = None
        start.is_visited = True  # ✅ Mark start as visited

        step = 0
        max_steps = 10000
        backtracking = False

        while stack:
            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current = stack.pop()
            step += 1

            # Visualize current node (different color for backtracking)
            if current != start and current != end:
                if backtracking:
                    current.color = (200, 100, 200)  # Purple for backtracking
                    backtracking = False
                else:
                    current.make_visited()
                    current.is_visited = True  # ✅ Mark as visited

            # Check if we reached the end
            if current == end:
                print(f"✓ DFS found path in {step} steps!")
                return Pathfinder.reconstruct_path(current)

            # Track if we have unvisited neighbors
            has_unvisited_neighbors = False

            # Explore neighbors (in reverse order for better visualization)
            for neighbor in reversed(current.neighbors):
                # ✅ FIX 2: Check both visited set AND node.is_visited flag
                if neighbor not in visited and not neighbor.is_visited:
                    visited.add(neighbor)
                    neighbor.is_visited = True  # ✅ Mark node as visited
                    neighbor.previous = current
                    stack.append(neighbor)
                    has_unvisited_neighbors = True

            # If no unvisited neighbors, mark for backtracking
            if not has_unvisited_neighbors and current != start:
                backtracking = True
                # Show backtracking longer
                draw_func()
                pygame.display.update()
                time.sleep(delay * 2)

            # Update visualization
            draw_func()
            pygame.display.update()
            time.sleep(delay)

            # Safety check
            if step > max_steps:
                print("⚠️ DFS step limit reached")
                break

        print("✗ DFS: No path exists!")
        return "NO_PATH"
