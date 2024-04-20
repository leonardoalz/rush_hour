from copy import deepcopy
from collections import deque
import time
import resource
import heapq

class Car(object):
    ''' need to define each car in the game
        name: which character it is, can save as colour
        size: how long the car is/how many fields of the game
        coordinate: start coordinate, always use the upper/most right point
        orientation: horizontally or vertically 
        red car: one to be freeed yes or no '''

    def __init__(self,name, size, coord, orientation, red_car):
        self.name = name
        self.size = size-1  # we use -1, bc we count the index
        self.coord = coord
        self.orientation = orientation
        self.redcar = red_car

    def __eq__(self, other):
        # tests if two classes are equal
        return self.__dict__ == other.__dict__

    def __str__(self):
        # returns a string representation of all information of a class
        return str(self.__dict__)

    def __ne__(self, other):
        # compares if two classes are not equal
        return not self.__eq__(other)

    def __hash__(self):
        ''' used to define how instances of a class should be hashed. Hashing is a process of mapping 
        data of arbitrary size to fixed-size values, typically for faster access in data structures like dictionaries or sets '''
        return hash(self.__repr__())

    
    def __repr__(self,board):
        if self.orientation == 'horizontal':
            other_coord = {'x': self.coord[0] + self.size,
                           'y': self.coord[1]}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)
        else:
            other_coord = {'x': self.coord[
                0], 'y': self.coord[1] + self.size}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)  # other coordninate is the end of the car 


    def move(self, direction, distance=1):       
        # moves we can do, always go one step at a time
    
        if self.orientation == 'vertical':
            if direction == 'up':
                self.coord[1] -= distance
    
            if direction == 'down':
                self.coord[1] += distance
        else:
            if direction == 'left':
                self.coord[0] -= distance
        
            if direction == 'right':      
                self.coord[0] += distance


