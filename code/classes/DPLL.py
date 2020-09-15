import copy
from CNF import CNF_Formula

# Pseudocode for DPLL recursive
def DPLL(sat_solver):

    # No clauses left 
    if not sat_solver.CNF.active_clauses:
        return "SAT"

    # The loop is so we can restart here after backtracking
    restart = True
    while restart == True:
        restart = False
       
         # No clauses left 
        if not sat_solver.CNF.active_clauses:
            return "SAT"

        """
        if sat_solver.CNF.current_depth == 4:
            sat_solver.backtracking = True
            sat_solver.backtrack_depth = 0
            sat_solver.CNF.print_total_status()
            return
        """
    
        # Pick variable
        # sat_solver.CNF.print_total_status()
        variable = sat_solver.CNF.pick_active_variable("lowest")
        # print(variable)
        # Try both True and False
        for boolean in (True, False):

            # Branch 
            sat_solver.CNF.branch(variable, boolean)
            sat_solver.CNF.remove_unit_clauses()

            # sat_solver.CNF.print_total_status()

            # No clauses left 
            if not sat_solver.CNF.active_clauses:
                return "SAT"
            
            # check_if_empty_clause
            empty_clause = sat_solver.CNF.contains_empty_clause()
            if empty_clause:
                # print(sat_solver.CNF.clauses_removed_part[str(empty_clause)])
                conflict_id = empty_clause
                
                # Learn clause and start backtracking
                backtrack_depth = sat_solver.CNF.learn_clause(conflict_id)
                
                sat_solver.backtracking = True
                sat_solver.backtracking_depth = backtrack_depth

                sat_solver.CNF.undo_unit_clauses()
                sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                
                if sat_solver.CNF.current_depth == 0:
                    sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                    sat_solver.CNF.undo_unit_clauses()

                    sat_solver.backtracking = False
                    sat_solver.backtrack_depth = None
                    restart = True
                    break

                return "UNSAT 1"
            
            # Recursive call
            sat_solver.CNF.current_depth += 1
            result = DPLL(sat_solver)
            sat_solver.CNF.current_depth -= 1
            
            if sat_solver.backtracking:
                print("backtracking: ", sat_solver.CNF.current_depth)
                sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                sat_solver.CNF.undo_unit_clauses()
                

                # Stop backtracking if depth reached
                if sat_solver.backtracking_depth == sat_solver.CNF.current_depth:
                    print("done")
                    sat_solver.backtracking = False
                    sat_solver.backtrack_depth = None
                    

                    # Go to the top of the function
                    restart = True
                    break

                # Go one level up
                return

            if result == "SAT":
                return "SAT"
            
            # Undo branching
            sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
            sat_solver.CNF.undo_unit_clauses()

        # If last step of backtracking, go back to top of function
        if restart == True:
            sat_solver.CNF.remove_unit_clauses()
            if sat_solver.CNF.contains_empty_clause():
                return "UNSAT 2"
            continue

        # If both True and False failed, branch is not possible
        sat_solver.CNF.undo_unit_clauses()
        print("wtf")
        return "UNSAT 2"