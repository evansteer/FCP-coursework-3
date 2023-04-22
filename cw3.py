import random, copy, time, argparse, random, copy
import matplotlib.pyplot as plt

#Args parser for task 2
parser = argparse.ArgumentParser()
parser.add_argument('--explain', action='store_true', 
		    help='Print out a set of instructions for solving the Sudoku puzzle')
parser.add_argument('--profile', action='store_true',
                    help='Measures the performance of the solver(s) in terms of time for grids of different size and difficulties')
parser.add_argument('--hint', type=int, help='Returns a grid with N values filled in')
parser.add_argument('-f', '--file', type=str, help='The path to the file containing the Sudoku grid.')
args = parser.parse_args()


#Grids 1-4 are 2x2
grid1 = [
		[1, 0, 4, 2],
		[4, 2, 1, 3],
		[2, 1, 3, 4],
		[3, 4, 2, 1]]

grid2 = [
		[1, 0, 4, 2],
		[4, 2, 1, 3],
		[2, 1, 0, 4],
		[3, 4, 2, 1]]

grid3 = [
		[1, 0, 4, 2],
		[4, 2, 1, 0],
		[2, 1, 0, 4],
		[0, 4, 2, 1]]

grid4 = [
		[1, 0, 4, 2],
		[0, 2, 1, 0],
		[2, 1, 0, 4],
		[0, 4, 2, 1]]

#Grids 4-7 are 3x3
grid5 = [
	[0, 0, 0, 0, 3, 0, 7, 0, 0],
	[0, 5, 0, 0, 0, 0, 0, 9, 0],
	[0, 0, 0, 0, 9, 0, 0, 0, 1],
	[1, 0, 0, 0, 7, 0, 4, 0, 0],
	[8, 0, 0, 0, 0, 0, 0, 0, 5],
	[0, 0, 7, 0, 6, 0, 0, 0, 0],
	[0, 0, 3, 0, 0, 0, 0, 0, 0],
	[0, 4, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 8, 0]]



grid6 = [
		[0, 0, 0, 0, 4, 2, 0, 0, 0],
		[7, 0, 5, 0, 6, 9, 0, 8, 2],
		[8, 3, 0, 0, 0, 0, 0, 0, 9],
		[1, 0, 0, 0, 9, 7, 0, 0, 4],
		[9, 6, 0, 0, 0, 0, 8, 0, 0],
		[0, 0, 3, 0, 8, 4, 6, 0, 1],
		[4, 0, 0, 9, 0, 6, 2, 0, 3],
		[0, 0, 1, 0, 2, 8, 0, 5, 0],
		[5, 0, 6, 0, 1, 0, 0, 4, 8]
		]

grid7 = [
		[6, 1, 9, 8, 4, 0, 0, 3, 7,],
		[7, 0, 5, 3, 6, 9, 1, 8, 2,],
		[8, 3, 0, 1, 7, 5, 4, 6, 9,],
		[1, 5, 8, 6, 9, 7, 3, 0, 4,],
		[9, 6, 4, 2, 3, 1, 8, 7, 5,],
		[2, 7, 0, 5, 8, 4, 6, 9, 1,],
		[4, 8, 7, 9, 5, 6, 2, 1, 3,],
		[3, 9, 1, 4, 2, 8, 0, 5, 6,],
		[5, 2, 6, 0, 1, 3, 9, 4, 8,]]

#grids 8-10 are 2x3
grid8 = [
		[0, 0, 6, 0, 0, 3],
		[5, 0, 0, 0, 0, 0],
		[0, 1, 3, 4, 0, 0],
		[0, 0, 0, 0, 0, 6],
		[0, 0, 1, 0, 0, 0],
		[0, 5, 0, 0, 6, 4]]

grid9 =[
		[0, 0, 6, 0, 0, 3],
		[5, 0, 0, 0, 0, 0],
		[0, 1, 3, 4, 0, 0],
		[0, 0, 0, 0, 0, 6],
		[0, 0, 1, 0, 0, 0],
		[0, 5, 0, 0, 6, 4]]

