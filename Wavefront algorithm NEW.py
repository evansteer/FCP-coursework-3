import random

def present_values(grid, row, col): 
    '''
    Function returning the values present in each row column and square of
    a given element of the sudoku grid.
       
    '''
    box_row = (row // 3) * 3  #(not finished) Uses remainder division to split the 9x9 sudoku grid into a 3x3 grid of 3x3 squares
    box_col = (col // 3) * 3
    square = []
    
    for i in range(3):
        for j in range(3):
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
            
            
    present_values =[]
    
    for i in row_values:
        present_values.append(i)
        
    for j in column:
        if j not in present_values:
            present_values.append(j)
            
    for k in square:
        if k not in present_values:
            present_values.append(k) #adds all value in row, col and square to present values if they are not already there
    
    return present_values


def amend_lists(grid, row, col, value):
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
            
    for amend_col in range(9):
        list_test2 = isinstance(grid[amend_col][col], list)
        if list_test2 == True and (value in grid[amend_col][col]):
            grid[amend_col][col].remove(value)
            
    box_row = (row // 3) * 3 #repeat of technique used in present_values function to attain the values in a square
    box_col = (col // 3) * 3
    square = []
    
    for i in range(3):
        for j in range(3):
            if str(grid[box_row + i][box_col + j]).isnumeric() and grid[box_row + i][box_col + j] > 0:
                square.append(grid[box_row + i][box_col + j])
                
    for amend_square in square:
        list_test3 = isinstance(amend_square, list)
        if list_test3 == True and (value in amend_square):
            amend_square.remove(value)
            
    return grid        


def fill_cells(grid):
    '''
    Function used to fill all elements that display '0' 
    of the initially entered sudoku list with the numbers that are able to be entered into that element
    Uses the present_values() function to do this
    Returns the amended sudoku grid
    '''
    values = [1,2,3,4,5,6,7,8,9] #initial list of all possible values
    empties = [] #contains the lists of values that are able to be entered into each empty element
    counter = 0
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                not_allowed = present_values(grid, row, col)
                for i in not_allowed:
                    if i in values:
                        values.remove(i) #removes values from the list of all possible values if they are already present in the row, col or square
                empties.append(values)
                values = [1,2,3,4,5,6,7,8,9]
                
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                grid[row][col] = empties[counter]
                counter += 1
    
    return grid

def smallest_empty(grid):
    smallest = [1,2,3,4,5,6,7,8,9]
    
    for row in range(9):
        for col in range(9):
            test = isinstance(grid[row][col], list)
            if test == True and len(grid[row][col]) == 0:
                return grid              
            elif test == True and len(grid[row][col]) < len(smallest):
                smallest = grid[row][col]
                smallest_row, smallest_col = row, col

    grid[smallest_row][smallest_col] = random.choice(smallest)
    amend_lists(grid, smallest_row, smallest_col, grid[smallest_row][smallest_col])
    
    return grid
    

def is_solved(grid):
    for row in grid:
        test = any(isinstance(element, list) for element in row)
        if test == True:
            return False
    return True

def is_unsolved(grid):
    for row in range(9):
        for col in range(9):
            test = isinstance(grid[row][col], list)
            if test == True and len(grid[row][col]) == 0:
                return True
            
    return False
            

def solve(grid):
    '''
    Main function to solve the initally sudoku grid that is entered 
    ''' 
    fill_cells(grid) #fills all cells containing 0 with a list of numbers that are possible to be placed 
    attempts = 0
    
    while attempts < 200:
        attempts += 1
        
        for i in range(9):
            for row in range(9):
                for col in range(9):
                    list_test = isinstance(grid[row][col], list)
                    if list_test == True and len(grid[row][col]) == 1:
                        grid[row][col] = (grid[row][col])[0]
                        amend_lists(grid, row, col, grid[row][col])
        
        
        if is_solved(grid) == False:
            smallest_empty(grid)
        elif is_solved(grid) == True:
            return grid  
            
    print("Failed Attempt")
    print(grid)
    
    
    
            
    return None         
                
    



print(solve([[0, 0, 0, 6, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 5, 0, 1],
             [3, 6, 9, 0, 8, 0, 4, 0, 0],
             [0, 0, 0, 0, 0, 6, 8, 0, 0],
             [0, 0, 0, 1, 3, 0, 0, 0, 9],
             [4, 0, 5, 0, 0, 9, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 3, 0, 0],
             [0, 0, 6, 0, 0, 7, 0, 0, 0],
             [1, 0, 0, 3, 4, 0, 0, 0, 0]]))

print(solve([
        [9, 0, 6, 0, 0, 1, 0, 4, 0],
        [7, 0, 1, 2, 9, 0, 0, 6, 0],
        [4, 0, 2, 8, 0, 6, 3, 0, 0],
        [0, 0, 0, 0, 2, 0, 9, 8, 0], 
        [6, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 9, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 3, 7, 0, 8, 4, 0, 9],
        [0, 4, 0, 0, 1, 3, 7, 0, 6],
        [0, 6, 0, 9, 0, 0, 1, 0, 8]]))

