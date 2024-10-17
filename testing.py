from sokoban import Warehouse
from mySokobanSolver import *

import glob
import time


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
    wh.load_warehouse(problem_file)

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


def testAll(number=-1, limit_of_boxes=3):
    file_name = "*" if number == -1 else f"warehouse_{number:04}"
    all_warehouses = sorted(glob.glob('warehouses/' + file_name + '.txt'))

    for problem_file in all_warehouses:
        print(f'Testing {problem_file}')
        s = time.time()
        a = test_warehouse(problem_file, limit_of_boxes=limit_of_boxes)
        if a != "Skip":
            print(f'Answer: {a}')
            print(f'Time taken: {time.time() - s :.3f} seconds')
        print("")



if __name__ == '__main__':
    print("Team:", my_team(), "\n")
    test_taboo_cells()
    test_check_elem_action_seq()
    test_solve_sokoban_elem()
    # test_can_go_there()
    # test_solve_sokoban_macro()

    # testAll()