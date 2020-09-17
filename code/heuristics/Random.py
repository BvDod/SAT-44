import random

def Random(CNF):
    
    var_list = set()
    for clause_id in CNF.active_clauses:
        for literal in CNF.clauses[str(clause_id)]:
            if abs(literal) not in var_list:
                var_list.add(abs(literal))
    
    random_boolean = random.choice([True, False])
    random_var = random.choice(tuple(var_list))
    
    return random_var, random_boolean