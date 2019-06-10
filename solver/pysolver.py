import numpy as np
from iqutils import Grid, Piece
from timeit import default_timer as timer

def get_solutions(pieces, sol_path, log_path, starting_grid = Grid()):
    sol_file = open(sol_path, "w")
    log_file = open(log_path, "w")

    SOLUTIONS = []
    def recurse(grid, piece_to_add, x, y, orientation, other_remaining_pieces, k):
        # print("Adding " + piece_to_add.color + " to " + str((x, y)))
        # grid.cprint()
        # if piece_to_add.color == "lg":
        # 	grid.cprint()
        new_piece = piece_to_add.reorient(piece_to_add.orientations[orientation])
        xdim = new_piece.grid.shape[0]
        ydim = new_piece.grid.shape[1]
        if x + xdim <= 8 and y + ydim <= 8:
            grid.add_piece(piece_to_add, x, y, orientation)
            # if piece_to_add.color == "br":
            #     print()
            #     grid.cprint()
            #     print()
            # if piece_to_add.color == "pu":
            #     print()
            #     grid.cprint()
            #     print()
            log_file.write(">"*k + " " + piece_to_add.color + " " + str((x, y, orientation)) + "\n")
            if grid.good_grid() and not grid.has_hole() and not other_remaining_pieces:
                sol_num = len(SOLUTIONS)
                sol_file.write("Solution " + str(sol_num) + ":\n")
                sol_file.write(grid.grid_to_string() + "\n\n")
                log_file.write("! solution found\n")
                print("Solution " + str(sol_num))
                # grid.cprint()
                SOLUTIONS.append(grid)
            elif grid.good_grid() and not grid.has_hole():
                next_piece = other_remaining_pieces[0]
                for r in range(8):
                    for c in range(8):
                        for o in range(next_piece.max_orient):
                            # if next_piece.color == "pu":
                            #     print(r, c, o)
                            recurse(Grid(grid.grid, grid.colorgrid), next_piece, \
                            r, c, o, other_remaining_pieces[1:], k + 1)
    
    # NOTE: only go until row 3 cause anything after that is just a rotated
    # version of a previous solution (this is unique to the blue piece
    # which I am starting with)
    for r in range(8):
        for c in range(8):
            for o in range(pieces[0].max_orient):
                # NOTE: don't have to do multiple orientations of first piece since
                # we want unique solutions and all solutions with 
                # the first piece in any orientation other than 0 will simply be rotations
                # or reflections of a solution with the first piece in orientation 0
                message = pieces[0].color + " in row " + str(r) + ", column " + str(c) + ", orientation " + str(o)
                # message = "Piece 1 in row " + str(r) + ", column " + str(c)
                log_file.write(message + "\n")
                print(message)
                start = timer()
                # recurse(starting_grid, pieces[0], r, c, 0, pieces[1:], 1) # see note above
                recurse(Grid(starting_grid.grid, starting_grid.colorgrid), pieces[0], r, c, o, pieces[1:], 1)
                end = timer()
                print(">>> Process completed in " + str((end - start)/3600) + " hours")

    sol_file.close()
    log_file.close()
    
    return(SOLUTIONS)

BLUE = Piece([[1,1,1,0,0],[0,0,1,0,0],[0,0,1,1,1]], "bl")
BROWN = Piece([[1,1,1,1],[1,1,1,1]], "br")
ORANGE = Piece([[1,0,0],[1,0,0],[1,1,1]], "or")
DARKGREEN = Piece([[1,1,0],[1,1,1],[1,1,1]], "dg")
YELLOW = Piece([[1,0,0],[1,0,0],[1,0,0],[1,1,1]], "ye")
PINK = Piece([[1,1],[1,1],[1,0],[1,0]],"pi")
PURPLE = Piece([[1,1,1],[1,1,1],[1,0,0],[1,0,0]], "pu")
LIGHTGREEN = Piece([[1,1],[1,0],[1,0]],"lg")
WHITE = Piece([[1,1],[1,1],[1,0],[1,0],[1,0]], "wh")
AQUA = Piece([[1,1],[1,1],[1,0]], "aq")

PIECES = [BLUE, BROWN, PURPLE, WHITE, DARKGREEN, YELLOW, ORANGE, PINK, AQUA, LIGHTGREEN]

## 00, 01, 02, 10, 11, 12, 13, 20, 21, 22, 23

for r in range(3):
    for c in range(4):
        grid = Grid()
        grid.add_piece(BLUE, r, c, 0)
        extension = str(r) + "_" + str(c) + ".txt"
        solutions = get_solutions(PIECES[1:], "solutions_blue_in_" +  extension, \
            "log_blue_in_" + extension, grid)
