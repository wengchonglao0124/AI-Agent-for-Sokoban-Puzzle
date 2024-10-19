import time
import glob
import os
import multiprocessing as mp
import multiprocessing.queues as mpq
import sokoban
import search
from typing import Tuple
import csv
from mySokobanSolver import *


def test_warehouse(problem_file, macro=False, search_method='astar', limit_of_boxes=6):
    '''
    This function tests the performance of your warehouse using either macro or elem solutions
    and returns the result, time taken, and number of steps.
    '''
    wh = sokoban.Warehouse()
    try:
        wh.load_warehouse(problem_file)
    except Exception as e:
        print("An error occurred when loading the warehouse.")
        return "Error", None, None

    num_of_boxes = len(wh.boxes)
    if num_of_boxes > limit_of_boxes:
        print("Skip: number of boxes exceeds limit")
        return "Skip", None, None

    start_time = time.time()
    if macro:
        student_answer, num_steps = solve_sokoban_macro(wh, search_method=search_method)
    else:
        student_answer, num_steps = solve_sokoban_elem(wh, search_method=search_method)
    time_taken = time.time() - start_time

    return student_answer, time_taken, num_steps


def warehouse_timeout(args: Tuple[object], q: mp.Queue):
    # Do not alter this code.
    result, time_taken, num_steps = test_warehouse(*args)
    q.put((result, time_taken, num_steps))


def test_with_timeout(problem_file, macro=False, search_method='astar', timeout=180, limit_of_boxes=6):
    """
    This function tests on a warehouse with the ability to timeout after a specified number of seconds.

    Parameters:
    problem_file (str): directory of a warehouse
    macro (bool): indicates whether to use the macro solver. If false, will use the elem solver
    search_method (str): 'astar' or 'bfs' indicating which search method to use
    timeout (int): The number of seconds the solver can run without timing out.
    limit_of_boxes (int): The maximum number of boxes allowed.

    Returns:
    A tuple (result, time_taken, num_steps) where result is the solver solution or a string indicating the outcome,
    time_taken is the time taken in seconds, and num_steps is the number of steps in the solution.
    """
    q_worker = mp.Queue()
    proc = mp.Process(target=warehouse_timeout, args=((problem_file, macro, search_method, limit_of_boxes), q_worker))
    proc.start()
    try:
        res = q_worker.get(timeout=timeout)
        result, time_taken, num_steps = res
    except mpq.Empty:
        proc.terminate()
        result = "Timed out"
        time_taken = None
        num_steps = None
    finally:
        proc.join()
    return result, time_taken, num_steps


