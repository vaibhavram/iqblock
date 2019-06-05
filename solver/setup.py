import numpy as np

class Grid:
    
    def __init__(self, grid = [[0]*8]*8, colorgrid = [["--"]*8]*8):
        self.grid = np.array(grid, dtype = np.int)
        self.colorgrid = np.array(colorgrid, dtype = object)
        
    def add_piece(self, piece, x, y, orientation_index):
        assert (orientation_index < piece.max_orient), "Orientation exceeds number of orientations"
        new_piece = piece.reorient(piece.orientations[orientation_index])
        xdim = new_piece.grid.shape[0]
        ydim = new_piece.grid.shape[1]
        assert (x + xdim <= 8 and y + ydim <= 8), "Piece is out of bounds"
        self.grid[x:(x + xdim),y:(y + ydim)] += new_piece.grid
        self.colorgrid[x:(x + xdim),y:(y + ydim)] += new_piece.colorgrid
            
    def good_grid(self):
        return(not np.any(self.grid > 1))
    
    def empty_space(self, x, y):
        return(self.grid[x,y] == 0)
    
    def gprint(self):
        s = [[str(e) for e in row] for row in self.grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
            
    def cprint(self):
        s = [[str(e)[(len(str(e)) - 2):] for e in row] for row in self.colorgrid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        
    def grid_to_string(self):
        s = [[str(e)[(len(str(e)) - 2):] for e in row] for row in self.colorgrid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return('\n'.join(table))

class Piece:
    
    def __init__(self, grid, color):
        self.grid = np.array(grid, dtype = np.int)
        self.color = color
        self.colorgrid = np.zeros(self.grid.shape, dtype = object)
        self.colorgrid[self.grid == 1] = self.color
        self.colorgrid[self.grid == 0] = ""
        self.__rotsym = np.array_equal(self.grid, np.rot90(self.grid, k = 2))
        self.__flipsym = np.array_equal(self.grid, np.flip(np.rot90(self.grid), axis = 1)) or \
        np.array_equal(self.grid, np.flip(self.grid, axis = 1))
        if self.__rotsym and self.__flipsym:
            self.max_orient = 2
            self.orientations = [0,1]
        elif self.__rotsym:
            self.max_orient = 4
            self.orientations = [0,1,4,5]
        elif self.__flipsym:
            self.max_orient = 4
            self.orientations = [0,1,2,3]
        else:
            self.max_orient = 8
            self.orientations = [0,1,2,3,4,5,6,7]
            
    def reorient(self, orientation):
        assert (orientation in self.orientations), "Not a valid orientation for this piece"
        # rotate piece appropriate number of rotations
        gr = np.rot90(self.grid, k = orientation % 4)
        # flip piece if needed
        if orientation > 3:
            gr = np.flip(gr, axis = 1)
        # add piece to grid in correct spot
        return Piece(gr.tolist(), self.color)
