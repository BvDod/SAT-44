import argparse
from classes.Solver import SAT_Solver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dimacs", '-d', type=str, help="The input dimacs file. Can either be rules+sudoku or just the rules.", required = True)
    parser.add_argument("--strategy", '-s', type=int, help="The number of the strategy to use", required = True)
    parser.add_argument("--sudoku_dimacs", '-i', type=str, help="Sudoku dimacs input file")
    parser.add_argument("--sudoku_unencoded", '-u', type=str, help="Optional unencoded sudoku file (non-dimacs)")

    args = parser.parse_args()

    strategies = {
        1: "PickFirst",  # Picks the first literal of the first active clause
        2: "LowestVar",        # Picks the active variable with the lowest int value
        3: "DLCS",
        4: "DLIS",
        5: "JeroslowWangOS",
        6: "JeroslowWangTS",
        7: "Random",
        8: "MOMS"}

    
    clause_learning = False
    k_factor = 0.2

    if args.strategy not in strategies:
        print("invalid strategy number")
        exit()
    heuristic = strategies[args.strategy]


    Solver = SAT_Solver(clause_learning, heuristic)
    Solver.CNF.k_factor = k_factor

    Solver.CNF.load_dimacs_file(args.dimacs)
    
    if args.sudoku_unencoded:
        Solver.CNF.load_sudoku_file(args.sudoku_unencoded)
    
    if args.sudoku_dimacs:
        Solver.CNF.load_dimacs_file(args.sudoku_dimacs)
   
    # Solve the sudoku and show the time it took
    Solver.solve_CNF()
    Solver.print_statistics()

    # Dump answer to out file.
    Solver.dump_answer(args.dimacs)
