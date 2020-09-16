from classes.CNF import CNF_Formula
from functions.DPLL import DPLL
import sys
import time
from time import perf_counter

class SAT_Solver():
    
    def __init__(self, clause_learning, heuristic):
        self.CNF = CNF_Formula()
        sys.setrecursionlimit(5000)
        
        # Statistics
        self.branch_counter = 0
        self.runtime = 0
        self.clauses_learned = 0
        self.depths_backtracked = 0
        
        # Heuristic used in picking variables
        self.heuristic = heuristic

        # Are we currently backtracking?
        self.backtracking = False
        self.backtracking_depth = None

        # Run the dpll with or without clause learning
        self.clause_learning = clause_learning
    
    def load_dimacs_file(self, file):
        """ Used to load dimacs file into the CNF"""
        self.CNF.load_dimacs_file(file)
    
    def load_sudoku_file(self, file):
        """Used to select and load a sudoku"""
        self.CNF.load_sudoku_file(file)


    def solve_CNF(self):
        """ Function used to run the DPLL algo used to try to solve the CNF"""
        
        # Tautologies dont exist in properly a properly made sudoku CNF, thus we keep this disabled
        # self.CNF.remove_tautologies
        # self.CNF.remove_pure_literals()
        self.CNF.build_unit_clauses_list()

        # Build initial list with unit clauses.
        self.CNF.remove_unit_clauses()
        
        # Run the DPLL algo and check runtime
        before = perf_counter()
        result = DPLL(self)
        self.runtime = perf_counter() - before

        if result == "SAT":
            print("\nSAT!")
            self.print_answer()
        else:
            print(result)
    
    def print_answer(self):
        """ Only prints the booleans interesting for sudoku: for full print use: CNF.print_assignments()"""
        self.CNF.print_answer()
    
    def print_statistics(self):

        print("Runtime: {:8f}".format(self.runtime))
        print("Times branched: ", self.branch_counter)
        print("Unit clauses removed: : ", self.CNF.unit_clause_counter)
    
        
        if self.clause_learning:
            print("Clauses learned/ Conflicts: ", self.clauses_learned)
            print("Total branches backtracked: ", self.depths_backtracked)
