import random, copy, time, argparse, random, copy, statistics
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

wavefront = False

#Easy grids 1-3
grid1 = [
	[9, 0, 6, 0, 0, 1, 0, 4, 0],
	[7, 0, 1, 2, 9, 0, 0, 6, 0],
	[4, 0, 2, 8, 0, 6, 3, 0, 0],
	[0, 0, 0, 0, 2, 0, 9, 8, 0],
	[6, 0, 0, 0, 0, 0, 0, 0, 2],
	[0, 9, 4, 0, 8, 0, 0, 0, 0],
	[0, 0, 3, 7, 0, 8, 4, 0, 9],
	[0, 4, 0, 0, 1, 3, 7, 0, 6],
	[0, 6, 0, 9, 0, 0, 1, 0, 8]]

grid2 = [
	[0, 0, 0, 2, 6, 0, 7, 0, 1],
	[6, 8, 0, 0, 7, 0, 0, 9, 0],
	[1, 9, 0, 0, 0, 4, 5, 0, 0],
	[8, 2, 0, 1, 0, 0, 0, 4, 0],
	[0, 0, 4, 6, 0, 2, 9, 0, 0],
	[0, 5, 0, 0, 0, 3, 0, 2, 8],
	[0, 0, 9, 3, 0, 0, 0, 7, 4],
	[0, 4, 0, 0, 5, 0, 0, 3, 6],
	[7, 0, 3, 0, 1, 8, 0, 0, 0]]

grid3 = [
		[0, 3, 0, 4, 0, 0],
		[0, 0, 5, 6, 0, 3],
		[0, 0, 0, 1, 0, 0],
		[0, 1, 0, 3, 0, 5],
		[0, 6, 4, 0, 3, 1],
		[0, 0, 1, 0, 4, 6]]


#Meadium grids 4-5
grid4 = [
	[0, 0, 0, 6, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 5, 0, 1],
	[3, 6, 9, 0, 8, 0, 4, 0, 0],
	[0, 0, 0, 0, 0, 6, 8, 0, 0],
	[0, 0, 0, 1, 3, 0, 0, 0, 9],
	[4, 0, 5, 0, 0, 9, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 3, 0, 0],
	[0, 0, 6, 0, 0, 7, 0, 0, 0],
	[1, 0, 0, 3, 4, 0, 0, 0, 0]]



grid5 = [
		[8, 0, 9, 0, 2, 0, 3, 0, 0],
		[0, 3, 7, 0, 6, 0, 5, 0, 0],
		[0, 0, 0, 4, 0, 9, 7, 0, 0],
		[0, 0, 2, 9, 0, 1, 0, 6, 0],
		[1, 0, 0, 3, 0, 6, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 3],
		[7, 0, 0, 0, 0, 0, 0, 0, 8],
		[5, 0, 0, 0, 0, 0, 0, 1, 4],
		[0, 0, 0, 2, 8, 4, 6, 0, 5]
		]

#Hard grid 6
grid6 = [
		[0, 2, 0, 0, 0, 0, 0, 1, 0],
		[0, 0, 6, 0, 4, 0, 0, 0, 0],
		[5, 8, 0, 0, 9, 0, 0, 0, 3],
		[0, 0, 0, 0, 0, 3, 0, 0, 4],
		[4, 1, 0, 0, 8, 0, 6, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 9, 5],
		[2, 0, 0, 0, 1, 0, 0, 8, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 3, 1, 0, 0, 8, 0, 5, 7]]



grids = [(grid1, 3, 3), (grid2, 3, 3), (grid3, 2, 3), (grid4, 3, 3), 
		 (grid5, 3, 3), (grid6,3,3)]

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
	time.sleep(0)	
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
	
	compare_different_difficulty()



def compare_different_difficulty():
	"""
	Compare the performance of sudoku solvers in terms of time for grids of different levels of difficulty.

	This function measures the time taken to solve 100 instances of each grid difficulty (easy, medium, hard) using the 
	'solve' function. The elapsed time for each run is added to a corresponding list ('time_for_easygrid', 
	'time_for_mediumgrid2', or 'time_for_hardgrid'), and the average time for each grid size is calculated. A bar graph is 
	then plotted with grid size on the x-axis and average time on the y-axis.

	Args:
		None

	Returns:
		None
	"""
 
	print("\nMeasuring the performance of solvers in terms of time for grids of different difficulty")
	print("====================================")
	# For easy grids, the elapsed time for each run is added to time_for_easygrid list
	time_for_easygrid = []
	# For medium grids, the elapsed time is added to time_for_mediumgrid list
	time_for_mediumgrid = []
	# For hard grids, the elapsed time is added to time_for_hardgrid list
	time_for_hardgrid = []

	for (i, (grid, n_rows, n_cols)) in enumerate(grids):
		if i in [0, 1, 2]:
			# We run these codes 100 times to get average value
			for _ in range(100):
				start_time = time.time()
				solve(grid, n_rows, n_cols)
				elapsed_time = time.time() - start_time
				time_for_easygrid.append(elapsed_time)
		elif i in [3,4]:
			for _ in range(100):
				start_time = time.time()
				solve(grid, n_rows, n_cols)
				elapsed_time = time.time() - start_time
				time_for_mediumgrid.append(elapsed_time)
		else:
			for _ in range(100):
				start_time = time.time()
				solve(grid, n_rows, n_cols)
				elapsed_time = time.time() - start_time
				time_for_hardgrid.append(elapsed_time)

	avg_time_for_easygrid = sum(time_for_easygrid) / len(time_for_easygrid)
	avg_time_for_mediumgrid = sum(time_for_mediumgrid) / len(time_for_mediumgrid)
	avg_time_for_hardgrid = sum(time_for_hardgrid) / len(time_for_hardgrid)

	plt.bar(["Easy grids", "Meadium grids", "Hard grid"], [avg_time_for_easygrid, avg_time_for_mediumgrid, avg_time_for_hardgrid])
	plt.xlabel("Grid Difficulty")
	plt.ylabel("Average Time")
	plt.title("The performance of the normal solver in terms of time for grids of different level of difficulty")
	plt.show()


