# File containing classes to represents a CNF formula

import math
import linecache
import time
from iteration_utilities import first


    
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self):
        
        # The current recursive depth
        self.current_depth = 0

        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {}

        # List of clauses which form the CNF
        self.clauses = {}
        self.active_clauses = []

        # Hold the removed clauses like {"depth": [clauseid, clauseid]}
        self.removed_clauses = {}

        # Hold the removed literals like {"depth": [[clauseid, literal], [clauseid, literal]]}
        self.removed_literals = {}

        # History of the variables assigned by branching
        self.branch_history = {}
        

        


    def remove_clause(self, clause_index):
        """Correctly removes a clause"""
        # Remove clause from variable_occurs_in
        for literal in self.clauses[str(clause_index)]:
            if literal < 0:
                self.variable_dict[str(abs(literal))].occurs_negated_in.remove(clause_index)
            if literal > 0:
                self.variable_dict[str(abs(literal))].occurs_positive_in.remove(clause_index)
        
        self.active_clauses.remove(clause_index)

        # Add to removed/depth log
        if str(self.current_depth) not in self.removed_clauses:
            self.removed_clauses[str(self.current_depth)] = []
            
        self.removed_clauses[str(self.current_depth)].append(clause_index)
    

    def undo_clause_remove(self, depth):
        """ Undos the removal of clauses at a specific height"""
        if str(depth) in self.removed_clauses:
            for clause_index in self.removed_clauses[str(depth)]:
                
                # Reactivate clause
                self.active_clauses.append(clause_index)

                # Re-add clause to variable_occurs_in
                for literal in self.clauses[str(clause_index)]:
                    if literal < 0:
                        self.variable_dict[str(abs(literal))].occurs_negated_in.add(clause_index)
                    if literal > 0:
                        self.variable_dict[str(abs(literal))].occurs_positive_in.add(clause_index)
        
        # Reset removed_clauses at that depth
        self.removed_clauses[str(depth)] = []
    

    def remove_literal(self, clause_index, literal):
        """"Propely removes a literal"""

        # Remove from variable.occurs_in
        if literal < 0:
            self.variable_dict[str(abs(literal))].occurs_negated_in.remove(clause_index)
        if literal > 0:
            self.variable_dict[str(abs(literal))].occurs_positive_in.remove(clause_index)
        
        self.clauses[str(clause_index)].remove(literal)

        if str(self.current_depth) not in self.removed_literals:
            self.removed_literals[str(self.current_depth)] = []
        self.removed_literals[str(self.current_depth)].append([clause_index, literal])
    

    def undo_branch(self, depth):
        """Undos a branch at a specigic depth"""
        if str(depth) in self.branch_history:
            for var in self.branch_history[str(depth)]:
                self.variable_dict[str(var)].boolean = None
        self.undo_clause_remove(depth)
        self.undo_literal_remove(depth)


    def undo_literal_remove(self, depth):
        """undos the removal of literals at a specific depth"""
        
        if str(depth) in self.removed_literals:
            for clause_index, literal in self.removed_literals[str(depth)]:
                
                # Re-add literal
                self.clauses[str(clause_index)].add(literal)

                # Re add to occurs_in
                if literal < 0:
                    self.variable_dict[str(abs(literal))].occurs_negated_in.add(clause_index)
                if literal > 0:
                    self.variable_dict[str(abs(literal))].occurs_positive_in.add(clause_index)
        
        # Reset removed_clauses at that depth
        self.removed_literals[str(depth)] = []
    

    def branch(self, variable, boolean):
        """Branch the clauses by changing a variable to a boolean"""

        # Set variable to boolean
        self.variable_dict[str(variable)].boolean = boolean
        if boolean:

            # Remove clause if its satisfies the clause
            for clause_index in self.variable_dict[str(variable)].occurs_positive_in.copy():
                self.remove_clause(clause_index)
            
            # Only remove literal if clause not satisfied
            for clause_index in self.variable_dict[str(variable)].occurs_negated_in.copy():
                self.remove_literal(clause_index, -1*variable)

        if not boolean:
            # Only remove literal if clause not satisfied
            for clause_index in self.variable_dict[str(variable)].occurs_positive_in.copy():
                self.remove_literal(clause_index, (variable))

            # Remove clause if its satisfies the clause
            for clause_index in self.variable_dict[str(variable)].occurs_negated_in.copy():
                self.remove_clause(clause_index)

        if not str(self.current_depth) in self.branch_history:
            self.branch_history[str(self.current_depth)] = []
        self.branch_history[str(self.current_depth)].append(variable)
                
    def pick_active_variable(self, heuristic_name):
        """Picks the variable which will be branched"""
        # Returns first literal (actually random though) of first active clause
        if heuristic_name == "pick-first":
            return abs(first(self.clauses[str(self.active_clauses[0])]))


    

    def remove_unit_clauses(self):
        """Remove unit clauses and add it to removed clauses"""
        active_clauses_index = 0
        while active_clauses_index < len(self.active_clauses):
            clause_id = self.active_clauses[active_clauses_index]
            if len(self.clauses[str(clause_id)]) == 1:
                literal = first(self.clauses[str(clause_id)])
                
                # We save unit clauses in the minus version of the current depth
                self.current_depth *= -1
                boolean = (literal > 0)
                self.branch(abs(literal), boolean)
                self.current_depth *= -1
                
                # We want to reset the search for unit clauses because new ones could have been created
                active_clauses_index = 0
            else:
                active_clauses_index += 1
    
    def undo_unit_clauses(self):
        self.undo_branch(self.current_depth * -1)
    
    def remove_pure_literals(self):
        """Remove all clauses with pure literals"""
        for variable in self.variable_dict:
            variable = self.variable_dict[variable]
            
            if not variable.occurs_negated_in.copy():
                self.branch(variable.variable_name, True)
            
            elif not variable.occurs_positive_in.copy():
                self.branch(variable.variable_name, False)
        
        # Clear history, you dont want to turn this back
        if str(0) in self.removed_clauses:
            del self.removed_clauses[str(0)]
        if str(0) in self.removed_literals:
            del self.removed_literals[str(0)]
        if str(0) in self.branch_history:
            del self.branch_history[str(0)]

    def remove_tautologies(self):
        """Removes all the clauses containing a tautology"""
        # Check for every variable if it is both in negated and postive form in the same clause
        for variable in self.variable_dict:
            variable = self.variable_dict[variable]
            for occurs_negated in variable.occurs_negated_in.copy():
                if occurs_negated in variable.occurs_positive_in:
                    self.remove_clause(occurs_negated)
        
        # Clear history, you dont want to turn this back
        if str(0) in self.removed_clauses:
            del self.removed_clauses[str(0)]
        if str(0) in self.removed_literals:
            del self.removed_literals[str(0)]
        if str(0) in self.branch_history:
            del self.branch_history[str(0)]




    def contains_empty_clause(self):
        """Returns if the CNF contains an empty clause and is thus unsatisfiable"""
        
        # Check if there exists a clause that is empty
        for clause_index in self.active_clauses:
            if not self.clauses[str(clause_index)]:
                return True
        return False


    def load_dimacs_string(self, string):
        """Encode a dimacs string and add it to the clause list of this CNF_formula"""
        
        clause_counter = len(self.clauses)
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
            self.active_clauses.append(clause_counter)
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
        
        for clause_key in sorted(self.active_clauses):
            value = self.clauses[str(clause_key)]
            if not value:
                print(f"{clause_key}: empty clause")
            else:
                print(f"{clause_key}: {value}")
        print()
    

    def print_variable_counts(self):
        """Prints the records of in which clause literals are still located"""

        print("Variable name, followed by in which clauses it is located negated (-) and positive(+)")
        for variable in sorted(self.variable_dict, key = lambda x: int(x) ):
            print("{} occurs in clauses: -:{}, +:{}".format(self.variable_dict[variable].variable_name, list(self.variable_dict[variable].occurs_negated_in), list(self.variable_dict[variable].occurs_positive_in)))
        print()
        

    def print_status(self):
        """Print the currently loaded variables and clauses"""

        print(f"Variables: {len(self.variable_dict)}, Clauses: {len(self.active_clauses)}")
        print()


    def print_assignments(self):
        for variable in sorted(self.variable_dict, key = lambda x: int(x)):
            print(f"{variable}: {self.variable_dict[variable].boolean}")
        print()

    def print_answer(self):
        print("Sudoku answer: ")
        for variable in sorted(self.variable_dict, key = lambda x: int(x)):
            if self.variable_dict[variable].boolean == True:
                print(f"{variable}: {self.variable_dict[variable].boolean}")
        print()

    def print_total_status(self):

        print("-------------------------------------------------------------")
        print("Depth = {}\n".format(self.current_depth))
        self.print_status()
        self.print_clauses()
        self.print_assignments()
        self.print_variable_counts()
        print("Removed clauses: ", self.removed_clauses)
        print("Removed literals: ", self.removed_literals)
        
        print("-------------------------------------------------------------")


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



if __name__ == "__main__":
    pass