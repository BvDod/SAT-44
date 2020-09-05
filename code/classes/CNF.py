# File containing classes to represents a CNF formula

class Variable():
    """Represents a variable"""

    def __init__(self):
        # Name of the variable (e.g. 112)
        self.variable_name =

        # Current boolean status of the variable, starts as None
        self.boolean = 

class Literal():
    """Represents a single literal"""

    def __init__(self, ):
        # The variable "name" this literal represents
        self.variable = 

        # Bool which represents if the literal is negated or not.
        self.negation = 

class Clause():
    """"Represents a single clause, which is a disjunction of literals"""

    def __init__(self,):

        # List of literals that are contained in the Clause.
        self.literals = 
        
class CNF_Formula():
    """Represents a CNF_Formula, which is a conjuction of clauses"""

    def __init__(self, clause_list):
        # Dict with variables thats are used to buid literal and thus clauses
        self.variable_dict = {"variable name": Variable()}

        # List of clauses which form the CNF
        self.clauses = 


    def load_dimacs(self, file):
        """Encode a dimacs file and add it to the clause list of this CNF_formula"""
        