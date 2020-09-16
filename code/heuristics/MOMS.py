from iteration_utilities import first

def MOMS(CNF):
    k = CNF.k_factor


    smallest_len = len(CNF.clauses[str(first(CNF.active_clauses))])
    smallest_clauses = []
    
    for clause_id in CNF.active_clauses:
        if len(CNF.clauses[str(clause_id)]) < smallest_len:
            smallest_len = len(CNF.clauses[str(clause_id)])
            smallest_clauses = []
        
        if len(CNF.clauses[str(clause_id)]) == smallest_len:
            smallest_clauses.append(clause_id)

    var_counts = {}

    for clause_id in smallest_clauses:
        for literal in CNF.clauses[str(clause_id)]:
            if not abs(literal) in var_counts:
                var_counts[abs(literal)] = [0, 0]
            
            if literal > 0:
                var_counts[abs(literal)][0] += 1
            elif literal < 0:
                var_counts[abs(literal)][1] += 1
    
    highest_S = 0
    highest_var = None
    boolean = None

    for var in var_counts:
        Fn = var_counts[var][0]
        Fp = var_counts[var][1]

        S = (Fn + Fp) * 2**k + (Fn * Fp)

        if S > highest_S:
            highest_S = S
            highest_var = var
            
            if Fn > Fp:
                boolean = False
            else:
                boolean = True
    
    return highest_var, boolean

        