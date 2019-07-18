import numpy as np

class Grid:
    
    def __init__(self, grid = [[0]*8]*8, colorgrid = [["--"]*8]*8):
        self.grid = np.array(grid, dtype = np.int)
        self.colorgrid = np.array(colorgrid, dtype = object)
        self.pieces = set()
        
    def add_piece(self, piece, x, y, orientation_index):
        assert (orientation_index < piece.max_orient), "Orientation exceeds number of orientations"
        new_piece = piece.reorient(piece.orientations[orientation_index])
        xdim = new_piece.grid.shape[0]
        ydim = new_piece.grid.shape[1]
        assert (x + xdim <= 8 and y + ydim <= 8), "Piece is out of bounds"
        self.grid[x:(x + xdim),y:(y + ydim)] += new_piece.grid
        self.colorgrid[x:(x + xdim),y:(y + ydim)] += new_piece.colorgrid
        self.pieces.add((piece.color, x, y, orientation_index))

    def remove_piece(self, piece, x, y, orientation_index):
        assert ((piece.color, x, y, orientation_index) in self.pieces), "Piece is not in grid"
        new_piece = piece.reorient(piece.orientations[orientation_index])
        xdim = new_piece.grid.shape[0]
        ydim = new_piece.grid.shape[1]
        self.grid[x:(x + xdim),y:(y + ydim)] -= new_piece.grid
        for r in range(x, x + xdim):
            for c in range(y, y + ydim):
                if self.colorgrid[r,c].endswith(piece.color):
                    self.colorgrid[r,c] = self.colorgrid[r,c][:-2]
        self.pieces.remove((piece.color, x, y, orientation_index))
            
    def good_grid(self):
        return(not np.any(self.grid > 1))

    def has_hole(self):
        for r in range(8):
            for c in range(8):
                if self.has1x1hole(r, c) or (c < 7 and self.has1x2hole(r,c)) \
                or (r < 7 and self.has2x1hole(r,c)):
                    return(True)
        return(False)

    def has1x1hole(self, r, c):
        if self.grid[r,c] == 0:
            if r == 0 and c == 0:
                if self.grid[r,c+1] > 0 and self.grid[r+1,c] > 0:
                    return(True)
            elif r == 0 and c == 7:
                if self.grid[r,c-1] > 0 and self.grid[r+1,c] > 0:
                    return(True)
            elif r == 7 and c == 0:
                if self.grid[r,c+1] > 0 and self.grid[r-1,c] > 0:
                    return(True)
            elif r == 7 and c == 7:
                if self.grid[r,c-1] > 0 and self.grid[r-1,c] > 0:
                    return(True)
            elif r == 0:
                if self.grid[r,c-1] >0 and self.grid[r,c+1] > 0 and self.grid[r+1,c] > 0:
                    return(True)
            elif r == 7:
                if self.grid[r,c-1] > 0 and self.grid[r,c+1] > 0 and self.grid[r-1,c] > 0:
                        return(True)
            elif c == 0:
                if self.grid[r-1,c] > 0 and self.grid[r+1,c] > 0 and self.grid[r,c+1] > 0:
                    return(True)
            elif c == 7:
                if self.grid[r-1,c] > 0 and self.grid[r+1,c] > 0 and self.grid[r,c-1] > 0:
                    return(True)
            else:
                if self.grid[r+1,c] > 0 and self.grid[r-1,c] > 0 and self.grid[r,c+1] > 0 \
                and self.grid[r,c-1] > 0:
                    return(True)
        return(False)

    def has1x2hole(self, r, c):
        assert (c < 7), "Column out of bounds"
        if self.grid[r,c] == 0 and self.grid[r,c+1] == 0:
            if r == 0 and c == 0:
                if self.grid[r,c+2] > 0 and self.grid[r+1,c] > 0 and self.grid[r+1,c+1] > 0:
                    return(True)
            elif r == 0 and c == 6:
                if self.grid[r,c-1] > 0 and self.grid[r+1,c] > 0 and self.grid[r+1,c+1] > 0:
                    return(True)
            elif r == 7 and c == 0:
                if self.grid[r,c+2] > 0 and self.grid[r-1,c] > 0 and self.grid[r-1,c+1] > 0:
                    return(True)
            elif r == 7 and c == 6:
                if self.grid[r,c-1] > 0 and self.grid[r-1,c] > 0 and self.grid[r-1,c+1] > 0:
                    return(True)
            elif r == 0:
                if self.grid[r,c-1] >0 and self.grid[r,c+2] > 0 \
                and self.grid[r+1,c] > 0 and self.grid[r+1,c+1] > 0:
                    return(True)
            elif r == 7:
                if self.grid[r,c-1] > 0 and self.grid[r,c+2] > 0 \
                and self.grid[r-1,c] > 0 and self.grid[r-1,c+1] > 0:
                        return(True)
            elif c == 0:
                if self.grid[r-1,c] > 0 and self.grid[r+1,c] > 0 \
                and self.grid[r-1,c+1] > 0 and self.grid[r+1,c+1] > 0 \
                and self.grid[r,c+2] > 0:
                    return(True)
            elif c == 6:
                if self.grid[r-1,c] > 0 and self.grid[r+1,c] > 0 \
                and self.grid[r-1,c+1] > 0 and self.grid[r+1,c+1] > 0 \
                and self.grid[r,c-1] > 0:
                    return(True)
            else:
                if self.grid[r+1,c] > 0 and self.grid[r-1,c] > 0 \
                and self.grid[r+1,c+1] > 0 and self.grid[r-1,c+1] \
                and self.grid[r,c+2] > 0 and self.grid[r,c-1] > 0:
                    return(True)
        return(False)

    def has2x1hole(self, r, c):
        self.grid = np.transpose(self.grid)
        has2x1 = self.has1x2hole(c, r)
        self.grid = np.transpose(self.grid)
        return(has2x1)
    
    def empty_space(self, x, y):
        return(self.grid[x,y] == 0)
    
    def gprint(self):
        s = [[str(e) for e in row] for row in self.grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
            
    # def cprint(self):
    #     s = [[str(e)[(len(str(e)) - 2):] for e in row] for row in self.colorgrid]
    #     lens = [max(map(len, col)) for col in zip(*s)]
    #     fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
    #     table = [fmt.format(*row) for row in s]
    #     print('\n'.join(table))

    def cprint(self):
        output = ""
        for r in range(8):
            for c in range(8):
                item = self.colorgrid[r,c][-2:]
                if item == "bl":
                    output += "\x1b[0;34m"
                elif item == "pu":
                    output += "\x1b[0;35m"
                elif item == "aq":
                    output += "\x1b[0;36m"
                elif item == "br":
                    output += "\x1b[0;31m"
                elif item == "lg":  
                    output += "\x1b[1;32m"
                elif item == "dg":  
                    output += "\x1b[0;32m"
                elif item == "pi":  
                    output += "\x1b[1;35m"
                elif item == "or":
                    output += "\x1b[1;31m"
                elif item == "wh":
                    output += "\x1b[0;37m"
                elif item == "ye":
                    output += "\x1b[1;33m"
                output += item + " "
                if item != "--":
                    output += "\x1b[0m"
            output += "\n"
        print(output)
        
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

    def pprint(self, orientation = 0):
        assert (orientation < self.max_orient), "Not a valid orientation for this piece"
        reoriented = self.reorient(self.orientations[orientation])
        s = [[str(e) for e in row] for row in reoriented.grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