class Board(object):
    # 6x6 board size

    def __init__(self, board,cars,size=6):
        # board a list of lists
        # cars 
        self.board = deepcopy(board)
        self.size = {'x': len(board), 'y': len(board[0])}
        self.width = len(board)
        self.height = len(board[0])
        self.cars = cars
        self.g_score = 0    # Initialize g_score attribute for A*
        self.f_score = 0    # Initialize f_score attribute for A*

    def __eq__(self, other):
        # tests if two boards have the same layout
        return self.board == other.board

    def __ne__(self, other):
        # compares if two classes are not equal
        return not self.__eq__(other)
    
    def __lt__(self, other):
        # compare based on f_score
        return self.f_score < other.f_score

    def __hash__(self):
        ''' used to define how instances of a class should be hashed. Hashing is a process of mapping 
        data of arbitrary size to fixed-size values, typically for faster access in data structures like dictionaries or sets. '''
        return hash(self.__repr__())

    def next_possible_moves(self):
        # checks the next possible moves from a board, but does not do them
        for car in self.cars:  # check each car object in the field for the next movement 
            if car.orientation == 'vertical':
                # UP
                if car.coord[1] > 0 and self.board[car.coord[1] - 1][car.coord[0]] == '#':
                    new_board = deepcopy(self.board)
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord[1] -= 1
                    new_board[car.coord[1] - 1][car.coord[0]] = car.name  # Update the board
                    new_board[car.coord[1] + car.size][car.coord[0]] = '#'  # Clear the previous position
                    yield [[[car.name, 'up']], Board(new_board, new_cars)]  # Yield the performed move and the new board state
                # DOWN
                if car.coord[1] + car.size + 1 <= (self.size['y'] - 1) and self.board[car.coord[1] + car.size + 1][car.coord[0]] == '#':
                    new_board = deepcopy(self.board)
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord[1] += 1
                    new_board[car.coord[1] + car.size + 1][car.coord[0]] = car.name  # Update the board
                    new_board[car.coord[1]][car.coord[0]] = '#'  # Clear the previous position
                    yield [[[car.name, 'down']], Board(new_board, new_cars)]  # Yield the performed move and the new board state
            else:
                # LEFT
                if car.coord[0] - 1 >= 0 and self.board[car.coord[1]][car.coord[0] - 1] == '#':
                    new_board = deepcopy(self.board)
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord[0] -= 1
                    new_board[car.coord[1]][car.coord[0] - 1] = car.name  # Update the board
                    new_board[car.coord[1]][car.coord[0] + car.size] = '#'  # Clear the previous position
                    yield [[[car.name, 'left']], Board(new_board, new_cars)]  # Yield the performed move and the new board state
                # RIGHT
                if car.coord[0] + car.size + 1 <= (self.size['x'] - 1) and self.board[car.coord[1]][car.coord[0] + car.size + 1] == '#':
                    new_board = deepcopy(self.board)
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord[0] += 1
                    new_board[car.coord[1]][car.coord[0] + car.size + 1] = car.name  # Update the board
                    new_board[car.coord[1]][car.coord[0]] = '#'  # Clear the previous position
                    yield [[[car.name, 'right']], Board(new_board, new_cars)]  # Yield the performed move and the new board state



    def __str__(self, board):
        # printable version that represents the 2D array of the puzzle
        board_str = ""
        for row in board.board:
            board_str += '|' + '|'.join(str(cell) for cell in row) + '|\n'
        
        return board_str
                
        ''' for sub in board.board:
            print(sub) '''
      
    def goal_state(self):
        # checking if the red car is in the right position
        for cars in self.cars:
            if cars.name == 0 and cars.coord[0] == 4:
                return True
       
        return False
    
    def problems(difficulty, version):
        easy = [[['#','#','#','#','#',1],['#','#','#','#','#',1], [0,0,'#','#','#',1], ['#','#','#',2,2,2], ['#','#',3,3,4,4], ['#','#','#','#','#','#']], 
                [['#','#','#','#','#','#'],['#','#','#',1,'#','#'],[0,0,'#',1,2,'#'],['#','#','#','#',2,'#'],['#','#','#','#',3,'#'],['#','#','#','#',3,'#']],
                [['#','#','#','#',1,1],['#','#','#','#','#',2],[0,0,'#',3,'#',2],['#','#','#',3,4,4],['#','#','#','#','#','#'],['#','#','#','#','#','#']]]
        
        
        medium = [[['#',1,2,3,3,3],['#',1,2,'#','#',4], [0,0,2,'#','#',4], [5,5,5,'#','#','#'], ['#',6,6,'#',7,7], ['#','#','#','#','#','#']], 
                [[1,'#','#','#','#',2],[1,'#','#','#','#',2],[1,3,3,0,0,4],['#','#','#','#','#',4],['#','#',5,6,6,6],[7,7,5,'#','#','#']],
                [['#','#','#',1,2,2],['#','#','#',1,'#',3],[4,4,0,0,'#',3],['#','#','#','#','#','#'],[5,6,6,6,7,7],[5,'#','#','#','#','#']]]
        
        
        hard = [[['#','#',1,2,2,2],['#','#',1,'#',3,3], [0,0,1,4,'#',5], [6,6,6,4,'#',5], ['#','#',7,7,8,8], ['#','#',9,9,'#','#']], 
                [['#',1,2,2,3,3],['#',1,'#',4,4,5],['#',1,0,0,6,5],['#','#','#','#',6,'#'],[7,7,8,8,8,'#'],['#','#','#','#','#','#']],
                [['#','#','#',1,1,1],['#',2,2,2,3,3],[4,4,4,0,0,5],['#','#','#','#','#',5],['#','#',6,7,7,7],['#','#',6,'#','#','#']]]
        
        if difficulty == 'easy': 
            return easy[version-1]
        elif difficulty == 'medium': 
            return medium[version-1]
        elif difficulty == 'hard':
            return hard[version-1]
        else:
            print("Level not found.\n")
    
    
