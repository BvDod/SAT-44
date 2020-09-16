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

        # Implication graph info
        self.by_branch = None
        self.set_depth = None
        self.caused_by_clause_id = None