#Below all relate to the wavefront algorithm

def wavefront_present_values(grid, row, col, rows, cols): 
	'''
	Function returning the values present in each row column and square of
	a given element of the sudoku grid.
	   
	'''
	#Use of if statements to decide how to allocate the dimensions of subsquares in the sudoku grid based on the dimensions of the sudoku grid
	if rows < 9:
		row_divisor, row_multiplier = 2, 2
	else:
		row_divisor, row_multiplier = 3, 3
	if cols < 6:
		cols_divisor, cols_multiplier = 2, 2
	else:
		cols_divisor, cols_multiplier = 3, 3

	box_row = (row // row_divisor) * row_multiplier #Uses remainder division and multiplication to attain the list indicies squares and thus detect the values in a square
	box_col = (col // cols_divisor) * cols_multiplier
	square = []
	
	for i in range(row_divisor):
		for j in range(cols_divisor):
			if str(grid[box_row + i][box_col + j]).isnumeric() and grid[box_row + i][box_col + j] > 0:
				square.append(grid[box_row + i][box_col + j])  #casts the elements in the square as string to be able to test if they are numeric and above zero
	
	row_values = [i for i in str(grid[row]) if (i.isnumeric())]
	row_values = [j for j in row_values if int(j) > 0]
	row_values = [int(k) for k in row_values] #casts the values in the targetted row as string to be able to test if they are numeric instead of list
	# then tests if the numbers are greater than zero before casting back to integers
	
	column = []
	for i in range(9):
		if str(grid[i][col]).isnumeric() and grid[i][col] > 0: #cast to string for same reason as for square and row
			column.append(grid[i][col])
			
			
	wavefront_present_values =[]
	
	for i in row_values:
		wavefront_present_values.append(i)
		
	for j in column:
		if j not in wavefront_present_values:
			wavefront_present_values.append(j)
			
	for k in square:
		if k not in wavefront_present_values:
			wavefront_present_values.append(k) #adds all value in row, col and square to present values if they are not already there
	
	return wavefront_present_values


def wavefront_amend_lists(grid, row, col, value, rows, cols):
	'''
	Function to amend the lists of available numbers for unfilled elements 
	in the sudoku grid after an element has been filled
	Returns the amended grid
	Uses isinstance() to test for the presence of nested lists, indicating an unfilled element
	to be amended
	'''
	for amend_row in grid[row]:
		list_test = isinstance(amend_row, list)
		if list_test == True and (value in amend_row):
			amend_row.remove(value)
			
	for amend_col in range(rows):
		list_test2 = isinstance(grid[amend_col][col], list)
		if list_test2 == True and (value in grid[amend_col][col]):
			grid[amend_col][col].remove(value)
			
	if rows < 9:
		row_divisor, row_multiplier = 2, 2
	else:
		row_divisor, row_multiplier = 3, 3
        
	if cols < 6:
		cols_divisor, cols_multiplier = 2, 2
	else:
		cols_divisor, cols_multiplier = 3, 3
        
	box_row = (row // row_divisor) * row_multiplier #repeat of technique used in present_values function to attain the values in a square
	box_col = (col // cols_divisor) * cols_multiplier
	square = []
	
	for i in range(row_divisor):
		for j in range(cols_divisor):
			if str(grid[box_row + i][box_col + j]).isnumeric() and grid[box_row + i][box_col + j] > 0:
				square.append(grid[box_row + i][box_col + j])
				
	for amend_square in square:
		list_test3 = isinstance(amend_square, list)
		if list_test3 == True and (value in amend_square):
			amend_square.remove(value)
			
	return grid        


def wavefront_fill_cells(grid, rows, cols):
	'''
	Function used to fill all elements that display '0' 
	of the initially entered sudoku list with the numbers that are able to be entered into that element
	Uses the wavefront_present_values() function to do this
	Returns the amended sudoku grid
	'''
	if rows == 9:
		values = [1,2,3,4,5,6,7,8,9]#initial list of all possible values, depending on dimensions of the sudoku grid
	elif rows == 6:
		values = [1,2,3,4,5,6]
	elif rows == 4:
		values = [1,2,3,4]
	empties = [] #contains the lists of values that are able to be entered into each empty element
	counter = 0
	
	for row in range(rows):
		for col in range(cols):
			if grid[row][col] == 0:
				not_allowed = wavefront_present_values(grid, row, col, rows, cols)
				for i in not_allowed:
					if i in values:
						values.remove(i) #removes values from the list of all possible values if they are already present in the row, col or square
				empties.append(values)
				if rows == 9:
					values = [1,2,3,4,5,6,7,8,9]
				elif rows == 6:
					values = [1,2,3,4,5,6]
				elif rows == 4:
					values = [1,2,3,4]
				
	for row in range(rows):
		for col in range(cols):
			if grid[row][col] == 0:
				grid[row][col] = empties[counter]
				counter += 1
	
	return grid

def wavefront_smallest_empty(grid, rows, cols):
	smallest = [1,2,3,4,5,6,7,8,9]
	
	for row in range(rows):
		for col in range(cols):
			test = isinstance(grid[row][col], list)
			if test == True and len(grid[row][col]) == 0:
				return grid              
			elif test == True and len(grid[row][col]) < len(smallest):
				smallest = grid[row][col]
				smallest_row, smallest_col = row, col

	grid[smallest_row][smallest_col] = random.choice(smallest)
	wavefront_amend_lists(grid, smallest_row, smallest_col, grid[smallest_row][smallest_col], rows, cols)
	
	return grid
	

def wavefront_is_solved(grid):
	for row in grid:
		test = any(isinstance(element, list) for element in row)
		if test == True:
			return False
	return True
			

def wavefront_solve(grid):
	'''
	Main function to solve the initally sudoku grid that is entered 
	''' 
	rows = len(grid) #finds the number of rows and collumns in the grid
	cols = len(grid[0])
	wavefront_fill_cells(grid, rows, cols) #fills all cells containing 0 with a list of numbers that are possible to be placed 
	attempts = 0
	
	while attempts < 200:
		attempts += 1
		
		for i in range(9):
			for row in range(rows):
				for col in range(cols):
					list_test = isinstance(grid[row][col], list)
					if list_test == True and len(grid[row][col]) == 1:
						grid[row][col] = (grid[row][col])[0]
						wavefront_amend_lists(grid, row, col, grid[row][col], rows, cols)
		
		
		if wavefront_is_solved(grid) == False:
			wavefront_smallest_empty(grid, rows, cols)
		elif wavefront_is_solved(grid) == True:
			return grid  
			
	print("Failed Attempt")
	print(grid)
	
	time.sleep(1)

	
			
	return None         

def main():

	# initialize points counter
	algorithm = input("Which algorithm do you want to use? Wavefront: W, Normal: N \n").upper()
	if algorithm == "W":
		wavefront = True
	else:
		wavefront = False

	

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

		if wavefront:
			wavefront_times = []
			normal_times = []
			for (i, (grid, n_rows, n_cols)) in enumerate(grids):				
					# measure the solving time for normal solver
						start_time = time.time()
						result = solve(grid, n_rows, n_cols)
						end_time = time.time()
						final_time = float(end_time - start_time)
						print("Wavefront solver solving time:", final_time)
						wavefront_times.append(final_time)

			for (i, (grid, n_rows, n_cols)) in enumerate(grids):
				start_time = time.time()
				solution = solve(grid, n_rows, n_cols)
				end_time = time.time()
				final_time = float(end_time - start_time)
				print("Normal solver solving time:", final_time)
				normal_times.append(final_time)

			print("====================================")
			print("Wavefront solving times: ", wavefront_times)
			print("Mean solving time for the Wavefront algorithm: ", statistics.mean(wavefront_times))
			print("\n")
			print("Normal solving times: ", normal_times)
			print("Mean solving time for the Normal algorithm: ", statistics.mean(normal_times))
		else:
			measure_performance()

	# if no flags are used, run the test script on all grids
	else:
		if wavefront == True:
				print("====================================")
				print("Solving grid 1")
				start_time = time.time()
				print(wavefront_solve(grid1))
				elapsed_time = time.time() - start_time
				print("Solved in: %f seconds" % elapsed_time)

				print("Solving grid 2")
				start_time = time.time()
				print(wavefront_solve(grid2))
				elapsed_time = time.time() - start_time
				print("Solved in: %f seconds" % elapsed_time)

		if wavefront == False:
			print("====================================")
			for (i, (grid, n_rows, n_cols)) in enumerate(grids):
				if args.hint:
					print("Hint for grid ", i)
					solution = solve(grid, n_rows, n_cols)
				if args.hint is None:
					print("Solving grid: %d" % (i+1))
					start_time = time.time()
					solution = solve(grid, n_rows, n_cols)
					elapsed_time = time.time() - start_time
					print("Solved in: %f seconds" % elapsed_time)
					print(solution)
					# check if the solution is correct and update points counter
					if check_solution(solution, n_rows, n_cols):
						print("grid %d correct" % (i+1))
					else:
						print("grid %d incorrect" % (i+1))

			print("====================================")
			print("Script complete")



if __name__ == "__main__":
	main()