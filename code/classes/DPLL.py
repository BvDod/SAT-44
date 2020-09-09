import copy

# Pseudocode for DPLL recursive
def DPLL(sat_solver):

    # No clauses left TODO: is this one needed?
    if not sat_solver.CNF.clauses:
        return "SAT"
    
    # Contains an empty clause
    if sat_solver.CNF.contains_empty_clause():
        print("unsat")
        return "UNSAT"


    sat_solver.CNF.remove_tautologies()
    sat_solver.CNF.remove_unit_clauses()
    sat_solver.CNF.remove_pure_literals()
   
    variable = sat_solver.CNF.pick_variable()

    for boolean in (True, False):
        changes_made = sat_solver.CNF.branch(variable, boolean)

        # recursive function call
        result = DPLL(sat_solver)
        if result == "SAT":
            return "SAT"

        sat_solver.CNF.undo_branch(changes_made)
    
    # Undo changes you made to CNF
    sat_solver.CNF.undo_simplify_changes.
    
    return "UNSAT"