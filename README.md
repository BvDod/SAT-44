# SAT-44
We need to remember to document: the important design decisions for your SAT solver (both how and why)

## TODO
#### Now (ish)
- Read dimac and construct CNF structure
- Translating sudoku into a CNF readable form
      Check code file SudToCNF.py for an implementation. Command line : python SudToCNF.py Path\To\SudokuFile.txt
      If you want to test a file easily, put it in the same folder as the code. Don't forget the ".txt" at the end of your file.
      I've tested it on 4x4.txt, 16x16.txt and damnhard.sdk.txt. Feel free to ask questions. - Jade

- Basic SAT Solver <- divide into sub-task!!
- Recursive vs iterative (Jade!?!?)
      If we can do one, we can do the other. Final decision should probably be made based on our experiment. - Jade

- Decide which heuristics/ type of SAT solver we would like to make.

#### Future
- Create a hypothesis (plus motivation why it is interesting and plausible)
- Your experimental design (which experimental conditions do you test, which test set do you use, which metrics are you measuring, and why)
- Your experimental results (consider including plots or graphs or bar charts, and to test for statistical significance of your results)
- The conclusion about your hypothesis that you draw from your results (and why)




