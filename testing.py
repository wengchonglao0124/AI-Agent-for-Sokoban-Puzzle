import search
import sokoban
from mySokobanSolver import *

import glob
import time


def test_solve_sokoban_elem():
    puzzle_t1 ='#######\n#@ $. #\n#######'
    wh = sokoban.Warehouse()
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Right']
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    puzzle_t2 ='#######\n#@ $ #.#\n#######'
    wh = sokoban.Warehouse()
    wh.extract_locations(puzzle_t2.split(sep='\n'))
    # second test
    answer = solve_sokoban_elem(wh)
    expected_answer = 'Impossible'
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)

# test_solve_sokoban_elem()


def test_warehouse(problem_file, macro=False):
    '''
    This function will test the performance of your warehouse for either macro or elem solutions and return the result.
    You can check if this solution works with your gui, or by cleverly using the check_action_seq function.
    '''

    wh = sokoban.Warehouse()
    wh.load_warehouse(problem_file)

    if macro:
        student_answer = solve_sokoban_macro(wh)
    else:
        student_answer = solve_sokoban_elem(wh)

    return student_answer


def testAll(number=-1):
    file_name = "*" if number == -1 else f"warehouse_{number:04}"
    all_warehouses = sorted(glob.glob('warehouses/' + file_name + '.txt'))

    for problem_file in all_warehouses:
        print(f'Testing {problem_file}')
        s = time.time()
        a = test_warehouse(problem_file)
        print(f'Answer: {a}')
        print(f'Time taken: {time.time() - s :.3f} seconds')

# testAll(9)