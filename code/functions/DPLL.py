import copy

def DPLL(sat_solver):
    """Function which exexcuts the DPLL algorithm for the SAT solver"""

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

        # Pick variable
        variable, first_boolean = sat_solver.CNF.pick_active_variable(sat_solver.heuristic)
        
        if first_boolean == True:
            boolean_order = [True, False]
        else: 
            boolean_order = [False, True]

        # Try both True and False
        for boolean in boolean_order:

            # Branch 
            sat_solver.CNF.branch(variable, boolean)
            sat_solver.branch_counter += 1
            sat_solver.CNF.remove_unit_clauses()

            # No clauses left 
            if not sat_solver.CNF.active_clauses:
                return "SAT"
            
            # check_if_empty_clause
            empty_clause = sat_solver.CNF.contains_empty_clause()
            if empty_clause:

                # If clause_learning enabled
                if sat_solver.clause_learning:
                   
                    conflict_id = empty_clause
                    
                    # Learn clause and start backtracking
                    backtrack_depth = sat_solver.CNF.learn_clause(conflict_id)
                    sat_solver.clauses_learned += 1
                
                    sat_solver.backtracking = True
                    sat_solver.backtracking_depth = backtrack_depth

                    sat_solver.CNF.undo_unit_clauses()
                    sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                    
                    # If we have to backtrack at depth 0, go back to top of current function
                    if sat_solver.CNF.current_depth == 0:
                        sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                        sat_solver.CNF.undo_unit_clauses()

                        sat_solver.backtracking = False
                        sat_solver.backtrack_depth = None
                        restart = True
                        break

                    return "UNSAT"
                
                # If clause learning disabled
                else:
                    sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                    sat_solver.CNF.undo_unit_clauses()
                    continue
            
            # Recursive call
            sat_solver.CNF.current_depth += 1
            result = DPLL(sat_solver)
            sat_solver.CNF.current_depth -= 1
            
            # If backtracking, go up a depth
            if sat_solver.backtracking:
                print("Backtracking to: ", sat_solver.CNF.current_depth)
                sat_solver.CNF.undo_branch(sat_solver.CNF.current_depth)
                sat_solver.CNF.undo_unit_clauses()
                sat_solver.depths_backtracked += 1

                # Stop backtracking if depth reached
                if sat_solver.backtracking_depth == sat_solver.CNF.current_depth:
                   
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
                return "UNSAT"
            continue

        # If both True and False failed, branch is not possible
        sat_solver.CNF.undo_unit_clauses()
       
        return "UNSAT"