from CNF import CNF_Formula
from DPLL import DPLL
import sys

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
        print(DPLL(self))
        print("Satisfying assignment: ")
        self.CNF.print_assignments()


if __name__ == "__main__":
    
    Solver = SAT_Solver()
    Solver.load_dimacs_file("test.txt")
    Solver.CNF.print_total_status()
    Solver.solve_CNF()
