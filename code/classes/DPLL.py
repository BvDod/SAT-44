# Pseudocode for DPLL recursive
def DPLL(CNF):

    if CNF.clauses has no clauses left:
        return sat
    if CNF.clases contains empty clause:
        return unsat
    
    # Simplify CNF
    remove tautologies
    remove units
    remove pure literals
    
    # Pick variable to "branch"
    pick a variable

    for boolean in (True, False):
        set variable to boolean
        split_CNF()
        remove all clauses were one is now true
        # recursive function call
        result = DPLL(CNF)
        if result = SAT:
            return sat
        undo removing clauses
    
    # Undo changes you made to CNF
    reset picked variable to None
    undo remove_taunts
    undo remove units
    undo remove pure literals
    
    return unsat