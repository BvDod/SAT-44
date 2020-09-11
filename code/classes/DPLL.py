import copy
from CNF import CNF_Formula

# Pseudocode for DPLL recursive
def DPLL(sat_solver):

    sat_solver.CNF.remove_unit_clauses()

    # No clauses left 
    if not sat_solver.CNF.active_clauses:
        return "SAT"
    
    # Contains an empty clause
    if sat_solver.CNF.contains_empty_clause():
        sat_solver.CNF.undo_unit_clauses()
        return "UNSAT"

    # Pick variable
    variable = sat_solver.CNF.pick_active_variable("pick-first")

    # Try both True and False
    for boolean in (True, False):

        # Branch 
        sat_solver.CNF.branch(variable, boolean)
        
        sat_solver.CNF.current_depth += 1
        
        # Recursive call
        result = DPLL(sat_solver)
        sat_solver.CNF.current_depth -= 1
        
        if result == "SAT":
            return "SAT"
        
        # Undo branching
        sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
        
    # If both True and False failed, branch is not possible
    sat_solver.CNF.undo_unit_clauses()
    return "UNSAT"