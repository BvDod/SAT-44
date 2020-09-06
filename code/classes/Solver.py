from CNF import CNF_Formula


class SAT_Solver():
    
    def __init__(self):
        self.CNF = CNF_Formula()

        # Use this in the future to counter iterations
        self.iterations_counter = 0
    
    def load_dimacs_file(self, file):
        self.CNF.load_dimacs_file(file)
    
    def load_sudoku_file(self, file):
        self.CNF.load_sudoku_file(file)
    
    def print_CNF_status(self):
        self.CNF.print_status()

    def solve_CNF(self):
        pass


if __name__ == "__main__":
    
    Solver = SAT_Solver()
    Solver.load_dimacs_file("rules.txt")
    Solver.load_sudoku_file("4x4.txt")
    Solver.print_CNF_status()