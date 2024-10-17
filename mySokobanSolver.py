'''
IFN680 Sokoban Assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
'''
import math
import search
import sokoban

def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    e.g.  [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    '''

    return [(9319638, 'Zhiyun', 'Pan'), (11679719, 'Weng Chong', 'Lao')]
 

def getTabooCellsList(walls: [(int, int)], targets: [(int, int)]) -> [(int, int)]:
    taboo_cell_set: set[(int, int)] = set()
    num_of_row, num_of_col = (max(y for _, y in walls) + 1), (max(x for x, _ in walls) + 1)

    # Extract all possible dead-end corners
    dead_corner_space: [[WarehouseCell]] = []
    for y in range(num_of_row):
        dead_corner_space.append([])
        for x in range(num_of_col):
            if not isWall(x, y, walls):
                warehouse_cell: WarehouseCell = createWarehouseCell(x, y, walls)
                if isDeadCorner(warehouse_cell) and not isTarget(x, y, targets):
                    dead_corner_space[-1].append(warehouse_cell)
        if not dead_corner_space[-1]:
            dead_corner_space.pop() # remove empty row

    # Determine all possible taboo cells
    for row in range(len(dead_corner_space)):
        num_of_item = len(dead_corner_space[row])
        for col in range(num_of_item):
            corner: WarehouseCell = dead_corner_space[row][col]
            corner_pos: (int, int) = corner.getPos()

            # Horizontal check
            x_free_dir_list: [(int, int)] = corner.getXFreeDir()
            if x_free_dir_list:
                # Rule 1 ----------------------------------------------------------------------------------------------
                walls_in_row: [(int, int)] = [coordinate for coordinate in walls if coordinate[1] == corner_pos[1]]
                for wall_pos in walls_in_row:
                    if checkVectorDirection(corner_pos, wall_pos, x_free_dir_list[0]):
                        taboo_cell_set.add(corner_pos)
                        break

                # Rule 2 ----------------------------------------------------------------------------------------------
                if col + 1 < num_of_item:
                    corner_next: WarehouseCell = dead_corner_space[row][col + 1]
                    corner_next_pos: (int, int) = corner_next.getPos()
                    x_free_dir_list_next: [(int, int)] = corner_next.getXFreeDir()

                    if x_free_dir_list_next:
                        if x_free_dir_list[0] == (1, 0) and checkOppositeVector(x_free_dir_list[0], x_free_dir_list_next[0]):
                            empty_space_list: [(int, int)] = []
                            for x_index in range(corner_pos[0] + 1, corner_next_pos[0]):
                                if isTarget(x_index, corner_pos[1], targets):
                                    empty_space_list = []
                                    break
                                else:
                                    cell: WarehouseCell = createWarehouseCell(x_index, corner_pos[1], walls)
                                    empty_space_list.append(cell)
                            if empty_space_list:
                                if checkContinueWalls(empty_space_list, (0, -1)) or checkContinueWalls(empty_space_list, (0, 1)):
                                    for empty_space in empty_space_list:
                                        taboo_cell_set.add(empty_space.getPos())

            # Vertical check
            y_free_dir_list: [(int, int)] = corner.getYFreeDir()
            if y_free_dir_list:
                # Rule 1 ----------------------------------------------------------------------------------------------
                walls_in_col: [(int, int)] = [coordinate for coordinate in walls if coordinate[0] == corner_pos[0]]
                for wall_pos in walls_in_col:
                    if checkVectorDirection(corner_pos, wall_pos, y_free_dir_list[0]):
                        taboo_cell_set.add(corner_pos)
                        break

                # Rule 2 ----------------------------------------------------------------------------------------------
                dead_corner_list_vertical: [WarehouseCell] = [dead_corner_cell for dead_corner_row in dead_corner_space for dead_corner_cell in dead_corner_row if dead_corner_cell.getPos()[0] == corner_pos[0] and dead_corner_cell.getPos()[1] > corner_pos[1]]
                dead_corner_list_vertical: [WarehouseCell] = sorted(dead_corner_list_vertical, key=lambda dead_corner_cell: dead_corner_cell.getPos()[1])
                num_of_dead_corner_vertical: int = len(dead_corner_list_vertical)

                if num_of_dead_corner_vertical > 0:
                    corner_next: WarehouseCell = dead_corner_list_vertical[0]
                    corner_next_pos: (int, int) = corner_next.getPos()
                    y_free_dir_list_next: [(int, int)] = corner_next.getYFreeDir()

                    if y_free_dir_list_next:
                        if y_free_dir_list[0] == (0, 1) and checkOppositeVector(y_free_dir_list[0], y_free_dir_list_next[0]):
                            empty_space_list: [(int, int)] = []
                            for y_index in range(corner_pos[1] + 1, corner_next_pos[1]):
                                if isTarget(corner_pos[0], y_index, targets):
                                    empty_space_list = []
                                    break
                                else:
                                    cell: WarehouseCell = createWarehouseCell(corner_pos[0], y_index, walls)
                                    empty_space_list.append(cell)
                            if empty_space_list:
                                if checkContinueWalls(empty_space_list, (-1, 0)) or checkContinueWalls(empty_space_list, (1, 0)):
                                    for empty_space in empty_space_list:
                                        taboo_cell_set.add(empty_space.getPos())
    return list(taboo_cell_set)


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    walls: [(int, int)] = warehouse.walls
    targets: [(int, int)] = warehouse.targets

    num_of_row, num_of_col = (max(y for _, y in walls) + 1), (max(x for x, _ in walls) + 1)
    taboo_cell: [(int, int)] = getTabooCellsList(walls, targets)

    return getTabooMapString(num_of_row, num_of_col, walls, taboo_cell)


WALL = '#'
TABOO_CELL = 'X'
BOX = '$'
EMPTY = ' '

class WarehouseCell(object):
    def __init__(self, x: int, y: int, free_dir: [(int, int)]):
        self.x: int = x
        self.y: int = y
        self.free_dir: [(int, int)] = free_dir

    def getPos(self) -> (int, int):
        return (self.x, self.y)

    def getNumOfAllFreeDir(self) -> int:
        return len(self.free_dir)

    def getAllFreeDir(self) -> [(int, int)]:
        return self.free_dir

    def getXFreeDir(self) -> [(int, int)]:
        return [(x, y) for x, y in self.free_dir if x != 0]

    def getNumOfXFreeDir(self) -> int:
        return len(self.getXFreeDir())

    def getYFreeDir(self) -> [(int, int)]:
        return [(x, y) for x, y in self.free_dir if y != 0]

    def getNumOfYFreeDir(self) -> int:
        return len(self.getYFreeDir())

def isWall(x: int, y: int, walls: [(int, int)]) -> bool:
    return (x, y) in walls

def isTarget(x: int, y: int, targets: [(int, int)]) -> bool:
    return (x, y) in targets

def isDeadCorner(cell: WarehouseCell) -> bool:
    if cell.getNumOfAllFreeDir() <= 2:
        if cell.getNumOfXFreeDir() <= 1 and cell.getNumOfYFreeDir() <= 1:
            return True
    return False

def createWarehouseCell(x: int, y: int, walls: [(int, int)]) -> WarehouseCell:
    free_dir: [(int, int)] = []
    if not isWall(x - 1, y, walls):
        free_dir.append((-1, 0)) # x negative direction - Left
    if not isWall(x + 1, y, walls):
        free_dir.append((1, 0)) # x positive direction - Right
    if not isWall(x, y - 1, walls):
        free_dir.append((0, -1)) # y negative direction - Top
    if not isWall(x, y + 1, walls):
        free_dir.append((0, 1)) # y positive direction - Down

    return WarehouseCell(x, y, free_dir)

def getTabooMapString(num_of_row: int, num_of_col: int, walls: [(int, int)], taboo_cell_list: [(int, int)]) -> str:
    taboo_map = [[EMPTY for _ in range(num_of_col)] for _ in range(num_of_row)]
    for x, y in walls:
        taboo_map[y][x] = WALL
    for x, y in taboo_cell_list:
        taboo_map[y][x] = TABOO_CELL

    result_list: [str] = [(''.join(row_list) + "\n") for row_list in taboo_map]
    result = ''.join(result_list)
    return result.rstrip('\n')

def checkVectorDirection(point1: (int, int), point2: (int, int), direction: (int, int)) -> bool:
    x1, y1 = point1
    x2, y2 = point2
    vector: (int, int) = (x2 - x1, y2 - y1)
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    unit_vector: (int, int) = (vector[0] / magnitude, vector[1] / magnitude)
    return unit_vector[0] == direction[0] and unit_vector[1] == direction[1]

def checkOppositeVector(vector1: (int, int), vector2: (int, int)) -> bool:
    return vector1[0] == -vector2[0] and vector1[1] == -vector2[1]

def checkContinueWalls(cells: [WarehouseCell], wall_direction: (int, int)) -> bool:
    for cell in cells:
        free_dir: [(int, int)] = cell.getXFreeDir() if wall_direction[0] != 0 else cell.getYFreeDir()
        if wall_direction in free_dir:
            return False
    return True


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. It uses search.Problem as a sub-class. 
    That means, it should have a:
    - self.actions() function
    - self.result() function
    - self.goal_test() function
    See the Problem class in search.py for more details on these functions.
    
    Each instance should have at least the following attributes:
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    
    
    '''
    
    def __init__(self, warehouse, allow_taboo_push=False, macro=False):
        self.warehouse: sokoban.Warehouse = warehouse
        self.allow_taboo_push: bool = allow_taboo_push
        self.macro: bool = macro

        initial: ((int, int), [(int, int)]) = warehouse.worker, warehouse.boxes
        super().__init__(initial)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        worker_pos, boxes = state

        taboo_cells_list = None
        if not self.allow_taboo_push:
            taboo_cells_list = getTabooCellsList(self.warehouse.walls, self.warehouse.targets)

        available_actions: [str] = []
        for action in movements.keys():
            result = check_action(worker_pos, boxes, self.warehouse.walls, action)
            if result != 'Failure':
                available_actions.append(action)

                if taboo_cells_list is not None:
                    _, boxes_new = result
                    for box in boxes_new:
                        if box in taboo_cells_list:
                            available_actions.remove(action)
                            break
        return available_actions

    def result(self, state, action):
        available_actions: [str] = self.actions(state)
        if action not in available_actions:
            return state
        else:
            worker_pos, boxes = state
            result = check_action(worker_pos, boxes, self.warehouse.walls, action)
            if result == 'Failure':
                return state
            else:
                return result


movements = {
    'Up': (0, -1),
    'Down': (0, 1),
    'Left': (-1, 0),
    'Right': (1, 0)
}

def check_action(worker_pos: (int, int), boxes: [(int, int)], walls: [(int, int)], action: str):
    boxes: [(int, int)] = boxes[:]
    dx, dy = movements[action]
    worker_pos_new: (int, int) = (worker_pos[0] + dx, worker_pos[1] + dy)

    # worker walk into a wall
    if worker_pos_new in walls:
        return 'Failure'

    if worker_pos_new in boxes:
        behind_pos: (int, int) = (worker_pos_new[0] + dx, worker_pos_new[1] + dy)

        # worker push one box into a wall
        if behind_pos in walls:
            return 'Failure'

        # worker push two boxes at the same time
        if behind_pos in boxes:
            return 'Failure'

        boxes.remove(worker_pos_new)
        boxes.append(behind_pos)

    return worker_pos_new, boxes


def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall, or walk into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    worker_pos: (int, int) = warehouse.worker
    boxes: [(int, int)] = warehouse.boxes[:]
    walls: [(int, int)] = warehouse.walls[:]

    for action in action_seq:
        result = check_action(worker_pos, boxes, walls, action)
        if result == 'Failure':
            return 'Failure'
        else:
            worker_pos, boxes = result

    warehouse_new: sokoban.Warehouse = warehouse.copy(worker_pos, boxes)
    return warehouse_new.__str__()


def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

