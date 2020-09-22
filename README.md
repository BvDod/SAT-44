# SAT solver project - Group 44

## How to run
You can run the SAT solver by running the python file /code/SAT.py after making sure all dependencies in requirements.txt are installed.
The file can be run in the following way: 

~ python SAT.py -d rule_dimacs.txt -s strategy_int -i sud_dimacs.txt -u sud_unencoded.txt

-d : The input dimacs file, most likely used for the rules

-i : Sudoku dimacs input file

-u : Optional unencoded sudoku file (non-dimacs)

-s : The number of the strategy to use

The following strategies are available using -s:

1: "PickFirst",  # Picks the first literal of the first active clause

2: "LowestVar",  # Picks the active variable with the lowest int value

3: "DLCS",

4: "DLIS",

5: "JeroslowWangOS",

6: "JeroslowWangTS",

7: "Random",

8: "MOMS"}

Clause learning can be enable/ disabled by setting clause_learning to either True or False in SAT.py. The k used by moms can also be changed by changing k_factor to a different int.

### Heuristics:
You can find the heuristics under /code/heuristics/

## Constructed rule-files
The different implemented rule files were created using /code/make-rules.py and can be found under code/files/rules/
The following rule_files were created:
- 9x9 minimal
- 9x9 efficient
- 9x9 extended
- 16x16 minimal
- 16x16 efficient
- 16x16 extended