def create_board(difficulty, version):
    prob = Board.problems(difficulty, version)  # gets the according level 
    
    # generates the car information to play 
    cars_coord = {}

    for y, row in enumerate(prob):
        for x, value in enumerate(row):
            if isinstance(value, int) and value not in cars_coord:
                cars_coord[value] = (x, y)
                
    raw_cars = []
    
    for k,v in cars_coord.items():
        
        def plane(coords, prob):
            # determines the orientation of the car, only works when calles
            x = coords[0]
            y = coords[1]
            if x<5 and prob[y][x] == prob[y][x+1]:
                # print("h",x,y)
                return 'horizontal'
            else:
                # print("v",x,y)             
                return 'vertical'
            
        def size(k, prob):
            s = 0
            for i in range(len(prob)):
                for j in range(len(prob[0])):
                    if k == prob[i][j]:
                        s += 1
            return s
        
        def red(k):
            if k == 0:
                return 'yes'
            return 'no'
            
            
        raw_cars.append(Car(k, size(k,prob), list(v), plane(v,prob),red(k)))
        
        
    return Board(prob, raw_cars)
      

def play_game():
    while True:
        difficulty = input("\n- Enter the difficulty -\n(easy, medium, hard): ")
        if difficulty not in  ['easy', 'medium', 'hard']:
            print("Invalid option! Please choose a valid one.")
            continue
            
        version = int(input("\n- Which version do you want to play? -\n(1, 2, 3): "))
        print('\n')
            
        move_count = 0
        
        board= create_board(difficulty,version)
            
        print("Initial board state:")
        
        while True:
            print(board.__str__(board))
            
            # check for win condition
            if board.goal_state():
                print("Congratulations! You have won!")
                break
            
            # display the current state of the board
            
            # get user input
            help = int(input("\n- Do you want help to finish the game? -\n1: Yes\n0: No\n"))
            if (help == 1):
                breadth_first_search( board, lambda board: board.goal_state(), lambda board: board.next_possible_moves() )
                print("\nThat is one solution!\n")
                break
                
            car_name = int(input("\n- Enter car number to move -\n(0, 1, 2, 3, etc.): "))
            direction = input("\n- Enter direction -\n(up, down, left, right): ")
            
            print('\n')
            
            # move the car
            for move, new_board in board.next_possible_moves():
        
                # print("Available move:", move)  # debug print statement
                # print("User input - Car name:", car_name, "Direction:", direction)
                if move[0][0] == car_name and move[0][1] == direction:
                    board = new_board
                    move_count += 1
                    break
            else:
                print("Invalid move! Try again.")
                continue


