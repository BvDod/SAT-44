# File containing classes to represents a CNF formula

import math
import linecache

class Variable():
    """Represents a variable"""

    def __init__(self, name):
        # Name of the variable (e.g. 112)
        self.variable_name = name

        # Current boolean status of the variable, starts as None
        self.boolean = None

class Literal():
    """Represents a single literal"""

    def __init__(self, variable, negated):
        # The variable "name" this literal represents
        self.variable = variable

        # Bool which represents if the literal is negated or not
        self.negation = negated
    
    def __str__(self):
        return ("-" * self.negation) + (self.variable.variable_name)

class Clause():
    """"Represents a single clause, which is a disjunction of literals"""

    def __init__(self, literals):

        # List of literals that are contained in the Clause.
        self.literals = literals
    
    def __str__(self):
        string = ""
        for literal in self.literals:
            string += "{} v ".format(literal)
        return string[:-3]
        
    
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self):
        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {}

        # List of clauses which form the CNF
        self.clauses = []


    def load_dimacs_string(self, string):
        """Encode a dimacs string and add it to the clause list of this CNF_formula"""
           
        # Every line is a clause
        for line in string.splitlines():

            # Skip the lines starting with p or c
            if line[0] == "p" or line[0] == "c":
                continue

            # Puts ints in a list. Remove last cause its 0
            literals = line.split(" ")[:-1]
            
            # Turn all literal strings to literal objects 
            literal_objects = []
            for literal in literals:

                literal = int(literal)
        
                # Get (none negated) variable
                variable = abs(literal)

                # If not yet in dict create new dict entry
                if variable not in self.variable_dict:
                    self.variable_dict[str(variable)] = Variable(str(variable))
                
                # Check if negated
                negated = (literal < 0)

                literal_objects.append(Literal(self.variable_dict[str(variable)], negated))

            # Make new clause and append to CNF clause list
            clause = Clause(literal_objects)
            self.clauses.append(clause)
    
    def load_dimacs_file(self, file):
        """Accepts a dimac file and turns it into a string, then uses another method to encode it and add it to the clauses"""
        
        # Turn file into string
        with open(file, "r") as dimac:
            string = dimac.read()

        # Add string to clauses
        self.load_dimacs_string(string)

    def load_sudoku(self, mfile):
        # Opens the file, reads the number of sudokus (lines) in it and asks which sudoku you want to solve
        with open(mfile, "r") as sud_file:
            nbLines = len(sud_file.readlines())
        print ("Loading file",mfile)
        sudNb = input("{} sudokus have been found in this file.\nWhich one should we solve ?\n".format(nbLines))
        
        # Opens the file to transform the sudoku line into a string in CNF
        line = linecache.getline(mfile, int(sudNb))
        length = math.sqrt(len(line))
        length = (int(round(length)))
        sudtorules = []
        for i in range(length):
            for j in range(length):
                n = line[i*length+j]
                if n!="." :
                    string = ("{}{}{}".format(i+1,j+1,n))
                    sudtorules.append(string)
        sudoku_dimacs = ""
        for rule in sudtorules:
            sudoku_dimacs = sudoku_dimacs +("{} 0\n".format(rule))
        
        # Use this method to encode the dimac file and add it to the CNF
        self.load_dimacs_string(sudoku_dimacs)

    # Prints all clauses of the CNF
    def print_clauses(self):
        for clause in self.clauses:
            print(clause)  

     
if __name__ == "__main__":
    
    CNF = CNF_Formula()
    
    CNF.load_dimacs_file("rules.txt")
    # CNF.print_clauses()
    print(f"Variables: {len(CNF.variable_dict)}, Clauses: {len(CNF.clauses)}")
    
    CNF.load_sudoku("4x4.txt")
    print(f"Variables: {len(CNF.variable_dict)}, Clauses: {len(CNF.clauses)}")