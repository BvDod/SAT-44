
def JeroslowWangOS(CNF):
    var_with_highest_J = None
    highest_J = 0

    for var in CNF.variable_dict:
        variable = CNF.variable_dict[var]
        J = 0
        
        for clause_id in variable.occurs_negated_in:
            J += 2**(-len(CNF.clauses[str(clause_id)]))
        
        for clause_id in variable.occurs_positive_in:
            J += 2**(-len(CNF.clauses[str(clause_id)]))
        
        if J > highest_J:
            highest_J = J
            var_with_highest_J = variable.variable_name

    # One-sided
    boolean = True
    
    return int(var_with_highest_J), boolean