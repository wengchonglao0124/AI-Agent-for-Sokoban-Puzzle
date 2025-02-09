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

### Running the Solver

1. **Solve a puzzle using A\***:
   ```bash
   python mySokobanSolver.py --input data/warehouse_01.txt --algorithm astar
   ```

2. **Solve a puzzle using BFS**:
   ```bash
   python mySokobanSolver.py --input data/warehouse_01.txt --algorithm bfs
   ```

3. **Test all puzzles**:
   ```bash
   python testing.py
   ```

### Testing in Jupyter Notebook

Run the interactive notebook:
```bash
jupyter notebook notebooks/sokobanTester.ipynb
```

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

For more details, see the [Report.pdf](Report.pdf).

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

## Authors

- **Zhiyun Pan**: Algorithm design, heuristic implementation, and report writing.
- **Weng Chong Lao**: Code optimization, testing framework, and report finalization.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
