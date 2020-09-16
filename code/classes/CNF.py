# File containing classes to represents a CNF formula

import math
import linecache
import time
from iteration_utilities import first

from classes.Variable import Variable
from functions.sud2cnf import SUD2CNF

from heuristics.PickFirst import PickFirst
from heuristics.LowestVar import LowestVar
from heuristics.DLCS import DLCS
from heuristics.DLIS import DLIS
from heuristics.JeroslowWangOS import JeroslowWangOS
from heuristics.JeroslowWangTS import JeroslowWangTS
from heuristics.MOMS import MOMS

    
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self):
        
        # The current recursive depth
        self.current_depth = 0

        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {}

        # List of clauses which form the CNF
        self.clauses = {}
        self.active_clauses = set()
        self.clauses_removed_part = {}

        # Hold the removed clauses like {"depth": [clauseid, clauseid]}
        self.removed_clauses = {}

        # Hold the removed literals like {"depth": [[clauseid, literal], [clauseid, literal]]}
        self.removed_literals = {}

        # History of the variables assigned by branching
        self.branch_history = {}

        # List of clause id's that are unit clauses
        self.unit_clauses = set()
        
        self.unit_clause_counter = 0

        # K factor as used by MOMS
        self.k_factor = 1

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

        # Check if we removed a unit_clause.
        if len(self.clauses[str(clause_index)]) == 1:
            self.unit_clauses.remove(clause_index)
    

    def undo_clause_remove(self, depth):
        """ Undos the removal of clauses at a specific height"""
        if str(depth) in self.removed_clauses:
            for clause_index in self.removed_clauses[str(depth)]:
                
                # Reactivate clause
                self.active_clauses.add(clause_index)

                # Re-add clause to variable_occurs_in
                for literal in self.clauses[str(clause_index)]:
                    if literal < 0:
                        self.variable_dict[str(abs(literal))].occurs_negated_in.add(clause_index)
                    if literal > 0:
                        self.variable_dict[str(abs(literal))].occurs_positive_in.add(clause_index)

                # Check if the new clause is a unit clause
                if len(self.clauses[str(clause_index)]) == 1:
                    self.unit_clauses.add(clause_index)

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

        # Add to removed literals history
        if str(self.current_depth) not in self.removed_literals:
            self.removed_literals[str(self.current_depth)] = []
        self.removed_literals[str(self.current_depth)].append([clause_index, literal])

        # Add to removed part of clauses
        if str(clause_index) not in self.clauses_removed_part:
            self.clauses_removed_part[str(clause_index)] = []
        self.clauses_removed_part[str(clause_index)].append(literal)

        # Check if removed a unit_clause
        if len(self.clauses[str(clause_index)]) == 0:
            self.unit_clauses.remove(clause_index)

        # Check if we ADDED a unit clause
        elif len(self.clauses[str(clause_index)]) == 1:
            self.unit_clauses.add(clause_index)
        
    
    def undo_branch(self, depth):
        """Undos a branch at a specific depth"""
        
        if str(depth) in self.branch_history:
            for var in self.branch_history[str(depth)]:
                self.variable_dict[str(var)].boolean = None
                self.variable_dict[str(var)].by_branch = None
                self.variable_dict[str(var)].set_depth = None
                self.variable_dict[str(var)].caused_by_clause_id = None
            self.branch_history[str(depth)] = []
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

                self.clauses_removed_part[str(clause_index)].remove(literal)

                # Check if we added/removed a unit clause
                if clause_index in self.active_clauses:
                    if len(self.clauses[str(clause_index)]) == 1:
                        self.unit_clauses.add(clause_index)
                    elif clause_index in self.unit_clauses:
                        self.unit_clauses.remove(clause_index)
        
        # Reset removed_clauses at that depth
        self.removed_literals[str(depth)] = []
    

    def branch(self, variable, boolean):
        """Branch the clauses by changing a variable to a boolean"""

        # Set variable to boolean
        self.variable_dict[str(variable)].boolean = boolean
        self.variable_dict[str(variable)].by_branch = True
        self.variable_dict[str(variable)].set_depth = self.current_depth

        # if True
        if boolean:
            # Remove clause if its satisfies the clause
            for clause_index in self.variable_dict[str(variable)].occurs_positive_in.copy():
                self.remove_literal(clause_index, variable)
                self.remove_clause(clause_index)
            
            # Only remove literal if clause not satisfied
            for clause_index in self.variable_dict[str(variable)].occurs_negated_in.copy():
                self.remove_literal(clause_index, -1*variable)

        # If False
        if not boolean:
            # Only remove literal if clause not satisfied
            for clause_index in self.variable_dict[str(variable)].occurs_positive_in.copy():
                self.remove_literal(clause_index, (variable))

            # Remove clause if its satisfies the clause
            for clause_index in self.variable_dict[str(variable)].occurs_negated_in.copy():
                self.remove_literal(clause_index, -1 *variable)
                self.remove_clause(clause_index)

        # Create depth if doesnt exists yet
        if not str(self.current_depth) in self.branch_history:
            self.branch_history[str(self.current_depth)] = []

        self.branch_history[str(self.current_depth)].append(variable)


    def pick_active_variable(self, heuristic_name):
        """Picks the variable which will be branched"""

        # Returns first literal (actually random though) of first active clause.
        if heuristic_name == "PickFirst":
            return PickFirst(self)

        # Returns the avtive variable with lowest value.
        if heuristic_name == "LowestVar":
            return LowestVar(self)
        
        if heuristic_name == "DLCS":
            return DLCS(self)

        if heuristic_name == "DLIS":
            return DLIS(self)

        if heuristic_name == "JeroslowWangOS":
            return JeroslowWangOS(self)
        
        if heuristic_name == "JeroslowWangTS":
            return JeroslowWangTS(self)
        
        if heuristic_name == "MOMS":
            return MOMS(self)

        else:
            print("Error: Invalid heuristic")
            exit()


    def build_unit_clauses_list(self):
        """ Initially build up the unit clauses list """
        for clause_id in self.clauses:
            if len(self.clauses[clause_id]) == 1:
                self.unit_clauses.add(int(clause_id))


    def remove_unit_clauses(self):
        """Remove unit clauses and add it to removed clauses"""
        while self.unit_clauses:
            clause_id = first(self.unit_clauses)
            if len(self.clauses[str(clause_id)]) == 1:

                if clause_id not in self.unit_clauses:
                    print(f"Error: not in unit clauses: {clause_id}")
                    self.print_total_status()
                    exit()

                literal = first(self.clauses[str(clause_id)])
                
                # We save unit clauses in the minus version of the current depth
                self.current_depth *= -1
                boolean = (literal > 0)
                self.branch(abs(literal), boolean)
                self.current_depth *= -1
                
                # Save implication_graph_info
                self.variable_dict[str(abs(literal))].by_branch = False
                self.variable_dict[str(abs(literal))].set_depth = self.current_depth
                self.variable_dict[str(abs(literal))].caused_by_clause_id = clause_id
                
                self.unit_clause_counter += 1
            else:
                print("ERROR")
        
        if self.unit_clauses:
            print(f"Error: unit clauses left: {self.unit_clauses}")
            self.print_total_status()
            exit()
        

    def undo_unit_clauses(self):
        """ Undo all unit clauses at a specific depth """
        self.undo_branch(self.current_depth * -1)
    

    def remove_pure_literals(self):
        """ Remove all clauses with pure literals """
        for variable in self.variable_dict:
            variable = self.variable_dict[variable]
            
            if not variable.occurs_negated_in.copy():
                self.branch(int(variable.variable_name), True)
            
            elif not variable.occurs_positive_in.copy():
                self.branch(int(variable.variable_name), False)
        
        # Clear history, you dont want to turn this back
        if str(0) in self.removed_clauses:
            del self.removed_clauses[str(0)]
        if str(0) in self.removed_literals:
            del self.removed_literals[str(0)]
        if str(0) in self.branch_history:
            del self.branch_history[str(0)]

    def remove_tautologies(self):
        """ Removes all the clauses containing a tautology """
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

    def learn_clause(self, conflict_id):
        """ Learn a new clause based on a current conflict"""

        
        partial_clause = set(self.clauses_removed_part[conflict_id])

        while True:
            

            # Count amount that have current depth_level
            current_depth_amount = 0
            for literal in partial_clause:
            
                if self.variable_dict[str(abs(literal))].set_depth == self.current_depth:
                    current_depth_amount += 1
            if current_depth_amount == 1:
                break
            
            # Expand first literal
            for literal in partial_clause:
                if (self.variable_dict[str(abs(literal))].by_branch == False 
                and self.variable_dict[str(abs(literal))].set_depth == self.current_depth
                and self.variable_dict[str(abs(literal))].caused_by_clause_id != None ):
                    partial_clause = partial_clause | {literal for literal in self.clauses_removed_part[str(self.variable_dict[str(abs(literal))].caused_by_clause_id)] if literal not in partial_clause}
                    self.variable_dict[str(abs(literal))].caused_by_branch = True
                    break
                    
            else:
                print("no literal to expand found, error")
                exit()
            
            # Resolve the parial:
            literal_counter = 0
            while literal_counter < len(partial_clause):
                if -1*literal in partial_clause:
                    partial_clause.remove(literal)
                    partial_clause.remove(-1*literal)
                else:
                    literal_counter += 1
        
        if len(partial_clause) < 20:
            print("Found learning clause: ", partial_clause)
        else:
            print("Found learning clause: len > 20")
        
        # Find highest depth that is not the current depth:
        highest_depth = -1
        
        # Unit clauses always have to go back to depth 0
        if len(partial_clause) == 1:
            highest_depth = 0
        else:
            for literal in partial_clause:
                # Search for higher highest depth that is not the current depth
                if self.current_depth > self.variable_dict[str(abs(literal))].set_depth > highest_depth:
                    highest_depth = self.variable_dict[str(abs(literal))].set_depth

        if highest_depth == -1:
            print("Error: found invalid highest depth")
            exit()

        # Add learned clause to clauses:
        clause_id = len(self.clauses)
        self.clauses[str(clause_id)] = set(partial_clause)
        self.active_clauses.add(clause_id)
        
        # Also add to unit clause list
        if len(self.clauses[str(clause_id)]) == 1:
            self.unit_clauses.add(clause_id)

        # Updat var counters
        for literal in partial_clause:
            if literal < 0:
                self.variable_dict[str(abs(literal))].occurs_negated_in.add(clause_id)
            else:
                self.variable_dict[str(abs(literal))].occurs_positive_in.add(clause_id)
        
        # We also need to remove literals if already set to boolean
        for literal in partial_clause:
            if literal < 0:
                if self.variable_dict[str(abs(literal))].boolean == True:
                    correct_depth = self.current_depth
                    self.current_depth = self.variable_dict[str(abs(literal))].set_depth
                    self.remove_literal(clause_id, literal)
                    self.current_depth = correct_depth
                if self.variable_dict[str(abs(literal))] == False:
                    print("Error")
                    exit()
            
            if literal > 0:
                if self.variable_dict[str(abs(literal))].boolean == False:
                    correct_depth = self.current_depth
                    self.current_depth = self.variable_dict[str(abs(literal))].set_depth
                    self.remove_literal(clause_id, literal)
                    self.current_depth = correct_depth
                if self.variable_dict[str(abs(literal))] == True:
                    print("Error")
                    exit()

        return highest_depth


    def contains_empty_clause(self):
        """Returns if the CNF contains an empty clause and is thus unsatisfiable"""
        
        # Check if there exists a clause that is empty
        for clause_index in self.active_clauses:
            if not self.clauses[str(clause_index)]:
                return str(clause_index)
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
            literals = line.split()[:-1]
            
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
            self.active_clauses.add(clause_counter)
            clause_counter += 1
    

    def load_dimacs_file(self, file):
        """Accepts a dimac file and turns it into a string, then uses another method to encode it and add it to the clauses"""
        
        # Turn file into string
        with open(file, "r") as dimac:
            string = dimac.read()

        # Add string to clauses
        self.load_dimacs_string(string)


    def load_sudoku_file(self, mfile, sudN=False):
        """ Function to load sudoku from external file"""
        sud_loader = SUD2CNF()
        sud_loader.load(mfile, sudN)

        
        # Use this method to encode the dimac file and add it to the CNF
        self.load_dimacs_string(sud_loader.sudtorules)

    
    def print_clauses(self):
        """Print all active clauses of the cnf"""

        print("Clause_id: clause_set : removed_part")
        if not self.clauses:
            print("No clauses left")
            print()
            return
        
        #for clause_key in range(0, max([int(key) for key in self.clauses.keys()]) + 1):
        for clause_key in self.active_clauses:
            value = self.clauses[str(clause_key)]
            if not value:
                if str(clause_key) in self.clauses_removed_part:
                    print(f"{clause_key}: empty clause:      {self.clauses_removed_part[str(clause_key)]}")
                else:
                    print(f"{clause_key}: empty clause")
            else:
                if str(clause_key) in self.clauses_removed_part:
                    print(f"{clause_key}: {value} :        {self.clauses_removed_part[str(clause_key)]}")
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
        """ Print all variable boolean assignments"""
        for variable in sorted(self.variable_dict, key = lambda x: int(x)):
            print(f"{variable}: {self.variable_dict[variable].boolean}")
            variable = self.variable_dict[variable]
            print(f"     by_branch: {variable.by_branch}     depth: {variable.set_depth}     caused_by: {variable.caused_by_clause_id}")
        print()

    def print_answer(self):
        """ Print the found sudoku answer"""
        print("Sudoku answer: ")
        for variable in sorted(self.variable_dict, key = lambda x: int(x)):
            if self.variable_dict[variable].boolean == True:
                print(f"{variable}: {self.variable_dict[variable].boolean}")
        print()

    def print_total_status(self):
        """ Print ALLL the status prints (a lot)"""
        print("-------------------------------------------------------------")
        print("Depth = {}\n".format(self.current_depth))
        self.print_status()
        self.print_clauses()
        self.print_assignments()
        self.print_variable_counts()
        print("Removed clauses: ", self.removed_clauses)
        print("Removed literals: ", self.removed_literals)
        print(self.branch_history)
        print("-------------------------------------------------------------")