grid10 = [
		[1, 0, 6, 5, 4, 3],
		[5, 0, 4, 6, 2, 1],
		[6, 1, 3, 0, 5, 2],
		[2, 4, 5, 3, 1, 6],
		[4, 6, 1, 2, 3, 5],
		[3, 5, 2, 1, 6, 4]]


grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), 
		 (grid5, 3, 3), (grid6,3,3), (grid7, 3, 3), 
		 (grid8, 2, 3), (grid9, 2, 3), (grid10, 2, 3)]

explanation = []

def check_section(section, n):
	"""
    Check if the given section is valid for a partition of n.

    Args:
    section (list): A list of integers representing a section of the partition.
    n (int): An integer representing the total number being partitioned.

    Returns:
    bool: True if the section is valid, False otherwise.
    """
	if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n+1)]):
		return True
	return False




def get_squares(grid, n_rows, n_cols):
	"""
    Returns a list of all the square sub-grids of the given size in the given grid.
    
    Args:
    - grid (list): A 2D list representing the grid.
    - n_rows (int): The number of rows in each square sub-grid.
    - n_cols (int): The number of columns in each square sub-grid.
    
    Returns:
    - squares (list): A list of all the square sub-grids in the grid, represented as 1D lists.
    """
	squares = []
	for i in range(n_cols):
		rows = (i*n_rows, (i+1)*n_rows)
		for j in range(n_rows):
			cols = (j*n_cols, (j+1)*n_cols)
			square = []
			for k in range(rows[0], rows[1]):
				line = grid[k][cols[0]:cols[1]]
				square +=line
			squares.append(square)

	return(squares)




def check_solution(grid, n_rows, n_cols):
	"""
    Checks if a given grid is a valid solution to a Sudoku puzzle.

    Args:
    - grid (List[List[int]]): a 2D list representing the grid to be checked
    - n_rows (int): the number of rows in each sub-grid
    - n_cols (int): the number of columns in each sub-grid

    Returns:
    - bool: True if the grid is a valid solution, False otherwise
    """
	n = n_rows*n_cols
	
	print(grid)
	for row in grid:
		if check_section(row, n) == False:
			return False

	for i in range(n):
		column = []
		for row in grid:
			column.append(row[i])

		if check_section(column, n) == False:
			return False

	squares = get_squares(grid, n_rows, n_cols)
	for square in squares:
		if check_section(square, n) == False:
			return False

	return True



def find_empty(grid):
    """
    Returns the coordinates of the next empty cell (with a value of 0) in the grid, in the form of a tuple (row, col). 
    If there are no empty cells, returns None.

    Args:
    - grid (List[List[int]]): a 2D list representing the grid to be checked
    
    Returns:
    - A tuple containing the row and column coordinates of the next empty cell, or None if there are no empty cells.
    """
    
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if grid[i][j] == 0:
                return (i, j)
    return None



