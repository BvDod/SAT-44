import copy
from CNF import CNF_Formula

# Pseudocode for DPLL recursive
def DPLL(sat_solver):

    if sat_solver.CNF.current_depth == 5 and sat_solver.no_b_yet:
        sat_solver.no_b_yet = False
        sat_solver.currently_backtracking = True
        sat_solver.backtrack_depth = 0
        return
    

    print(sat_solver.CNF.current_depth)
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
        
        if sat_solver.CNF.current_depth == 0:
            sat_solver.CNF.print_total_status()
        sat_solver.CNF.current_depth += 1
        
        # Recursive call
        sat_solver.total_branches += 1
        result = DPLL(sat_solver)
        sat_solver.CNF.current_depth -= 1

        # Check if in backtracking mode and backtrack
        if sat_solver.currently_backtracking:
            print("backtracking: ", sat_solver.CNF.current_depth)
            sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
            sat_solver.CNF.undo_unit_clauses()
            
            # Stop backtracking if depth reached
            if sat_solver.backtrack_depth + 1 == sat_solver.CNF.current_depth:
                sat_solver.currently_backtracking = False
                sat_solver.CNF.print_total_status()
                exit()
            # Go one level up
            return
        
        if result == "SAT":
            return "SAT"
        
        # Undo branching
        sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
        
    # If both True and False failed, branch is not possible
    sat_solver.CNF.undo_unit_clauses()
    return "UNSAT"