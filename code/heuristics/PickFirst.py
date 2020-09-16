from iteration_utilities import first

def PickFirst(CNF):
    return abs(first(CNF.clauses[str(first(CNF.active_clauses))]))