def test_game():
    while True:
        difficulty = input("\n- Enter the difficulty -\n(easy, medium, hard): ")
        if difficulty not in  ['easy', 'medium', 'hard']:
            print("Invalid option! Please choose a valid one.")
            continue
        version = int(input("\n- Which version do you want to play? -\n(1, 2, 3): "))
        print('\n')
            
        move_count = 0
        
        board = create_board(difficulty, version)
            
        print("Initial board state: ")
        
        while True:
            print(board.__str__(board))
            
            # check for win condition
            if board.goal_state():
                print("Congratulations! You have won!")
                break
            
            # display the current state of the board
            
            # get user input
            help_test = int(input("Do you want help to test the game?\n1: Yes\n0: No\n"))
            if help_test:
                algorithm = int(input("\nWhich algorithm do you want to use?\n1: BFS, 2: DFS, 3: Depth Limited Search, 4: Greedy, 5: A*? "))
                if algorithm == 1:
                    start_time = time.time()
                    breadth_first_search(board, lambda board: board.goal_state(), lambda board: board.next_possible_moves())
                    print("--- %s seconds ---" % (time.time() - start_time))
                elif algorithm == 2:
                    start_time = time.time()
                    depth_first_search(board, lambda board: board.goal_state(), lambda board: board.next_possible_moves())
                    print("--- %s seconds ---" % (time.time() - start_time))
                elif algorithm == 3:
                    depth = int(input("Enter the maximum depth: "))
                    start_time = time.time()
                    depth_limited_search(depth, board, lambda board: board.goal_state(), lambda board: board.next_possible_moves())
                    print("--- %s seconds ---" % (time.time() - start_time))
                elif algorithm == 4:
                    heuristic = int(input("Which heuristic function do you want to use? 1: h1, 2: h2 "))
                    if heuristic == 1:
                        start_time = time.time()
                        greedy_search(board, lambda board: board.goal_state(), h1)
                        print("--- %s seconds ---" % (time.time() - start_time))
                    elif heuristic == 2:
                        start_time = time.time()
                        greedy_search(board, lambda board: board.goal_state(), h2)
                        print("--- %s seconds ---" % (time.time() - start_time))
                elif algorithm == 5:
                    heuristic = int(input("Which heuristic function do you want to use? 1: h1, 2: h2 "))
                    if heuristic == 1:
                        start_time = time.time()
                        a_star_search(board, lambda board: board.goal_state(), h1, lambda board: board.next_possible_moves())
                        print("--- %s seconds ---" % (time.time() - start_time))
                    elif heuristic == 2:
                        start_time = time.time()
                        a_star_search(board, lambda board: board.goal_state(), h2, lambda board: board.next_possible_moves())
                        print("--- %s seconds ---" % (time.time() - start_time))

                # get maximum memory usage (not available by default on Windows)
                resource_usage = resource.getrusage(resource.RUSAGE_SELF)
                max_memory_used = resource_usage.ru_maxrss / 1024  # Convert from kilobytes to megabytes
                print("Maximum memory usage (MB): ", max_memory_used)
                
                break

            car_name = int(input("\n- Enter car number to move -\n(0, 1, 2, 3, etc.): "))
            direction = input("\n- Enter direction -\n(up, down, left, right): ")
            
            print('\n')
            
            # move the car
            for move, new_board in board.next_possible_moves():
                if move[0][0] == car_name and move[0][1] == direction:
                    board = new_board
                    move_count += 1
                    break
            else:
                print("Invalid move! Try again.")
                continue
 
    
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue/list to store the nodes
    
    
    visited = [initial_state]  # to avoid loops
    nodes_generated = 1  # Initial node (root) is already generated

    while queue:                # still have states to expand
        node = queue.popleft()   # get first element in the queue

        if goal_state_func(node.state):   # check goal state
            print_solution(node)
            print("Nodes generated:", nodes_generated)
            return node

        for action, state in operators_func(node.state):   # go through next states
            if state not in visited:
                child_node = TreeNode(state=state, parent=node)  # create tree node with the new state
                node.add_child(child_node)  # link child node to its parent in the tree
                queue.append(child_node)    # enqueue the child node
                visited.append(state)      # to avoid loops
                nodes_generated += 1

    return None


def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = deque([root])   #stores all the nodes
    visited = [initial_state]   #for depth first search it is very important to check for the visited states
    node_count = 1  # initialize node count
    
    while queue:
        node = queue.pop()  # does the popping of the pilha
        node_count += 1 # increment node count
        
        if goal_state_func(node.state):
            print_solution(node)
            print("Total nodes generated:", node_count) # print total node count
            return node
        
        for action, state in operators_func(node.state):    #state stand for the next possible state
            if state not in visited:    #verifies if we already visited/checked that state
                child_node = TreeNode(state=state, parent=node)
                node.add_child(child_node)  #adds the child to the tree
                queue.append(child_node)    #appends the next node to the states we need to check 
                visited.append(state)   #will add the stated to the visited ones
    return None
   
            
