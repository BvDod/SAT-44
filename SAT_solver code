#Looking for numbers in the sudoku grid#

def possible(y,x,n): 
  global grid
  for i in range(0,9): 
    if grid[y][i] == n: 
      return False 
  for i in range(0,9): 
    if grid[i][x] == n:
      return False
  x0 = (x//3)*3
  y0 = (x//3)*3
  for i in range(0,3):
    for j in range(0,3):
      if grid[y0+1][x0+j] == n:
        return False
   return True

#Check solutions of the puzzle with determining the position of open box (y, x) and possible answer (n)#
#Returns either True (correct answer) or False (not correct answer)

possible(y,x,n)

#Solve the sudoku with all possible numbers 1-9#
#0 = empty box, could also be '.'?#
def solve():
  global grid
  for y in range(9)
    for x in range(9):
      if grid[y][x] == 0:
        for n in range (1,10)
          if possible(y,x,n)
            grid[y][x]= n
            solve()
            grid[y][x]= 0
          return 

#Print the matrix grid#
  print(np.matrix(grid)) 

#Check if there are more solutions to the problem? All options will be printed underneath each other#
  input("More?")

#If all solutions to the problem have been given, FIN#
          
  
   
     
