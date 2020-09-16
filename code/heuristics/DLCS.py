# Pick the variable which has the highest sum(occurs_negated, occurs_positive)
# The boolean to pick is based if its exists more in negated or positve form

def DLCS(CNF):
    most_occuring_var = None
    most_occuring_count = 0

    for var in CNF.variable_dict:
        variable = CNF.variable_dict[var]
        var_count = len(variable.occurs_negated_in) + len(variable.occurs_positive_in)
        if var_count > most_occuring_count:
            most_occuring_var = variable.variable_name
            most_occuring_count = var_count

    # If it occurs more positive than negated
    if len(CNF.variable_dict[str(most_occuring_var)].occurs_positive_in) >= len(CNF.variable_dict[str(most_occuring_var)].occurs_negated_in):
        boolean = True
    
    # Occurs more negated than positive
    else:
        boolean = False
 
    return int(most_occuring_var), boolean