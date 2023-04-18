import random, copy, time, sys, argparse


#Args parser for task 2
parser = argparse.ArgumentParser()
parser.add_argument('--explain', action='store_true', help='Print out a set of instructions for solving the Sudoku puzzle')
parser.add_argument('--hint', '-n', type=int, help='Return grid with N values filled in')
args = parser.parse_args()


'''
EDGE CASE: If a row contains only 0s then it will throw a NoneType error,
this is because the sum of the row is 0 so python returns that as False.
Its kinda weird and we can't do anything about it :/

CONFIRM: whether the grids will be 2x3 or 3x2 as this is a very important difference

FLAGS: To run flags you need to use gitbash. If you want to run the flag --explain for example,
you need to do 'python cw3.py --explain'
'''

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


def check_section(section, n):

	if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n+1)]):
		return True
	return False



def get_squares(grid, n_rows, n_cols):

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
	'''
	This function returns the index (i, j) to the first zero element in a sudoku grid
	If no such element is found, it returns None
	args: grid
	return: A tuple (i,j) where i and j are both integers, or None
	'''
	for i in range(len(grid)):
		row = grid[i]
		for j in range(len(row)):
			if grid[i][j] == 0:
				return (i, j)
	return None


def get_possible_values(grid,row,col,n,n_rows,n_cols):

	values_in_row = set(grid[row])
	values_in_col = set([grid[i][col] for i in range(n)])
	values_in_square = set([grid[i][j] for i in range(row//n_rows*n_rows,row//n_rows*n_rows+n_rows) for j in range(col//n_cols*n_cols,col//n_cols*n_cols+n_cols)])
	all_possible_values = set(range(1,n+1))
	return all_possible_values - values_in_row - values_in_col - values_in_square

def recursive_solve(grid, n_rows, n_cols, explain):
	"""
	Recursive Soduku solver by removing all possible values
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
			ans = recursive_solve(grid,n_rows,n_cols,args.explain)

			#If we've found a solution with this value then return it.
			if ans:
				if explain:
					print(f"Put {value} in location ({row+1}, {col+1})")
				return ans 

			#If we couldn't find a solution with this value then reset it and try another one.
			grid[row][col] = 0 


	#Return none to indicate that previous values are incorrect.
	return None



def solve(grid, n_rows, n_cols):
	return recursive_solve(grid, n_rows, n_cols, args.explain)



def hint(grid):
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

#THIS CAN NOW BE EDITTED
def main():

	points = 0

	if args.hint:
		hint(grid5)

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
			if check_solution(solution, n_rows, n_cols):
				print("grid %d correct" % (i+1))
				points = points + 10
			else:
				print("grid %d incorrect" % (i+1))

		print("====================================")
		print("Test script complete, Total points: %d" % points)



if __name__ == "__main__":
	main()