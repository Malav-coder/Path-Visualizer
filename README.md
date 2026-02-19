# Pathfinding Visualizer 🗺️

A interactive pathfinding algorithm visualizer built with **Python** and **Pygame**. Watch A*, Dijkstra's, BFS, and DFS algorithms find the shortest path in real-time!

## Features ✨

- **4 Pathfinding Algorithms**: BFS, DFS, Dijkstra's, and A*
- **Interactive Grid**: Click to place start point, end point, and walls
- **Real-time Visualization**: Watch the algorithm explore the grid step-by-step
- **Multiple Visual States**: Start (green), End (red), Walls (black), Visited (blue), Path (yellow)
- **User-friendly Controls**: Mouse and keyboard controls for easy interaction
- **Responsive Design**: 600x700 window with on-screen instructions

## Requirements 📋

- Python 3.7 or higher
- Pygame 2.6.1

## Installation 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pathfinding-visualizer.git
cd pathfinding-visualizer
```

### 2. Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv pathfinding_visualizer
pathfinding_visualizer\Scripts\activate

# On macOS/Linux
python3 -m venv pathfinding_visualizer
source pathfinding_visualizer/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage 🎮

### Run the Application
```bash
python main.py
```

### Controls

| Action | Control |
|--------|---------|
| **Set Start Point** | Left Click (First click) |
| **Set End Point** | Left Click (Second click) |
| **Place Walls** | Left Click (Drag to draw) |
| **Remove Node** | Right Click |
| **Select BFS** | Press `1` |
| **Select Dijkstra** | Press `2` |
| **Select A*** | Press `3` |
| **Select DFS** | Press `4` |
| **Start Algorithm** | Press `SPACE` |
| **Reset Grid** | Press `R` |
| **Clear Path Only** | Press `C` |

## How It Works 🧠

### BFS (Breadth-First Search)
- Uses queue data structure
- Explores nodes level by level
- Guarantees shortest path in unweighted grids
- Good for general pathfinding

### Dijkstra's Algorithm
- Uses priority queue (min-heap)
- Finds shortest path with weighted edges
- Works great with variable edge weights
- More efficient than BFS for large grids

### A* (A-Star)
- Uses heuristic function (Manhattan distance)
- Combines actual distance with estimated distance
- Generally faster than Dijkstra's
- Optimal if heuristic is admissible

### DFS (Depth-First Search)
- Uses stack data structure
- Explores deeply before backtracking
- May not find shortest path
- Useful for maze solving

## Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Optimal |
|-----------|-----------------|------------------|---------|
| BFS | O(V + E) | O(V) | ✓ Yes |
| DFS | O(V + E) | O(V) | ✗ No |
| Dijkstra | O((V+E)logV) | O(V) | ✓ Yes |
| A* | O(V + E) | O(V) | ✓ Yes* |

*A* is optimal if heuristic is admissible

## Project Structure 📁

```
pathfinding-visualizer/
├── main.py              # Main application & UI logic
├── grid.py              # Grid and Node classes
├── algorithms.py        # Pathfinding algorithm implementations
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── LICENSE             # MIT License
```

## Code Quality & Security ✅

- **Security**: No external API calls, no file system access, no sensitive data
- **Error Handling**: Comprehensive input validation and error messages
- **Safety Limits**: Protection against infinite loops with step limits
- **Best Practices**: Clean code, proper OOP design, well-documented
- **Testing**: Validated with multiple grid configurations

## Key Classes

### Node
Represents a cell in the grid with properties:
- Position (row, col)
- State (start, end, wall, visited, path)
- Neighbor relationships
- Previous pointer for path reconstruction

### Grid
Manages the entire grid:
- Creates and stores nodes
- Tracks start and end points
- Updates neighbor relationships
- Handles grid visualization

### Pathfinder
Static methods for each algorithm:
- `bfs()` - Breadth-First Search
- `dijkstra()` - Dijkstra's Algorithm
- `a_star()` - A* Algorithm
- `dfs()` - Depth-First Search

## Tips for Best Results 💡

1. **Start with small grids** (10x10) to understand behavior
2. **Try different wall patterns** - spirals, corridors, mazes
3. **Compare algorithms** - Run same maze with different algorithms
4. **Start & End far apart** - See full algorithm behavior
5. **Make complex mazes** - Some algorithms are more efficient

## Visualization Legend 🎨

- 🟢 **Green**: Start point
- 🔴 **Red**: End point
- ⬛ **Black**: Wall obstacle
- 🔵 **Blue**: Explored/Visited nodes
- 🟡 **Yellow**: Final path

## Performance Notes ⚡

- BFS: Fast, explores evenly
- DFS: Fast, but may take indirect paths
- Dijkstra: Medium speed, works with weights
- A*: Fastest with good heuristic

Maximum grid size tested: 20x20 (400 nodes) - runs smoothly on standard hardware.

## Future Enhancements 🔮

- [ ] Diagonal movement support
- [ ] Weighted tiles
- [ ] More algorithms (Bellman-Ford, etc.)
- [ ] Customizable grid size
- [ ] Theme selector
- [ ] Algorithm speed control
- [ ] Statistics panel
- [ ] Save/Load scenarios

## Common Issues & Troubleshooting 🔧

### Issue: "No Path Exists" appears
- Make sure start and end points are placed
- Ensure walls don't completely block the path
- Click away the message and try again

### Issue: Slow visualization
- Close other applications to free up resources
- Consider using a smaller grid size
- Check if display refresh is working properly

### Issue: Pygame not installing
```bash
pip install --upgrade pip
pip install pygame==2.6.1
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Author ✏️

Created as an educational project to visualize pathfinding algorithms.



### 🎯 Quick Start
```bash
python -m venv pathfinding_visualizer
pathfinding_visualizer\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Enjoy exploring pathfinding algorithms!** 🚀