def testAll(number=-1, timeout=180, limit_of_boxes=6):
    file_name = "*" if number == -1 else f"warehouse_{number:04}"
    all_warehouses = sorted(glob.glob('warehouses/' + file_name + '.txt'))

    # Prepare a list to store the results
    results = []

    for problem_file in all_warehouses:
        print(f'Testing {problem_file}')
        warehouse_name = os.path.basename(problem_file)
        num_of_boxes = None

        # Get the number of boxes
        wh = sokoban.Warehouse()
        try:
            wh.load_warehouse(problem_file)
            num_of_boxes = len(wh.boxes)
            print(f'Number of boxes: {num_of_boxes}')
            if num_of_boxes > limit_of_boxes:
                print("Skip: number of boxes exceeds limit")
                # Record 'Skip' for all methods
                result_row = {
                    'Warehouse': warehouse_name,
                    'elem_astar': 'Skip',
                    'elem_bfs': 'Skip',
                    'macro_astar': 'Skip',
                    'macro_bfs': 'Skip',
                    'elem_astar_time': '',
                    'elem_bfs_time': '',
                    'macro_astar_time': '',
                    'macro_bfs_time': '',
                    'elem_astar_steps': '',
                    'elem_bfs_steps': '',
                    'macro_astar_steps': '',
                    'macro_bfs_steps': ''
                }
                results.append(result_row)
                continue
        except Exception as e:
            print("An error occurred when loading the warehouse.")
            # Record 'Error' for all methods
            result_row = {
                'Warehouse': warehouse_name,
                'elem_astar': 'Error',
                'elem_bfs': 'Error',
                'macro_astar': 'Error',
                'macro_bfs': 'Error',
                'elem_astar_time': '',
                'elem_bfs_time': '',
                'macro_astar_time': '',
                'macro_bfs_time': '',
                'elem_astar_steps': '',
                'elem_bfs_steps': '',
                'macro_astar_steps': '',
                'macro_bfs_steps': ''
            }
            results.append(result_row)
            continue

        # Define methods to test
        methods = [
            {'macro': False, 'search_method': 'astar', 'name': 'elem_astar'},
            {'macro': False, 'search_method': 'bfs', 'name': 'elem_bfs'},
            {'macro': True, 'search_method': 'astar', 'name': 'macro_astar'},
            {'macro': True, 'search_method': 'bfs', 'name': 'macro_bfs'},
        ]

        result_row = {'Warehouse': warehouse_name}
        for m in methods:
            method_name = m['name']
            print(f'Testing method: {method_name}')
            result, time_taken, num_steps = test_with_timeout(problem_file, macro=m['macro'],
                                                              search_method=m['search_method'], timeout=timeout,
                                                              limit_of_boxes=limit_of_boxes)
            if result == "Timed out":
                print(f"Solver timed out: {timeout}s")
                result_str = "Timed out"
                time_str = ''
                steps_str = ''
            elif result == "Skip":
                print("Warehouse skipped due to too many boxes.")
                result_str = "Skip"
                time_str = ''
                steps_str = ''
            elif result == "Error":
                print("Error loading warehouse.")
                result_str = "Error"
                time_str = ''
                steps_str = ''
            else:
                if result == "Impossible":
                    print("Puzzle is impossible to solve.")
                    result_str = "Impossible"
                    steps_str = ''
                else:
                    print(f'Solution found.')
                    result_str = "Solution found"
                    steps_str = str(num_steps)
                time_str = f'{time_taken:.3f}s' if time_taken is not None else ''
            # Record the result, time, and steps
            result_row[method_name] = result_str
            result_row[method_name + '_time'] = time_str
            result_row[method_name + '_steps'] = steps_str
            print(f'Time taken: {time_str}')
            print(f'Number of steps: {steps_str}')
            print("")
        results.append(result_row)

    # Save results to CSV
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Warehouse',
                      'elem_astar', 'elem_astar_time', 'elem_astar_steps',
                      'elem_bfs', 'elem_bfs_time', 'elem_bfs_steps',
                      'macro_astar', 'macro_astar_time', 'macro_astar_steps',
                      'macro_bfs', 'macro_bfs_time', 'macro_bfs_steps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def solve_sokoban_elem(warehouse, search_method='astar'):
    '''
    This function solves the Sokoban puzzle using elementary actions.

    @param warehouse: a valid Warehouse object
    @param search_method: 'astar' or 'bfs' indicating which search method to use

    @return
        If puzzle cannot be solved return the string 'Impossible' and None for steps
        If a solution was found, return the solution and the number of steps
    '''
    solver = SokobanPuzzle(warehouse)
    if search_method == 'astar':
        solution = search.astar_graph_search(solver)
    elif search_method == 'bfs':
        solution = search.breadth_first_graph_search(solver)
    else:
        raise ValueError(f"Unknown search method: {search_method}")
    if solution:
        return solution.solution(), solution.path_cost
    else:
        return "Impossible", None


def solve_sokoban_macro(warehouse, search_method='astar'):
    '''
    Solve the Sokoban puzzle using macro actions.

    @param warehouse: a valid Warehouse object
    @param search_method: 'astar' or 'bfs' indicating which search method to use

    @return
        If puzzle cannot be solved return the string 'Impossible' and None for steps
        Otherwise return the solution and the number of steps
    '''
    solver = SokobanPuzzle(warehouse, macro=True)
    if search_method == 'astar':
        solution = search.astar_graph_search(solver)
    elif search_method == 'bfs':
        solution = search.breadth_first_graph_search(solver)
    else:
        raise ValueError(f"Unknown search method: {search_method}")
    if solution:
        return solution.solution(), solution.path_cost
    else:
        return "Impossible", None


# Ensure that all necessary modules and classes are imported and defined as per your previous code.
# This includes SokobanPuzzle, movements, and any helper functions.

# Example of running the testAll function:
if __name__ == "__main__":
    testAll(timeout=180, limit_of_boxes=100)