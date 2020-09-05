# File containing classes to represents a CNF formula

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


    def load_dimacs(self, file):
        """Encode a dimacs file and add it to the clause list of this CNF_formula"""
        
        with open(file, "r") as dimacs:
            
            # Every line is a clause
            for line in dimacs:

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

    # Prints all clauses of the CNF
    def print_clauses(self):
        for clause in self.clauses:
            print(clause)  


     
if __name__ == "__main__":
    
    CNF = CNF_Formula()
    CNF.load_dimacs("rules.txt")

    # doesnt fit in console ):
    # Uncomment to print
    # CNF.print_clauses()
    
    print(f"Variables: {len(CNF.variable_dict)}, Clauses: {len(CNF.clauses)}")