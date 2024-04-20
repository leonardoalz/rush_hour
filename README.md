## Rush Hour

This Python program provides functionality to solve the Rush Hour puzzle game. The Rush Hour puzzle involves moving vehicles within a grid to clear a path for a specific vehicle to exit the grid. Each vehicle has a specific size and orientation, and they can only move in the direction they are oriented.

### Usage

To use the program, follow these steps:

1. Run the program by executing the `rush_hour.py` file.
2. Choose an option:
   - **Play game**: Play the Rush Hour game interactively.
   - **Test game algorithms**: Test different search algorithms to solve the puzzle.
3. If you choose to play the game:
   - Select the difficulty level (easy, medium, hard).
   - Choose a version of the selected difficulty (1, 2, 3).
   - Follow the instructions to input moves and navigate the vehicles to solve the puzzle.
4. If you choose to test game algorithms:
   - Select the difficulty level (easy, medium, hard).
   - Choose a version of the selected difficulty (1, 2, 3).
   - Choose an algorithm to test:
     - Breadth-first search (BFS)
     - Depth-first search (DFS)
     - Depth-limited search (DLS)
     - Greedy search
     - A* search
   - Based on the chosen algorithm, you may need to provide additional inputs such as the maximum depth for DLS or the heuristic function for Greedy and A* search.
   - The program will execute the chosen algorithm to solve the puzzle and display the results, including the number of nodes generated and the time taken for execution.

### Classes and Functions

The program consists of the following classes and functions:

- **Car**: Represents a vehicle in the Rush Hour game. Each car has attributes such as name, size, coordinates, orientation, and whether it is the red car.
- **Board**: Represents the game board and provides methods to check for the goal state, generate next possible moves, and more.
- **TreeNode**: Represents a node in the search tree used by search algorithms.
- **Search Algorithms**: Includes implementations of various search algorithms such as BFS, DFS, DLS, Greedy search, and A* search.
- **Heuristic Functions**: Includes heuristic functions used for Greedy search and A* search.

### Dependencies

The program requires the following dependencies:

- `copy`: Used for deep copying objects.
- `collections`: Used for deque data structure.
- `time`: Used for measuring execution time.
- `resource`: Used for measuring memory usage (not available by default on Windows).

### Running the Program

To run the program, ensure you have Python installed on your system. Then, execute the `rush_hour.py` file using a Python interpreter.

```bash
python rush_hour.py
```

### Credits

This program was created by [insert your name] and is provided under [insert license].
