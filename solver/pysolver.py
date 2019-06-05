import numpy as np
from setup import Grid, Piece
from timeit import default_timer as timer

def get_solutions(pieces, sol_path, log_path):
    sol_file = open(sol_path, "w")
    log_file = open(log_path, "w")
    sol_num = 0
    
    SOLUTIONS = []
    
    def recurse(grid, piece_to_add, x, y, orientation, other_remaining_pieces, k):
        # print("Adding " + piece_to_add.color + " to " + str((x, y)))
        # grid.cprint()
        new_piece = piece_to_add.reorient(piece_to_add.orientations[orientation])
        xdim = new_piece.grid.shape[0]
        ydim = new_piece.grid.shape[1]
        if x + xdim <= 8 and y + ydim <= 8:
            grid.add_piece(piece_to_add, x, y, orientation)
            log_file.write(">"*k + " " + piece_to_add.color + " " + str((x, y, orientation)) + "\n")
            if grid.good_grid() and not other_remaining_pieces:
                sol_file.write("Solution " + str(sol_num) + ":\n")
                sol_file.write(grid.grid_to_string() + "\n\n")
                print("Solution " + str(sol_num))
                grid.cprint()
                SOLUTIONS.append(grid)
                sol_num += 1
            elif grid.good_grid():
                next_piece = other_remaining_pieces[0]
                for r in range(8):
                    for c in range(8):
                        if grid.empty_space(r, c):
                            for o in range(next_piece.max_orient):
                                new_grid = Grid(grid.grid, grid.colorgrid)
                                recurse(new_grid, next_piece, r, c, o, other_remaining_pieces[1:], k + 1)
    
    for r in range(8):
        for c in range(8):
        	# NOTE: don't have to do multiple orientations of first piece since
        	# we want unique solutions and all solutions with 
        	# the first piece in any orientation other than 0 will simply be rotations
        	# or reflections of a solution with the first piece in orientation 0
        	message = "Piece 1 in row " + str(r) + ", column " + str(c)
        	log_file.write(message + "\n")
        	print(message)
        	start = timer()
        	recurse(Grid(), pieces[0], r, c, 0, pieces[1:], 1) # see note above
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

PIECES = [BLUE, BROWN, PURPLE, WHITE, DARKGREEN, YELLOW, ORANGE, PINK, LIGHTGREEN, AQUA]

solutions = get_solutions(PIECES, "solutions.txt", "log.txt")

