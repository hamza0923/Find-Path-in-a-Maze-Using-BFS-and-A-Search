#Libraries Needed
import math
from queue import PriorityQueue
from queue import Queue

#function to print grid
def print_grid(Grid, Message=None, Path=None, Start_x=None, Start_y=None, End_x=None, End_y=None):
    if Message:
        print(Message)


    for i in range(len(Grid)):   # Loop through the rows of the grid
        for j in range(len(Grid[i])):  # Loop through the columns of the grid

            if j == 0:  # If this is the first column of the row, print a tab
                print("\t\t", end="  ")

            if i == Start_y and j == Start_x:  # If this cell is the start point, print it in bold
                print("\033[1mS\033[0m", end="  ")

            elif i == End_y and j == End_x:  # If this cell is the end point, print it in bold
                print("\033[1mG\033[0m", end="  ")

            elif Path and (i, j) in Path:  # If a path is provided and this cell is on the path, print an asterisk in bold
                print("\033[1m*\033[0m", end="  ")

            elif Grid[i][j] == 1:  # If this cell is a barrier, print a 1
                print("1", end="  ")

            else:  # Otherwise, print a 0
                print("0", end="  ")

        if j == len(Grid[i]) - 1:  # If this is the last column of the row, print a newline
            print("")


# Defines a function to get all valid neighbors of a node
def get_neighbors(node):
    # get the x and y coordinate of the current node
    y, x = node
    # initialize an empty list for storing the neighboring nodes
    neighbors = []
    # check if the node to the top of the current node is valid and add it to the list of neighbors
    if y > 0 and grid[y-1][x] != 1:
        neighbors.append((y-1, x))
    # check if the node to the right of the current node is valid and add it to the list of neighbors
    if x < grid_sz_x-1 and grid[y][x+1] != 1:
        neighbors.append((y, x+1))
    # check if the node to the bottom of the current node is valid and add it to the list of neighbors
    if y < grid_sz_y-1 and grid[y+1][x] != 1:
        neighbors.append((y+1, x))
    # check if the node to the left of the current node is valid and add it to the list of neighbors
    if x > 0 and grid[y][x-1] != 1:
        neighbors.append((y, x-1))
    # return the list of valid neighbors
    return neighbors



# Define a function to get the cost of moving from node1 to node2
def get_cost(node1, node2):
    y1, x1 = node1
    y2, x2 = node2

    # Check if moving to the right is a valid move
    if y1 == y2 and x2 == x1 + 1:  # right
        # If moving to the right is valid, return a cost of 2 if neither node is blocked,
        # otherwise return a high cost of 1000000 to discourage choosing this path
        return 2 if (grid[y1][x1] != 1 and grid[y2][x2] != 1) else 1000000

    # Check if moving to the left is a valid move
    elif y1 == y2 and x2 == x1 - 1:  # left
        # If moving to the left is valid, return a cost of 3 if neither node is blocked,
        # otherwise return a high cost of 1000000 to discourage choosing this path
        return 3 if (grid[y1][x1] != 1 and grid[y2][x2] != 1) else 1000000

    # Check if moving up is a valid move
    elif x1 == x2 and y2 == y1 - 1:  # up
        # If moving up is valid, return a cost of 2 if neither node is blocked,
        # otherwise return a high cost of 1000000 to discourage choosing this path
        return 2 if (grid[y1][x1] != 1 and grid[y2][x2] != 1) else 1000000

    # Check if moving down is a valid move
    elif x1 == x2 and y2 == y1 + 1:  # down
        # If moving down is valid, return a cost of 1 if neither node is blocked,
        # otherwise return a high cost of 1000000 to discourage choosing this path
        return 1 if (grid[y1][x1] != 1 and grid[y2][x2] != 1) else 1000000

    # If the move is not valid or not horizontal/vertical, return a high cost of 1000000
    else:
        return 1000000


# Define the function to calculate the Euclidean distance between two nodes
def euclidean_distance(node1, node2):
    # Extract the x and y coordinates of each node
    y1, x1 = node1
    y2, x2 = node2
    # Calculate the distance using the Euclidean formula
    distance = math.sqrt((y2-y1)**2 + (x2-x1)**2)
    return distance


#====================FILE HANDLING===================

#file handler to open the grid file
file_handle = open("grid.txt", mode="r")
if file_handle:
    print("\nSCANNING FILE FOR DATA...")
else:
    print("\nError: File Not Found!")

#-------------------Grid Size--------------------
#read first line to get the dimensions of the grid
data = file_handle.readline()
grid_sz_y = int(data[0])
grid_sz_x = int(data[2])

#check if the grid size is within constraints
if 1 < grid_sz_x < 8 and 1 < grid_sz_y < 8:
    print("\tGrid Size(Col x Row): ", grid_sz_y, "x", grid_sz_x)
else:
    print("\tError: Grid size out of bound!")

#---------------Starting Coordinates----------------
#read second line to get the starting coordinates
data = file_handle.readline()
start_y = int(data[0])
start_x = int(data[2])

#check if the coordinates are valid
if 0 <= start_x < grid_sz_x and 0 <= start_y < grid_sz_y:
    print("\tStarting Coordinates: (", start_y, ",", start_x, ")")
