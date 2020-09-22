from classes.Solver import SAT_Solver
from statistics import mean, stdev
import winsound
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    # Set clause learning to False/True and set up sat_solver
    clause_learning = True

    # heuristic = "PickFirst"  # Picks the first literal of the first active clause
    # heuristic = "LowestVar"        # Picks the active variable with the lowest int value
    # heuristic = "DLCS"
    # heuristic = "DLIS"
    # heuristic = "JeroslowWangOS"
    heuristic = "JeroslowWangTS"
    # heuristic = "Random"

    # heuristic = "MOMS"
    k_factor = 0.2  # Set k_factor of MOMS heuristic

    solve_range = [1, 51]

    rule_file = "files/rules/9x9-efficient.txt"
    results = []
    branches = []
    

    for sudN in range(solve_range[0], solve_range[1]):
        
        Solver = SAT_Solver(clause_learning, heuristic)
        Solver.CNF.k_factor = k_factor
        Solver.CNF.load_dimacs_file(rule_file)
        Solver.CNF.load_sudoku_file("files/sudokus/9x9.txt", sudN=sudN)
        Solver.solve_CNF()

        results.append([sudN, Solver.runtime])
        branches.append(Solver.branch_counter)
        Solver.print_statistics()
    
    print("Heuristic: ", heuristic)
    print(rule_file)
    
    
    print("AVG time to solve: ", mean([result[1] for result in results]))
    print("Standard_dev: ", stdev([result[1] for result in results]))
    print("AVG branches: ", mean(branches))
    print("Standard_dev: ", stdev(branches))
    print(clause_learning)

    frequency = 500 # Set Frequency To 2500 Hertz
    duration = 700  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=[result[1] for result in results], bins=40, color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Time in seconds')
    plt.ylabel('Frequency')

    plt.show()

    for result in results:
        print(result[1])