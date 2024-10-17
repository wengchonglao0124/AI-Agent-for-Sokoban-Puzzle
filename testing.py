from sokoban import Warehouse
from mySokobanSolver import *

import glob
import time
import multiprocessing as mp
import multiprocessing.queues as mpq
from typing import Tuple, Callable, Dict


def test_taboo_cells():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_0001.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
    fcn = test_taboo_cells
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)


def test_check_elem_action_seq():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_0001.txt")
    # first test
    answer = check_action_seq(wh, ['Right', 'Right', 'Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    fcn = test_check_elem_action_seq
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)
    # second test
    answer = check_action_seq(wh, ['Right', 'Right', 'Right'])
    expected_answer = 'Failure'
    fcn = test_check_elem_action_seq
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)


def test_solve_sokoban_elem():
    puzzle_t1 = '#######\n#@ $. #\n#######'
    wh = Warehouse()
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Right']
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)
    # second test
    puzzle_t2 = '#######\n#@ $ #.#\n#######'
    wh = Warehouse()
    wh.extract_locations(puzzle_t2.split(sep='\n'))
    # second test
    answer = solve_sokoban_elem(wh)
    expected_answer = 'Impossible'
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)


def test_can_go_there():
    puzzle_t1 = '#######\n#@ $. #\n#######'
    wh = Warehouse()
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = can_go_there(wh, (1, 2))
    expected_answer = True
    fcn = test_can_go_there
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)
    # second test
    answer = can_go_there(wh, (1, 5))
    expected_answer = False
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)


def test_can_go_there_custom(number: int, dst: (int, int), expected_answer: bool):
    file_name = f"warehouse_{number:04}"
    all_warehouses = sorted(glob.glob('warehouses/' + file_name + '.txt'))

    for problem_file in all_warehouses:
        fcn = test_can_go_there
        print('<<  Test of {} >>'.format(fcn.__name__))
        wh = sokoban.Warehouse()
        try:
            wh.load_warehouse(problem_file)
        except Exception as e:
            print("An error occurred when loading the warehouse.")

        answer = can_go_there(wh, dst, True)
        if answer == expected_answer:
            print(fcn.__name__, ' passed!  :-)\n')
        else:
            print(fcn.__name__, ' failed!  :-(')
            print('Expected ');
            print(expected_answer)
            print('But, received ');
            print(answer)


def test_solve_sokoban_macro():
    puzzle_t2 = '#######\n#@ $ .#\n#######'
    wh = Warehouse()
    wh.extract_locations(puzzle_t2.split(sep='\n'))
    # first test
    answer = solve_sokoban_macro(wh)
    expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
    fcn = test_solve_sokoban_macro
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer == expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');
        print(expected_answer)
        print('But, received ');
        print(answer)


def test_warehouse(problem_file, macro=False, limit_of_boxes=3):
    '''
    This function will test the performance of your warehouse for either macro or elem solutions and return the result.
    You can check if this solution works with your gui, or by cleverly using the check_action_seq function.
    '''
    wh = sokoban.Warehouse()
    try:
        wh.load_warehouse(problem_file)
    except Exception as e:
        print("An error occurred when loading the warehouse.")
        return "Error"

    num_of_boxes = len(wh.boxes)
    print(f'Number of boxes: {num_of_boxes}')
    if num_of_boxes > limit_of_boxes:
        print("Skip: number of boxes exceeds limit")
        return "Skip"

    if macro:
        student_answer = solve_sokoban_macro(wh)
    else:
        student_answer = solve_sokoban_elem(wh)

    return student_answer


def warehouse_timeout(args: Tuple[object], q: mp.Queue):
    # Do not alter this code.
    q.put(test_warehouse(*args))


def test_with_timeout(problem_file, macro=False, timeout=180, limit_of_boxes=3):
    """
    This function tests on a warehouse with the ability to timeout after a specified number of seconds.

    Parameters:
    problem_file (str): directory of a warehouse
    macro (bool): indicates whether to use the macro solver. If false, will use the elem solver
    timeout (int): The number of seconds the solver can run without timing out.
    limit_of_boxes (int): The maximum number of boxes allowed.

    Returns:
    The solver solution or the string "Timed out" or "Skip"
    """
    q_worker = mp.Queue()
    proc = mp.Process(target=warehouse_timeout, args=((problem_file, macro, limit_of_boxes), q_worker))
    proc.start()
    try:
        res = q_worker.get(timeout=timeout)
    except mpq.Empty:
        proc.terminate()
        res = "Timed out"
    finally:
        proc.join()
    return res


def testAll(number=-1, timeout=180, limit_of_boxes=5):
    file_name = "*" if number == -1 else f"warehouse_{number:04}"
    all_warehouses = sorted(glob.glob('warehouses/' + file_name + '.txt'))

    num_of_correct: int = 0
    for problem_file in all_warehouses:
        print(f'Testing {problem_file}')
        s = time.time()
        a = test_with_timeout(problem_file, timeout=timeout, limit_of_boxes=limit_of_boxes)
        if a == "Skip":
            print("Warehouse skipped due to too many boxes.")
        elif a == "Timed out":
            print(f"Solver timed out: {timeout}s")
        elif a == "Error":
            print("Skip ->")
        else:
            print(f'Answer: {a}')
            print(f'Time taken: {time.time() - s :.3f} seconds')
            num_of_correct += 1
        print("")

    print("Accuracy is", num_of_correct*100 / len(all_warehouses), "%")
    print("=======================================================")



if __name__ == '__main__':
    print("Team:", my_team(), "\n")
    test_taboo_cells()
    test_check_elem_action_seq()
    test_solve_sokoban_elem()
    test_can_go_there()
    test_can_go_there_custom(191, (12, 1), True)
    test_can_go_there_custom(191, (1, 17), False)
    # test_solve_sokoban_macro()

    # testAll()