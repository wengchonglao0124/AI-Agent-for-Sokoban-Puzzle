Here’s the updated README.md file with a note acknowledging that parts of the code were developed by and belong to QUT:

AI Agent for Sokoban Puzzle

Introduction

Sokoban is a classic puzzle game where a worker pushes boxes to designated target locations within a warehouse. It is a challenging task due to its large state-space complexity and the potential for deadlocks caused by irreversible moves. This project introduces an AI Agent designed to solve Sokoban puzzles using A* and BFS algorithms, optimized with heuristics and search space reduction techniques.

The solver treats Sokoban as a state-space search problem and efficiently finds solutions for various puzzles by implementing:
	•	A* Search: Uses a heuristic-driven approach for optimal pathfinding.
	•	Breadth-First Search (BFS): Explores all states to ensure solutions, albeit less efficiently.
	•	Macro Actions: Groups multiple actions to minimize search depth and improve efficiency.

Features
	•	Heuristic Optimization: Leverages Manhattan distance and weighting to improve A* performance.
	•	Taboo Cell Detection: Identifies deadlocks to avoid exploring invalid states.
	•	Macro and Elementary Actions: Reduces complexity while maintaining solution optimality.
	•	Performance Analysis: Benchmarked on over 200 warehouse environments.

Repository Structure

📂 AI-Agent-for-Sokoban/
├── 📁 src/                  # Core files
│   ├── mySokobanSolver.py   # AI solver implementation
│   ├── search.py            # Search algorithms (QUT-provided template)
│   ├── sokoban.py           # Sokoban warehouse representation (QUT-provided template)
├── 📁 data/                 # Sokoban puzzles
│   ├── warehouse_01.txt
│   ├── warehouse_02.txt
│   ├── ... (other puzzles)
├── 📁 notebooks/            # Demonstration and testing
│   ├── sokobanTester.ipynb
├── 📄 README.md             # Project documentation
├── 📄 Report.pdf            # Analysis and results report
├── 📄 testing.py            # Automated testing for various cases
├── 📄 requirements.txt      # Dependency file
├── 📄 LICENSE               # License information

Installation and Setup
	1.	Clone this repository to your local machine:

git clone https://github.com/yourusername/AI-Agent-for-Sokoban-Puzzle.git
cd AI-Agent-for-Sokoban-Puzzle


	2.	Install the required dependencies:

pip install -r requirements.txt


	3.	(Optional) Use a virtual environment to isolate dependencies:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Usage

Running the Solver
	1.	Solve a puzzle using A*:

python src/mySokobanSolver.py --input data/warehouse_01.txt --algorithm astar


	2.	Solve a puzzle using BFS:

python src/mySokobanSolver.py --input data/warehouse_01.txt --algorithm bfs


	3.	Test all puzzles:

python testing.py



Testing in Jupyter Notebook

Run the interactive notebook:

jupyter notebook notebooks/sokobanTester.ipynb

Results

Performance Summary

Solver Type	Solved Percentage	Average Solve Time
A* (Macro)	90%	1.5s
A* (Elem)	85%	2.3s
BFS (Macro)	70%	3.1s
BFS (Elem)	60%	5.0s

Insights
	•	A* outperforms BFS in both accuracy and efficiency, thanks to heuristic-driven optimization.
	•	Macro actions significantly reduce the search space, improving runtime.

For more details, see the Report.pdf.

Attribution
	•	Parts of the codebase, specifically the search.py and sokoban.py files, were provided by Queensland University of Technology (QUT) as part of the IFN680 Artificial Intelligence and Machine Learning course. These files include essential utilities and search algorithms that support the implementation of the Sokoban solver.
	•	Additional code, including the heuristic function, taboo cell detection, and overall AI solver logic, was developed by the project authors.

Limitations and Future Work

Current Limitations:
	•	The Manhattan heuristic may fail in complex puzzles with tight spaces.
	•	Time complexity remains a challenge in large warehouses with many boxes.

Future Improvements:
	•	Implementing dynamic box-target assignment for better heuristics.
	•	Exploring reinforcement learning or deep learning techniques.
	•	Adding iterative deepening to manage memory usage.

Authors
	•	Zhiyun Pan: Algorithm design, heuristic implementation, and report writing.
	•	Weng Chong Lao: Code optimization, testing framework, and report finalization.

License

This project is licensed under the MIT License. See the LICENSE file for details.

This version acknowledges the QUT-provided code and distinguishes your contributions from theirs. Let me know if you’d like further tweaks!