def get_possible_values(grid,row,col,n,n_rows,n_cols):
    """
    Get the possible values that can be assigned to a given cell in the grid.

    Args:
        grid (list): A 2D list representing the Sudoku grid.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        n (int): The maximum value that can be assigned to a cell.
        n_rows (int): The number of rows in each square of the grid.
        n_cols (int): The number of columns in each square of the grid.

    Returns:
        set: A set of integers representing the possible values that can be assigned
             to the given cell without violating the rules of Sudoku.
    """
    
    values_in_row = set(grid[row])
    values_in_col = set([grid[i][col] for i in range(n)])
    values_in_square = set([grid[i][j] for i in range(row//n_rows*n_rows,row//n_rows*n_rows+n_rows) for j in range(col//n_cols*n_cols,col//n_cols*n_cols+n_cols)])
    all_possible_values = set(range(1,n+1))
    return all_possible_values - values_in_row - values_in_col - values_in_square



def recursive_solve(grid, n_rows, n_cols, explain, hint, depth):
	"""
    Recursively solves a Sudoku puzzle using backtracking algorithm.

    Args:
        grid (list): A 2D list representing the Sudoku puzzle.
        n_rows (int): The number of rows in each square.
        n_cols (int): The number of columns in each square.
        explain (bool): A boolean flag to indicate whether to print the steps to solve the puzzle.
        hint (int or None): An integer value indicating the maximum depth of recursion to print steps.
        depth (int): The depth of recursion.

    Returns:
        list or None: A 2D list representing the solved Sudoku puzzle or None if there is no solution.

    """
	#N is the maximum integer considered in this board
	n = n_rows*n_cols
	#Find an empty place in the grid
	empty = find_empty(grid)

	#If there's no empty places left, check if we've found a solution
	if not empty:
		#If the solution is correct, return it.
		if check_solution(grid, n_rows, n_cols):
			return grid 
		else:
			#If the solution is incorrect, return None
			return None
	else:
		row, col = empty 

	#Get possible values for this cell based on its row/column/square values.
	possible_values = get_possible_values(grid,row,col,n,n_rows,n_cols)

	# Loop through possible values for this cell.
	for value in possible_values:

			#Place the value into the grid
			grid[row][col] = value
	
			#Recursively solve the grid with this new value.
			ans = recursive_solve(grid,n_rows,n_cols, explain, hint, depth+1)

			#If we've found a solution with this value then return it.
			if ans:
				if explain and hint is None:
					print(f"Put {value} in location ({row+1}, {col+1})")
					explanation.append(f"Put {value} in location ({row+1}, {col+1})")
				elif explain and hint is not None and depth <= hint:
					print(f"Put {value} in location ({row + 1}, {col + 1})")
					explanation.append(f"Put {value} in location ({row + 1}, {col + 1})")
				
				if hint is not None and depth > hint:
					ans[row][col] = 0
				
				return ans 

			#If we couldn't find a solution with this value then reset it and try another one.
			grid[row][col] = 0 


	#Return none to indicate that previous values are incorrect.
	return None

def solve(grid, n_rows, n_cols):
	"""
    Solves a Sudoku puzzle by calling the recursive_solve function with initial depth of 1.

    Args:
    - grid (list of lists): The Sudoku puzzle grid as a 2D list of integers. Empty cells are represented by 0.
    - n_rows (int): The number of rows in each square block.
    - n_cols (int): The number of columns in each square block.

    Returns:
    - A solved Sudoku puzzle grid as a 2D list of integers, or None if no solution was found.

    """
		
    # We set the minimun value of depth as 1
	return recursive_solve(grid, n_rows, n_cols, args.explain, args.hint, 1)



# The function calls two other functions
def measure_performance():
    """
    Runs performance measurements for the Sudoku solver. 
    This function compares the solver's performance using different grid sizes and difficulty levels.

    Args:
        None

    Returns:
        None
    """
 
    print("Running performance measurement")
    print("====================================\n")
    compare_different_size()
    compare_different_difficulty()



def compare_different_size():
    """
    Compare the performance of sudoku solvers in terms of time for grids of different sizes.

    This function measures the time taken to solve 100 instances of each grid size (2x2, 3x2, 3x3) using the 
    'solve' function. The elapsed time for each run is added to a corresponding list ('time_for_2x2', 
    'time_for_3x2', or 'time_for_3x3'), and the average time for each grid size is calculated. A bar graph is 
    then plotted with grid size on the x-axis and average time on the y-axis.

    Args:
        None

    Returns:
        None
    """
 
    print("\nMeasuring the performance of solvers in terms of time for grids of different size")
    print("====================================")
    # For grids of size 2x2, the elapsed time for each run is added to time_for_2x2 list
    time_for_2x2 = []
    # For grids of size 3x2, the elapsed time is added to time_for_3x2 list
    time_for_3x2 = []
    # For grids of size 3x3, the elapsed time is added to time_for_3x3 list
    time_for_3x3 = []

    for (i, (grid, n_rows, n_cols)) in enumerate(grids):
        if i in [0, 1, 2, 3]:
            # We run these codes 100 times to get average value
            for _ in range(100):
                start_time = time.time()
                solve(grid, n_rows, n_cols)
                elapsed_time = time.time() - start_time
                time_for_2x2.append(elapsed_time)
        elif i in [4, 5, 6]:
            for _ in range(100):
                start_time = time.time()
                solve(grid, n_rows, n_cols)
                elapsed_time = time.time() - start_time
                time_for_3x3.append(elapsed_time)
        else:
            for _ in range(100):
                start_time = time.time()
                solve(grid, n_rows, n_cols)
                elapsed_time = time.time() - start_time
                time_for_3x2.append(elapsed_time)

    avg_time_for_2x2 = sum(time_for_2x2) / len(time_for_2x2)
    avg_time_for_3x2 = sum(time_for_3x2) / len(time_for_3x2)
    avg_time_for_3x3 = sum(time_for_3x3) / len(time_for_3x3)

    plt.bar(["2x2", "3x2", "3x3"], [avg_time_for_2x2, avg_time_for_3x2, avg_time_for_3x3])
    plt.xlabel("Grid Size")
    plt.ylabel("Average Time")
    plt.title("the performance of solvers in terms of time for grids of different size")
    plt.show()


def compare_different_difficulty():
    """
    Measures the performance of the `solve` function in terms of time for grids of different difficulties.

    Args: 
        None
    
    Returns:
        None
    """
 
    print("\nMeasuring the performance of solvers in terms of time for grids of different difficulties")
    print("====================================")
    grid = [[6, 1, 9, 8, 4, 2, 5, 3, 7, ],
            [7, 4, 5, 3, 6, 9, 1, 8, 2, ],
            [8, 3, 2, 1, 7, 5, 4, 6, 9, ],
            [1, 5, 8, 6, 9, 7, 3, 2, 4, ],
            [9, 6, 4, 2, 3, 1, 8, 7, 5, ],
            [2, 7, 3, 5, 8, 4, 6, 9, 1, ],
            [4, 8, 7, 9, 5, 6, 2, 1, 3, ],
            [3, 9, 1, 4, 2, 8, 7, 5, 6, ],
            [5, 2, 6, 7, 1, 3, 9, 4, 8, ]]
    # We crean empty dictionary dic to store the elapsed time for each difficulty level
    dic = {}
    # For each difficulty level (increasing from 1 to 60)
    for i in range(60):
        # The unfilled location increasing by one after this code is run once
        num_of_unfilled_locations = i+1
        # It randomly selects a location in the grid that is not already empty, empties it
        dic[num_of_unfilled_locations] = []
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while grid[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        grid[row][col] = 0
        grid_copy = copy.deepcopy(grid)
        # We runs the solver 100 times
        for _ in range(100):
            start_time = time.time()
            solve(grid_copy, 3, 3)
            elapsed_time = time.time() - start_time
            # It stores the elapsed time in the corresponding list in dic
            dic[num_of_unfilled_locations].append(elapsed_time)

    num_of_unfilled_locations_list = []
    # The average elapsed time for each difficulty level is stored in avg_elapsed_time_list
    avg_elapsed_time_list = []

    for num_of_unfilled_locations, elapsed_time_list in dic.items():
        num_of_unfilled_locations_list.append(num_of_unfilled_locations)
        avg_elapsed_time = sum(elapsed_time_list) / len(elapsed_time_list)
        avg_elapsed_time_list.append(avg_elapsed_time)
        
    # It plots a bar chart showing the average elapsed time for each difficulty level
    plt.bar(num_of_unfilled_locations_list, avg_elapsed_time_list)
    plt.xlabel("Number of Unfilled Locations")
    plt.ylabel("Average Time")
    plt.title("the performance of solvers in terms of time for grids of different difficulties (specified by number of unfilled locations)")
    plt.show()



def hint(grid):
    """
    Generates a hint for the user by randomly filling in N empty cells in the given Sudoku grid.

    Args:
    - grid (list): A 2D list representing the Sudoku grid.

    Returns:
    None. Prints the hint grid, which is a copy of the original grid with N cells filled in with valid values.
    """
 
    # make a copy of the grid
    hint_grid = copy.deepcopy(grid)
    # randomly choose N cells to fill in
    cells = random.sample([(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0], args.hint)
    for cell in cells:
        # fill in the cell with a random valid value
        row, col = cell
        values = [i for i in range(1, 5) if check_solution(hint_grid, row, col)]
        hint_grid[row][col] = random.choice(values)
    # print the hint grid
    for row in hint_grid:
        print(row)


def wavefront_present_values(grid, row, col):
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    square = []
    
    for i in range(3):
        for j in range(3):
            if str(grid[box_row + i][box_col + j]).isnumeric() and grid[box_row + i][box_col + j] > 0:
                square.append(grid[box_row + i][box_col + j])
    
    row_values = [i for i in str(grid[row]) if (i.isnumeric())]
    row_values = [j for j in row_values if int(j) > 0]
    row_values = [int(k) for k in row_values]
    
    column = []
    for i in range(9):
        if str(grid[i][col]).isnumeric() and grid[i][col] > 0:
            column.append(grid[i][col])
            
            
    present_values =[]
    
    for i in row_values:
        present_values.append(i)
        
    for j in column:
        if j not in present_values:
            present_values.append(j)
            
    for k in square:
        if k not in present_values:
            present_values.append(k)
    
    return present_values


def wavefront_amend_lists(grid):
    all_values = [1,2,3,4,5,6,7,8,9]
    
    for row in range(9):
        for col in range(9):
            test = isinstance(grid[row][col], list)
            no_values = present_values(grid, row, col)
            if test == True:
                allow_values = [i if i not in no_values else None for i in all_values]
                for i in allow_values:
                    if str(i).isnumeric():
                        grid[row][col] = i
    
    return grid
        


def wavefront_fill_cells(grid):
    all_values = [1,2,3,4,5,6,7,8,9]

    for row in range(9):
        for col in range(9):
            no_values = present_values(grid, row, col)
            if grid[row][col] == 0:
                allow_values = [i if i not in no_values else None for i in all_values]
                for i in allow_values:
                    if str(i).isnumeric():
                        grid[row][col] = i
    return grid


def wavefront_solve(grid):
    fill_cells(grid)
    
    for row in range(9):
        for column in range(9):
            test =  isinstance(grid[row][column], list)
            if test == True and len(grid[row][column]) == 1:
                grid[row][column] = (grid[row][column])[0]
                amend_lists(grid)
                
    for rows in grid:
        second_test = any(isinstance(elements, list) for elements in rows)
        if second_test == True:
            solve(grid)
        else:
            return grid
                   
    return None



def main():

	# initialize points counter
	points = 0
	
	# if --hint flag is used, print a hint for grid5
	if args.hint:
		hint(grid5)

	# if --file flag is used, read the grid from file
	if args.file:
		with open(args.file, 'r') as f:
			lines = f.readlines()
			grid = [[int(num) for num in line.split()] for line in lines]
		
		# set number of rows and columns for the grid
		num_rows = 3
		num_cols = 3

		# solve the grid
		solution = solve(grid, num_rows, num_cols)

		# save the solution to file
		with open('OUTPUT.txt', 'w') as f:
			for row in solution:
				f.write(' '.join(str(num) for num in row) + '\n')

		# save the explanation to file if --explain flag is used
		if args.explain:
			with open('OUTPUT.txt', 'a') as f:
				for i in range(len(explanation)):
					f.write(explanation[i])
					f.write("\n")

	# if --profile flag is used, measure the performance of the solve function
	elif args.profile:
		measure_performance()

	# if no flags are used, run the test script on all grids
	else:

		print("Running test script for coursework 1")
		print("====================================")
	
		for (i, (grid, n_rows, n_cols)) in enumerate(grids):
			print("Solving grid: %d" % (i+1))
			start_time = time.time()
			solution = solve(grid, n_rows, n_cols)
			elapsed_time = time.time() - start_time
			print("Solved in: %f seconds" % elapsed_time)
			print(solution)
			# check if the solution is correct and update points counter
			if check_solution(solution, n_rows, n_cols):
				print("grid %d correct" % (i+1))
				points = points + 10
			else:
				print("grid %d incorrect" % (i+1))

		print("====================================")
		print("Test script complete, Total points: %d" % points)



if __name__ == "__main__":
	main()
