import os
from math import sqrt




if __name__ == "__main__":


    # Length of your sudoku
    # Should work with other size than 9? didnt test though
    size = 9

    # Define if cell, row, column and block definedness and uniqueness are enabled
    # Combine these settings to make the different types of sudoku rule encodings
    cell_def = True
    cell_uni = True

    row_def = True
    row_uni = True

    col_def = True
    col_uni = True

    block_def = True
    block_uni = True
    


    rules = []

    for row in range(1, size+1):

        for column in range(1, size+1):
            
            if cell_def:
                # Cell definedness
                clause = []
                for integer in range(1, size+1):
                    clause.append(f"{row}{column}{integer}")
                rules.append(clause)

            if cell_uni:
                # Cell uniqueness
                for integer in range(1, size+1):
                    for integer2 in range(integer+1, size+1):
                        clause = []
                        clause.append(f"-{row}{column}{integer}")
                        clause.append(f"-{row}{column}{integer2}")
                        rules.append(clause)

    for row in range(1, size+1):
        for integer in range(1, size+1):
            
            if row_def:
                # Row defideness
                clause = []
                for column in range(1, size+1):
                    clause.append(f"{row}{column}{integer}")
                rules.append(clause)

            if row_uni:
                # row Uniqueness
                for column in range(1, size+1):
                    for column2 in range(column+1, size+1):
                        clause = []
                        clause.append(f"-{row}{column}{integer}")
                        clause.append(f"-{row}{column2}{integer}")
                        rules.append(clause)
    
    for column in range(1, size+1):
        for integer in range(1, size+1):
            
            if col_def:
                # column defidenes
                clause = []
                for row in range(1, size+1):
                    clause.append(f"{row}{column}{integer}")
                rules.append(clause)

            if col_uni:
                # row Uniqueness
                for row in range(1, size+1):
                    for row2 in range(row+1, size+1):
                        clause = []
                        clause.append(f"-{row}{column}{integer}")
                        clause.append(f"-{row2}{column}{integer}")
                        rules.append(clause)
    

    blocks = int(sqrt(size))

    for block_x in range(0, blocks):
        for block_y in range(0, blocks):
        
                for integer in range(1, size+1):
                    
                    # Block defidness
                    if block_def:
                        clause = []
                        for row in range(1, blocks+1):
                            row = (block_x * blocks) + row
                            for column in range(1, blocks+1):
                                column = (block_y * blocks) + column
                                clause.append(f"{row}{column}{integer}")
                        rules.append(clause)
                    
                    
                    # Block uniqueness
                    if block_uni:
                        for row in range(1, blocks+1):
                                
                                for column in range(1, blocks+1):
                                    
                                    
                                    start_row = row
                                    if column + 1 > blocks:
                                        start_row += 1
                                    else:
                                        start_column = column + 1

                                    for row2 in range(start_row, blocks+1):
                                        for column2 in range(start_column, blocks+1):
                                            
                                            row_value = (block_x * blocks) + row
                                            column_value = (block_y * blocks) + column
                                            
                                            row2_value = (block_x * blocks) + row2
                                            column2_value = (block_y * blocks) + column2

                                            clause = []
                                            clause.append(f"-{row_value}{column_value}{integer}")
                                            clause.append(f"-{row2_value}{column2_value}{integer}")
                                            rules.append(clause)
                                            start_column = 1

                                        start_row = 1
                    
        
            
    
    # Write all found rule clauses in a file
    with open("9x9-extended.txt", "w+") as rules_file:
        for clause in rules:
            string = ""
            for literal in clause:
                string += literal + " "
            string += "0\n"
            rules_file.write(string)