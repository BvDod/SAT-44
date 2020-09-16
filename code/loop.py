from classes.Solver import SAT_Solver
from statistics import mean


if __name__ == "__main__":
    
    # Set clause learning to False/True and set up sat_solver
    clause_learning = False

    heuristic = "PickFirst"  # Picks the first literal of the first active clause
    # heuristic = "LowestVar"        # Picks the active variable with the lowest int value
    # heuristic = "DLCS"
    # heuristic = "DLIS"
    # heuristic = "JeroslowWangOS"
    # heuristic = "JeroslowWangTS"

    # heuristic = "MOMS"
    k_factor = 1  # Set k_factor of MOMS heuristic

    solve_range = [1, 100]

    results = []

    for sudN in range(solve_range[0], solve_range[1]):
        
        Solver = SAT_Solver(clause_learning, heuristic)
        Solver.CNF.k_factor = k_factor
        Solver.CNF.load_dimacs_file("files/rules16x16.txt")
        Solver.CNF.load_sudoku_file("files/16x16.txt", sudN=sudN)
        Solver.solve_CNF()

        results.append([sudN, Solver.runtime])
    
    
    print("AVG time to solve: ", mean([result[1] for result in results]))