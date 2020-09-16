#!/usr/bin/python3
import sys
import math

class SUD2CNF():
  def __init__(self):
    self.sudtorules = ""
	
  def load(self,mfile):
    # Opens the file, reads the number of sudokus (lines) in it and asks which sudoku you want to solve
    nbLines = len(open(mfile).readlines())
    print ("Loading file",mfile)
    sudNb = input("{} sudokus have been found in this file.\nWhich one should we solve ?\n".format(nbLines))
    
    # Opens the file to transform the sudoku line into a string in CNF
    mfread = open(mfile,"r")
    for i in range(int(sudNb)-1):
      mfread.readline()
    line = mfread.readline()
    length = math.sqrt(len(line))
    length = (int(round(length)))
    sudtorules = []
    if length==16:
      for i in range(length):
        for j in range(length):
          n = line[i*length+j]
          if n!="." :
            string = ("{}".format(289*(i+1)+17*(j+1)+int(n,17)))
            sudtorules.append(string)
    else:
      for i in range(length):
        for j in range(length):
          n = line[i*length+j]
          if n!="." :
            string = ("{}{}{}".format(i+1,j+1,n))
            sudtorules.append(string)
    for rule in sudtorules:
      self.sudtorules = self.sudtorules+("{} 0\n".format(rule))

if __name__ == "__main__":
  # Checks if you've entered the correct arguments
  if len(sys.argv) != 2 :
    print ("Error in number of arguments. Command form : python SudToCNF.py pathToFile")
    exit(1)

  # Main code
  cnf = SUD2CNF()
  cnf.load(sys.argv[1])
  print(cnf.sudtorules)
