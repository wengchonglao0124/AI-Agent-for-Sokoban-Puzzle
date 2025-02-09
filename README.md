# AI Agent for Sokoban Puzzle

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Complete-brightgreen)

---

## Introduction

Sokoban is a classic puzzle game where a worker pushes boxes to designated target locations within a warehouse. It is a challenging task due to its large state-space complexity and the potential for deadlocks caused by irreversible moves. This project introduces an **AI Agent** designed to solve Sokoban puzzles using **A\*** and **BFS** algorithms, optimized with heuristics and search space reduction techniques.

The solver treats Sokoban as a state-space search problem and efficiently finds solutions for various puzzles by implementing:
- **A\* Search**: Uses a heuristic-driven approach for optimal pathfinding.
- **Breadth-First Search (BFS)**: Explores all states to ensure solutions, albeit less efficiently.
- **Macro Actions**: Groups multiple actions to minimize search depth and improve efficiency.

---

## Features

- **Heuristic Optimization**: Leverages Manhattan distance and weighting to improve A\* performance.
- **Taboo Cell Detection**: Identifies deadlocks to avoid exploring invalid states.
- **Macro and Elementary Actions**: Reduces complexity while maintaining solution optimality.
- **Performance Analysis**: Benchmarked on over 200 warehouse environments.

---

## Installation and Setup

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/AI-Agent-for-Sokoban-Puzzle.git
   cd AI-Agent-for-Sokoban-Puzzle
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Use a virtual environment to isolate dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

---

## Usage

To run the Sokoban solver and its tests, execute the `testing.py` file, which contains various testing scenarios. Ensure you have the required files and dependencies in place.

### Example Usage

1. **Run all tests and demonstrations:**
   ```bash
   python testing.py
   ```

   This will:
   - Print the team information.
   - Test the taboo cells calculation.
   - Test the action sequence validation.
   - Solve Sokoban puzzles using elementary actions and macro actions.
   - Evaluate the `can_go_there` function for pathfinding.
   - Test multiple warehouses using different configurations.

2. **Run specific test cases:**
   Modify the `testing.py` script under the `if __name__ == '__main__':` block to focus on individual test functions like:
   ```python
   test_taboo_cells()
   test_check_elem_action_seq()
   test_solve_sokoban_elem()
   test_can_go_there()
   test_solve_sokoban_macro()
   ```

3. **Custom Warehouse Testing:**
   Use the `testAll()` function to test a specific warehouse or a batch:
   ```python
   testAll(5)  # Tests warehouse 5 with elementary actions
   testAll(5, macro=True)  # Tests warehouse 5 with macro actions
   ```

   To test all warehouses:
   ```python
   testAll()  # All warehouses with elementary actions
   testAll(macro=True)  # All warehouses with macro actions
   ```

4. **Custom Box Limits and Timeout:**
   Adjust the parameters in `testAll()` to experiment with custom configurations:
   ```python
   testAll(limit_of_boxes=100, timeout=300, macro=True)
   ```

### Output

- Results will display directly in the console, including the status of each test, time taken, and whether the solver passed or failed the test.

---

## Results

### Performance Summary

| Solver Type   | Solved Percentage | Average Solve Time |
|---------------|-------------------|--------------------|
| A\* (Macro)   | **68%**           | **6.4s**           |
| A\* (Elem)    | **49.5%**           | **16.5s**           |
| BFS (Macro)   | 65%               | 8.2s               |
| BFS (Elem)    | 43.7%               | 12.9s               |

### Insights
- **A\*** outperforms BFS in both accuracy and efficiency, thanks to heuristic-driven optimization.
- Macro actions significantly reduce the search space, improving runtime.

---

## Attribution

- Parts of the codebase, specifically the `search.py` and `sokoban.py` files, were provided by **Queensland University of Technology (QUT)** as part of the IFN680 Artificial Intelligence and Machine Learning course. These files include essential utilities and search algorithms that support the implementation of the Sokoban solver.
- Additional code, including the heuristic function, taboo cell detection, and overall AI solver logic, was developed by the project authors.

---

## Limitations and Future Work

### Current Limitations:
- The Manhattan heuristic may fail in complex puzzles with tight spaces.
- Time complexity remains a challenge in large warehouses with many boxes.

### Future Improvements:
- Implementing **dynamic box-target assignment** for better heuristics.
- Exploring **reinforcement learning** or **deep learning** techniques.
- Adding iterative deepening to manage memory usage.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