else:
    print("\tError: Invalid Starting Coordinates")

#---------------Ending Coordinates----------------
#read third line to get the ending coordinates
data = file_handle.readline()
end_y = int(data[0])
end_x = int(data[2])

#check if the coordinates are valid
if 0 <= end_x < grid_sz_x and 0 <= end_y < grid_sz_y:
    print("\tEnding Coordinates: (", end_y, ",", end_x, ")")
else:
    print("\tError: Invalid Starting Coordinates")

#---------------------Grid--------------------------
#read the rest of the file containing the grid
data = file_handle.readlines()
grid = []
#iterate through each line
for line in data:
    #strip each line and split it into each individual character and parse it as int and store it in the array 'row'
    row = [int(x) for x in line.strip().split()]
    #append the 2D array 'grid' with each created row
    grid.append(row)

print("\tGrid Data: ", grid)

#printing grid
print_grid(Grid=grid, Message="\nOriginal Grid:", Start_x=start_x, Start_y=start_y, End_x=end_x, End_y=end_y)



#====================================BREATH FIRST SEARCH===============================
print("\nAPPLYING BREATH FIRST SEARCH...")
# initialize the queue with the starting node and its cost/path, store it as a tuple
queue = Queue()
queue.put((start_y, start_x, 0, [(start_y, start_x)]))

# initialize an empty set to keep track of visited nodes and a flag to check if a path is found
visited = set()
path_found = False


while not queue.empty():  # iterate until the queue is empty or the path is found
    # get the current node from the queue
    current = queue.get()
    current_y, current_x, current_cost, current_path = current

    visited.add((current_y, current_x))  # mark the current node as visited

    if current_y == end_y and current_x == end_x:  # check if current node is the end node
        # if the end node is found, print the path and cost, set the flag to True, and break out of the loop
        print("\tPath found!")
        path_found = True
        print("\tPath: ", current_path)
        print("\tCost: ", current_cost)
        print_grid(Grid=grid, Message="\tGrid with Path using BFS:", Path=current_path, Start_x=start_x, Start_y=start_y, End_x=end_x, End_y=end_y)
        break


    for neighbor in get_neighbors((current_y, current_x)):  # generate child nodes and add to queue if they are valid and not visited
        neighbor_y, neighbor_x = neighbor
        if (neighbor_y, neighbor_x) not in visited:
            # add the child node to the queue with its updated cost/path
            if neighbor_x == current_x + 1:  # right
                queue.put((neighbor_y, neighbor_x, current_cost + 2, current_path + [(neighbor_y, neighbor_x)]))
            elif neighbor_y == current_y + 1:  # down
                queue.put((neighbor_y, neighbor_x, current_cost + 1, current_path + [(neighbor_y, neighbor_x)]))
            elif neighbor_x == current_x - 1:  # left
                queue.put((neighbor_y, neighbor_x, current_cost + 3, current_path + [(neighbor_y, neighbor_x)]))
            elif neighbor_y == current_y - 1:  # up
                queue.put((neighbor_y, neighbor_x, current_cost + 2, current_path + [(neighbor_y, neighbor_x)]))

# check if a path was not found
if not path_found:
    print("\tNo Path Found!")


#===========================A STAR SEARCH==========================
print("\nAPPLYING A* SEARCH...")

start = (start_y, start_x)
end = (end_y, end_x)

open_set = PriorityQueue()  # Initialize a priority queue to hold cells to be evaluated
open_set.put((0, start))  # Add the start cell to the queue with priority 0

came_from = {}  # Initialize a dictionary to keep track of each cell's parent in the path
cost_so_far = {}  # Initialize a dictionary to keep track of the cost to reach each cell
came_from[start] = None  # The start cell has no parent
cost_so_far[start] = 0  # The cost to reach the start cell is 0

while not open_set.empty():  # While there are still cells to be evaluated
    current = open_set.get()[1]  # Get the cell with the lowest priority value

    if current == end:  # If the current cell is the end cell, we have found the path
        break

    for neighbor in get_neighbors(current):  # Check each neighbor of the current cell
        new_cost = cost_so_far[current] + get_cost(current, neighbor)  # Calculate the cost to reach this neighbor
        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:  # If we haven't reached this neighbor before, or if this new cost is lower than the previous cost to reach it
            cost_so_far[neighbor] = new_cost  # Update the cost to reach this neighbor
            priority = new_cost + euclidean_distance(neighbor, end)  # Calculate the priority of this neighbor
            open_set.put((priority, neighbor))  # Add this neighbor to the queue with its priority
            came_from[neighbor] = current  # Update this neighbor's parent to be the current cell



if current == end:  #if the goal is reached
    # construct path
    path = []
    while current != start:  # loop until current position is equal to start position
        path.append(current)  # add current position to path list
        current = came_from[current]  # set current position to the position that led to it
    path.append(start)  # add start position to path list
    path.reverse()  # reverse the order of the path list (start to end)


    # print results
    print("\tPath found!")
    print("\tPath: ", path)
    print("\tCost: ", cost_so_far[end])
    print_grid(Grid=grid, Message="\tGrid with Path using A*:", Path=path, Start_x=start_x, Start_y=start_y,End_x=end_x, End_y=end_y)

else:
    print("\tNo Path Found!")
