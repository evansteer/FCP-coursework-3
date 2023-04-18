

def present_values(grid, row, col):
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


def amend_lists(grid):
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
        


def fill_cells(grid):
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

def solve(grid):
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

print(solve([
        [6, 1, 9, 8, 4, 0, 0, 3, 7,],
		[7, 0, 5, 3, 6, 9, 1, 8, 2,],
		[8, 3, 0, 1, 7, 5, 4, 6, 9,],
		[1, 5, 8, 6, 9, 7, 3, 0, 4,],
		[9, 6, 4, 2, 3, 1, 8, 7, 5,],
		[2, 7, 0, 5, 8, 4, 6, 9, 1,],
		[4, 8, 7, 9, 5, 6, 2, 1, 3,],
		[3, 9, 1, 4, 2, 8, 0, 5, 6,],
		[5, 2, 6, 0, 1, 3, 9, 4, 8,]]))
print(solve([
		[0, 1, 7, 8, 4, 2, 5, 3, 9,],
		[7, 4, 5, 3, 6, 9, 0, 8, 2,],
		[8, 3, 2, 1, 7, 5, 4, 6, 9,],
		[1, 5, 8, 6, 9, 7, 3, 2, 4,],
		[9, 6, 4, 0, 3, 1, 0, 7, 5,],
		[2, 7, 3, 5, 8, 4, 6, 9, 1,],
		[4, 8, 7, 9, 0, 6, 2, 0, 3,],
		[3, 9, 1, 4, 2, 8, 7, 5, 6,],
		[5, 2, 6, 7, 1, 0, 9, 4, 8,]]))

