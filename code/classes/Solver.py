from CNF import CNF_Formula
from DPLL import DPLL
import sys
import time

class SAT_Solver():
    
    def __init__(self):
        self.CNF = CNF_Formula()
        sys.setrecursionlimit(5000)
        # Use this in the future to counter iterations
        self.iterations_counter = 0

        # Are we currently backtracking?
        self.backtracking = False
        self.backtracking_depth = None
    
    def load_dimacs_file(self, file):
        self.CNF.load_dimacs_file(file)
    
    def load_sudoku_file(self, file):
        self.CNF.load_sudoku_file(file)
    
    def print_CNF_status(self):
        self.CNF.print_status()

    def solve_CNF(self):
        self.CNF.remove_pure_literals()
        self.CNF.build_unit_clauses_list()
        self.CNF.remove_unit_clauses()
        

        result = DPLL(self)
        if result == "SAT":
            print("\nSAT!")
            self.print_answer()
        else:
            print(result)
    
    def print_answer(self):
        self.CNF.print_answer()
        

if __name__ == "__main__":
    
    Solver = SAT_Solver()
    Solver.load_dimacs_file("files/rules.txt")
    Solver.load_sudoku_file("files/9x9.txt")
    # Solver.load_sudoku_file("files/hard.txt")
    print()
    before = time.time()
    Solver.solve_CNF()
    # Solver.CNF.print_total_status()
    print("Time:", time.time() - before)
