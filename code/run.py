from classes.Solver import SAT_Solver

if __name__ == "__main__":
    
    # Set clause learning to False/True and set up sat_solver
    clause_learning = False

    # heuristic = "pick-first"  # Picks the first literal of the first active clause
    heuristic = "LowestVar"        # Picks the active variable with the lowest int value

    Solver = SAT_Solver(clause_learning, heuristic)

    # Load rules and sudoku
    Solver.load_dimacs_file("files/rules16x16.txt")
    Solver.load_sudoku_file("files/16x16.txt")
    print()

    # Solve the sudoku and show the time it took
    Solver.solve_CNF()
    Solver.print_statistics()