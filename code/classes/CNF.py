# File containing classes to represents a CNF formula

import math
import linecache
    
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self):
        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {}

        # List of clauses which form the CNF
        self.clauses = []

        # Remember removed clauses so you can reverse it.
        self.removed_clauses = []
        self.changed_variables = []

    def remove_unit_clauses(self):
        """Remove unit clauses and add it to removed clauses"""
        clause_counter = 0
        while clause_counter < len(self.clauses):
            if len(self.clauses[clause_counter].literals) == 1:
                if self.clauses[clause_counter].literals[0].variable.boolean == None:
                    self.clauses[clause_counter].literals[0].variable.boolean = not self.clauses[clause_counter].literals[0].negation
                    self.changed_variables.append(variable)
                    print("removed", self.clauses[clause_counter])
                    self.remove_clause(clause_counter)
                    continue
                else:
                    print("Error: boolean should always be None in this case")
                    exit()
                
            clause_counter += 1  

    def remove_clause(self, clause_index):
        """This function is used to remove clauses and handle it correctly"""
        
        # Go over all literals in clause and remove them from the variable counter
        for literal in self.clauses[clause_index]:
            if literal.negation:
                literal.variable.occurs_negated -= 1
            else:
                literal.variable.occurs_positive -= 1

        self.removed_clauses.append(self.clauses[clause_index])
        
        del self.clauses[clause_index]

    def remove_pure_literals(self):
        """Remove all clauses with pure literals"""
        
        # Check for all variables if they only exist in negated or positive manner,
        for variable in self.variable_dict:
            
            self.print_clauses()
            print()
            # Only occurs negated 
            if (self.variable_dict[variable].occurs_negated != 0 and self.variable_dict[variable].occurs_positive == 0):
                self.variable_dict[variable].boolean = False
            
            # Only occurs positve
            elif (self.variable_dict[variable].occurs_negated == 0 and self.variable_dict[variable].occurs_positive != 0):
                self.variable_dict[variable].boolean = True

            # Else skip this variable
            else:
                continue
            
            # Add to list of vars we changed
            self.changed_variables.append(variable)

            # Remove all clauses that have that variable
            clause_counter = 0
            while clause_counter < len(self.clauses):
                

                # Check all literals in clauses
                for literal in self.clauses[clause_counter]:
                    # if variable in clause
                    if literal.variable.variable_name == variable:
                        print(literal.variable.variable_name, variable)
                        print("remove: ", self.clauses[clause_counter])
                        self.remove_clause(clause_counter)
                        break
                # if no break
                else: 
                    clause_counter += 1  

        
    
    def remove_tautologies(self):
        """Returns if the CNF contains a tautology"""

        # Go over every var, and delete var if a tautology exists inside the clause
        clause_counter = 0
        while clause_counter < len(self.clauses):
                clause_var_dict = {}

                # Count the amount of times a var exists negated and non negated
                for literal in self.clauses[clause_counter]:
                    if literal.variable.variable_name not in clause_var_dict:
                        clause_var_dict[literal.variable.variable_name] = [0, 0]
                    clause_var_dict[literal.variable.variable_name][literal.negation] += 1
                
                # Check if both negated and non negated vars exists inside same clause
                for var in clause_var_dict:
                    if clause_var_dict[var][0] > 0 and clause_var_dict[var][1] > 0:
                        self.remove_clause(clause_counter)
                        continue
                
                clause_counter += 1 
    
    def undo_changes(self):
        """undo the changes we made with the simplify rules"""
        
        # Reset booleans to None
        for variable in self.changed_variables:
            self.variable_dict[variable].boolean = None

        # Re add variable counts:
        for clause in self.removed_clauses:
            for literal in clause:
                if literal.negation:
                    literal.variable.occurs_negated += 1
                else:
                    literal.variable.occurs_positive += 1
        
        # Re add clauses
        self.clauses = self.clauses + self.removed_clauses

    def contains_empty_clause(self):
        """Returns if the CNF contains an empty clause and is thus unsatisfiable"""
        
        # Check if there exists a clause that is empty
        for clause in self.clauses:
            if not clause:
                return True
        return False

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
                if str(variable) not in self.variable_dict:
                    self.variable_dict[str(variable)] = Variable(str(variable))
                
                # Check if negated
                negated = (literal < 0)

                literal_objects.append(Literal(self.variable_dict[str(variable)], negated))
                
                # Update variable counter
                if negated:
                    self.variable_dict[str(variable)].occurs_negated += 1
                else:
                    self.variable_dict[str(variable)].occurs_positive += 1

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
        if not self.clauses:
            print("No clauses left")
            print()
            return
        
        for clause in self.clauses:
            if not clause:
                print("empty clause")
            print(clause)
        print()
    
    def print_variable_counts(self):
        for variable in self.variable_dict:
            print("{}: {}, {}".format(self.variable_dict[variable].variable_name, self.variable_dict[variable].occurs_negated, self.variable_dict[variable].occurs_positive))
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

        # A Counter which documents the amount of times this variable is used both negated and non negated.
        # This will be very usefull when we implement a remove unit clauses method.
        self.occurs_negated = 0
        self.occurs_positive = 0


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

    # Make for loops work with clauses
    def __iter__(self):
        return iter(self.literals)

if __name__ == "__main__":
    
    CNF = CNF_Formula()

    CNF.load_dimacs_file("test.txt")
    
    CNF.print_clauses()
    CNF.print_variable_counts()

    CNF.remove_tautologies()

    CNF.print_clauses()
    CNF.print_variable_counts()
    
    # Undo the changes made, should return to initial status.
    CNF.undo_changes()
    CNF.print_clauses()
    CNF.print_variable_counts()