# File containing classes to represents a CNF formula

import math
import linecache
import time


    
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self):
        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {}

        # List of clauses which form the CNF
        self.clauses = {}

    def remove_unit_clauses(self):
        """Remove unit clauses and add it to removed clauses"""

    def remove_pure_literals(self):
        """Remove all clauses with pure literals"""
        
    def remove_tautologies(self):
        """Returns if the CNF contains a tautology"""
        
    def contains_empty_clause(self):
        """Returns if the CNF contains an empty clause and is thus unsatisfiable"""
        
        # Check if there exists a clause that is empty
        for clause in self.clauses:
            if not clause:
                return True
        return False

    def load_dimacs_string(self, string):
        """Encode a dimacs string and add it to the clause list of this CNF_formula"""
        
        clause_counter = 0
        # Every line is a clause
        for line in string.splitlines():

            # Skip the lines starting with p or c
            if line[0] == "p" or line[0] == "c":
                continue

            # Puts ints in a list. Remove last cause its 0
            literals = line.split(" ")[:-1]
            
            # Turn all literal strings to literal objects 
            literal_set = set()
            for literal in literals:

                literal = int(literal)
        
                # Get (none negated) variable
                variable = abs(literal)

                # If not yet in dict create new dict entry
                if str(variable) not in self.variable_dict:
                    self.variable_dict[str(variable)] = Variable(str(variable))
                
                literal_set.add(literal)
                
                # Update variable counter
                if literal < 0:
                    self.variable_dict[str(variable)].occurs_negated_in.add(clause_counter)
                else:
                    self.variable_dict[str(variable)].occurs_positive_in.add(clause_counter)

            # Make new clause and append to CNF clause list
            self.clauses[str(clause_counter)] = literal_set
            clause_counter += 1
    
    def load_dimacs_file(self, file):
        """Accepts a dimac file and turns it into a string, then uses another method to encode it and add it to the clauses"""
        
        # Turn file into string
        with open(file, "r") as dimac:
            string = dimac.read()

        # Add string to clauses
        self.load_dimacs_string(string)

    def load_sudoku_file(self, mfile):
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
        print("Clause_id: clause_set")
        if not self.clauses:
            print("No clauses left")
            print()
            return
        
        for key, value in self.clauses.items():
            if not value:
                print(f"{key}: empty clause")
            else:
                print(f"{key}: {value}")
        print()
    
    def print_variable_counts(self):
        print("Variable name, followed by in which clauses it is located negated (-) and positive(+)")
        for variable in self.variable_dict:
            print("{} occurs in clauses: -:{}, +:{}".format(self.variable_dict[variable].variable_name, list(self.variable_dict[variable].occurs_negated_in), list(self.variable_dict[variable].occurs_positive_in)))
        print()
    # Print the currently loaded variables and clauses
    def print_status(self):
        print(f"Variables: {len(self.variable_dict)}, Clauses: {len(self.clauses)}")
        print()



class Variable():
    """Represents a variable"""

    def __init__(self, name):
        # Name of the variable (e.g. 112)
        self.variable_name = name

        # Current boolean status of the variable, starts as None
        self.boolean = None

        # The clause id's in which this variable is present in negated/positive from
        self.occurs_negated_in = set()
        self.occurs_positive_in = set()

        # A list
        self.occurs_in_clause_ids = []

if __name__ == "__main__":
    
    CNF = CNF_Formula()

    CNF.load_dimacs_file("test.txt")
    CNF.print_status()
    CNF.print_clauses()
    CNF.print_variable_counts()
    
    