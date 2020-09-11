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
    
    def load_dimacs_file(self, file):
        self.CNF.load_dimacs_file(file)
    
    def load_sudoku_file(self, file):
        self.CNF.load_sudoku_file(file)
    
    def print_CNF_status(self):
        self.CNF.print_status()

    def solve_CNF(self):
        self.CNF.remove_pure_literals()
        self.CNF.remove_tautologies()
        
        if DPLL(self) == "SAT":
            print("SAT!")
            self.print_answer
        else:
            print("UNSAT")
    
    def print_answer(self):
        self.CNF.print_answer()
        

if __name__ == "__main__":
    
    Solver = SAT_Solver()
    Solver.load_dimacs_file("rules.txt")
    Solver.load_sudoku_file("9x9.txt")
    before = time.time()
    Solver.solve_CNF()
    Solver.print_answer()
    print("Time:", time.time() - before)
