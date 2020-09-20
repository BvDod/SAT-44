from classes.Solver import SAT_Solver

if __name__ == "__main__":
    
    # Set clause learning to False/True and set up sat_solver
    clause_learning = False

    # heuristic = "PickFirst"  # Picks the first literal of the first active clause
    # heuristic = "LowestVar"        # Picks the active variable with the lowest int value
    # heuristic = "DLCS"
    # heuristic = "DLIS"
    # heuristic = "JeroslowWangOS"
    # heuristic = "JeroslowWangTS"
    heuristic = "Random"
    
    # heuristic = "MOMS"
    k_factor = 1  # Set k_factor of MOMS heuristic

    Solver = SAT_Solver(clause_learning, heuristic)
    Solver.CNF.k_factor = 0.3

    # Load rules and sudoku
    Solver.CNF.load_dimacs_file("files/rules/9x9-effi.txt")
    Solver.CNF.load_sudoku_file("files/sudokus/9x9.txt")
   
    # Solve the sudoku and show the time it took
    Solver.solve_CNF()
    Solver.print_answer()
    Solver.print_statistics()