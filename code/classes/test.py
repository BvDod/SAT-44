if bcp:
    varialbe.depth_set = current_depth
    by_branch = False
    bcp_clause = clause_id
    caused_by_vars = [variables for abs(variables) in self.clauses[bcp_clause]]

if branch:
    varialbe.depth_set = current_depth
    by_branch = False


clauses_with_removed_literals = dict()


if clause == empty:
    partial_learned = clauses_with_removed_literals[clause_id]
    while count_decision_level(partial_learned) != 1:
        for variable in partial_learned:
            if not variable.bcp and depth=current_depth:
                variable_to_expand = variable
                break
        partial_learned.append(variable.bcp_clause())
        simplify partial_learned
    
    backtrack_depth = min([variable for variable in partial_learned if variable.by_branch = True], key = lambda depth: depth.depth_set).depth_set
    
    backtrack(backtrack_depth)

change remove 
change undo