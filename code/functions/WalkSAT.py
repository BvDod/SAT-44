import random
import copy

# TRY DIFFERENT P VALUES

def WalkSAT (CNF,p=1):
    # Collects all clauses to classify them as unsatisfied and keep track of those
    unsatisfied_clauses = CNF.clauses.copy()
    satisfied_clauses = {}

    stop = 0

    print(len(satisfied_clauses))
    print(len(CNF.clauses))

    # Set all variables to random boolean values
    for variable in CNF.variable_dict :
        CNF.variable_dict[variable].boolean = bool(random.getrandbits(1))

    # Makes list of satisfied and unsatisfied clauses
    for variable in CNF.variable_dict :
        if CNF.variable_dict[variable].boolean == True :
            for clause in CNF.variable_dict[variable].occurs_positive_in :
                if str(clause) not in satisfied_clauses :
                    satisfied_clauses[str(clause)] = []
                satisfied_clauses[str(clause)].append(variable)
                if str(clause) in unsatisfied_clauses :
                    unsatisfied_clauses.pop(str(clause))
        else :
            for clause in CNF.variable_dict[variable].occurs_negated_in :
                if str(clause) not in satisfied_clauses :
                    satisfied_clauses[str(clause)] = []
                satisfied_clauses[str(clause)].append(variable)
                if str(clause) in unsatisfied_clauses :
                    unsatisfied_clauses.pop(str(clause))
    
    # Can be used to find the best answer if necessary ... maybe
    best_answer = CNF.variable_dict.copy()
    best_stat = len(satisfied_clauses)

    while unsatisfied_clauses :

        # Choose random unsatisfied clause
        clause = random.choice(list(unsatisfied_clauses.keys()))

        # Choose best variable from clause or random variable if p involved AND flips its value
        if p > 0 and random.uniform(0,1) < p :
            var = random.choice(list(unsatisfied_clauses[str(clause)]))
            CNF.variable_dict[str(abs(var))].boolean = not CNF.variable_dict[str(abs(var))].boolean
        else :
            max_unsat = len(CNF.clauses)
            var = None
            for variable in unsatisfied_clauses[str(clause)] :
                unsat = 0
                if CNF.variable_dict[str(abs(variable))].boolean :
                    for cl in CNF.variable_dict[str(abs(variable))].occurs_positive_in :
                        if satisfied_clauses[str(cl)] == [var] :
                            unsat = unsat + 1
                else :
                    for cl in CNF.variable_dict[str(abs(variable))].occurs_negated_in :
                        if satisfied_clauses[str(cl)] == [var] :
                            unsat = unsat + 1
                if unsat < max_unsat :
                    var = abs(variable)
                    max_unsat = unsat
            CNF.variable_dict[str(var)].boolean = not CNF.variable_dict[str(var)].boolean

        # Puts satisfied and unsatisfied in right dictionary
        var = str(abs(var))
        if CNF.variable_dict[var].boolean == True :
            for clause in CNF.variable_dict[var].occurs_positive_in :
                if str(clause) not in satisfied_clauses :
                    satisfied_clauses[str(clause)] = []
                satisfied_clauses[str(clause)].append(var)
                if str(clause) in unsatisfied_clauses :
                    unsatisfied_clauses.pop(str(clause))
            for clause in CNF.variable_dict[var].occurs_negated_in :
                satisfied_clauses[str(clause)].remove(var)
                if satisfied_clauses[str(clause)] == [] :
                    satisfied_clauses.pop(str(clause))
                    unsatisfied_clauses[str(clause)] = CNF.clauses[str(clause)].copy()

        else :
            for clause in CNF.variable_dict[var].occurs_negated_in :
                if str(clause) not in satisfied_clauses :
                    satisfied_clauses[str(clause)] = []
                satisfied_clauses[str(clause)].append(var)
                if str(clause) in unsatisfied_clauses :
                    unsatisfied_clauses.pop(str(clause))
            for clause in CNF.variable_dict[var].occurs_positive_in :
                satisfied_clauses[str(clause)].remove(var)
                if satisfied_clauses[str(clause)] == [] :
                    satisfied_clauses.pop(str(clause))
                    unsatisfied_clauses[str(clause)] = CNF.clauses[str(clause)].copy()
                      
        # Helps you make it stop
        stop = stop + 1
        #print(len(satisfied_clauses))
        if len(satisfied_clauses) > best_stat :
            best_stat = len(satisfied_clauses)
            best_answer = CNF.variable_dict.copy()
    
    # Print whatever you want
    print(len(satisfied_clauses))
    #print(stop)
    CNF.print_answer()
    print(len(unsatisfied_clauses))
    #print(unsatisfied_clauses)