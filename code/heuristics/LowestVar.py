from iteration_utilities import first


def LowestVar(CNF):
    
    lowest_var = abs(first(CNF.clauses[str(first(CNF.active_clauses))]))
    for clause_id in CNF.active_clauses:
        for literal in CNF.clauses[str(clause_id)]:
            if abs(literal) < lowest_var:
                lowest_var = abs(literal)
    return lowest_var