def depth_limited_search(maxdepth, initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = deque([(root, 0)])
    visited = [initial_state]   # for depth first search it is very important to check for the visited states
    node_count = 1  # initialize node count
    
    while queue:
        node, depth = queue.pop()   # does the popping of the pilha, get the next node to expand
        node_count += 1 # increment node count
        
        if depth <= maxdepth:
            if goal_state_func(node.state):
                print_solution(node)
                print("Total nodes generated:", node_count) # print total node count
                return None
            
            for action, state in operators_func(node.state):    # state stand for the next possible state
                if state not in visited:    # verifies if we already visited/checked that state
                    child_node = TreeNode(state=state, parent=node)
                    node.add_child(child_node)
                    queue.append((child_node, depth + 1))
                    visited.append(state)
    print("No solution at depth {}".format(maxdepth))
    return None


def print_solution(node):
    if node:
        path = []
        while node:
            path.append(node)
            node = node.parent
        print("Found goal state in {} steps:".format(len(path)-1))
        for step in reversed(path):
            print(step.state.__str__(step.state))
        
    
def h1(state):
    # returns the number of cars infront of the red car, tends to underestimate 
    total = 0
    red_found = 0
    cars_found = []
    for i in range(6):
        if state.board[2][i] != '#':
            if state.board[2][i] == 0:
                red_found = 1
            if red_found ==1:
                if state.board[2][i] > 0 and state.board[2][i] not in cars_found:
                    total +=1
                    cars_found.append(state.board[2][i])
    return total 


def h2(state):
    red_car_position = None
    for y, row in enumerate(state.board):
        for x, value in enumerate(row):
            if value == 0:  # Red car found
                red_car_position = (x, y)
                break
        if red_car_position:
            break
    
    # calculate Manhattan distance from red car's position to the goal position (2, 4)
    goal_position = (4, 2)
    distance = abs(red_car_position[0] - goal_position[0]) + abs(red_car_position[1] - goal_position[1])
    return distance


def greedy_search(initial_state, goal_state_func, heuristic):
    setattr(Board, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [initial_state]
    visited = []    # to not visit the same state twice
    node_count = 1  # initialize node count
    
    while states:
        current = heapq.heappop(states) # current is an instance of the Board Class
        visited.append(current)
        if goal_state_func(current):    # check goal state, node is from TreeNode
            print("It took {} steps to find the solution.".format(len(visited) - 1))    # just print the nr of steps bc the heuristic is not that good
            print("Total nodes generated:", node_count) # print total node count
            return None

        for move, child in current.next_possible_moves():
            if child not in visited:
                heapq.heappush(states, child)   # child is the item we will add to states
                node_count += 1 # increment node count
    
    print("No solution found.\n")
    return None


def a_star_search(initial_state, goal_state_func, heuristic_func, operators_func):
    states = [] # priority queue to store states
    heapq.heappush(states, initial_state)   # add initial state to priority queue
    visited = set() # initialize visited set
    nodes_generated = 1 # initial node (root) is already generated

    while states:   # while there are states to explore
        current_state = heapq.heappop(states)   # pop state with the lowest f_score
        visited.add(current_state)  # add current state to visited set

        if goal_state_func(current_state):  # check if current state is the goal state
            print_solution(current_state)
            print("Nodes generated:", nodes_generated)
            return current_state

        for action, next_state in operators_func(current_state):    # generate next possible moves
            if next_state not in visited:
                # calculate tentative g_score for the next state
                tentative_g_score = current_state.g_score + 1

                # update the next state's g_score and f_score if it represents an improvement
                if tentative_g_score < next_state.g_score:
                    next_state.g_score = tentative_g_score
                    next_state.f_score = tentative_g_score + heuristic_func(next_state)
                    heapq.heappush(states, next_state)  # add next state to priority queue
                    nodes_generated += 1

    return None


def main():
    while True:
        option = int(input("\n- Choose an option -\n1: Play game\n2: Test game algorithms\n"))
        if option == 1:
            play_game()
        elif option == 2:
            test_game()
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()