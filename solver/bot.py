import numpy as np
from iqutils import Grid, Piece

class Bot():
    def __init__(self):
        self.loaded = False
        self.matched = False
        self.matches = []
        self.sols = []
        self.grid = Grid()
        self.pieces = {"bl": Piece([[1,1,1,0,0],[0,0,1,0,0],[0,0,1,1,1]], "bl"),
                    "br": Piece([[1,1,1,1],[1,1,1,1]], "br"),
                    "or": Piece([[1,0,0],[1,0,0],[1,1,1]], "or"),
                    "dg": Piece([[1,1,0],[1,1,1],[1,1,1]], "dg"),
                    "ye": Piece([[1,0,0],[1,0,0],[1,0,0],[1,1,1]], "ye"),
                    "pi": Piece([[1,1],[1,1],[1,0],[1,0]],"pi"),
                    "pu": Piece([[1,1,1],[1,1,1],[1,0,0],[1,0,0]], "pu"),
                    "lg": Piece([[1,1],[1,0],[1,0]],"lg"),
                    "wh": Piece([[1,1],[1,1],[1,0],[1,0],[1,0]], "wh"),
                    "aq": Piece([[1,1],[1,1],[1,0]], "aq")}
        self.added = []
        self.show_ind = 0

    def load(self):
        file = open("solutions.txt", "r")
        lines = file.readlines()
        curr_sol = []
        for line in lines:
            if line.startswith("Solution"):
                curr_sol = []
            elif line == "\n":
                self.sols.append(Grid([[1]*8]*8, curr_sol))
            else:
                row = line[:-1].split(" ")
                row = [item for item in row]
                curr_sol.append(row)
        self.loaded = True
        print("Solutions loaded")

    def size(self):
        if self.matched:
            return(len(self.matches))
        else:
            return(len(self.sols))

    def random(self):
        if self.loaded:
            index = np.random.randint(0, self.size())
            orientation = np.random.randint(0, 8)
            if self.matched:
                solset = self.matches
            else:
                solset = self.sols
            result = solset[index]
            result.colorgrid = np.rot90(result.colorgrid, k = orientation % 4)
            if orientation > 3:
                result.colorgrid = np.flip(result.colorgrid, axis = 1)
            if not self.matched:
                print("Solution " + str(index) + ":")
            else:
                print("Match " + str(index) + ":")
            result.cprint()
        else:
            print("Not yet loaded")

    def show(self, num = 10):
        if self.loaded:
            if self.matched:
                solset = self.matches
            else:
                solset = self.sols
            result = solset[self.show_ind:(self.show_ind + num)]
            for i in range(min(num, len(result))):
                if not self.matched:
                    print("Solution " + str(self.show_ind + i) + ":")
                else:
                    print("Match " + str(self.show_ind + i) + ":")
                result[i].cprint()
            self.show_ind += num
        else:
            print("Not yet loaded")

    def process(self, color):
        if color in ["darkgreen", "lightgreen"]:
            color = color[0] + "g"
        else:
            color = color[0:2]
        if color not in self.pieces:
            print("Invalid color")
            return(None)
        else:
            return(color)

    def piece(self, color, orientation):
        color = self.process(color)
        if color:
            piece = self.pieces[color]
            try:
                piece.print(orientation)
            except AssertionError:
                print("Invalid orientation")

    def add(self, color, r, c, o):
        color = self.process(color)
        if color:
            if color in self.added:
                print("Piece already added")
            else:
                piece = self.pieces[color]
                try:
                    self.grid.add_piece(piece, r, c, o)
                    if self.grid.good_grid():
                        self.grid.cprint()
                        self.added.append(color)
                    else:
                        self.grid.remove_piece(piece, r, c, o)
                        print("Invalid placement")
                except AssertionError:
                    print("Invalid orientation")

    def remove(self, color, r, c, o):
        color = self.process(color)
        if color:
            if color not in self.added:
                print("Color not in grid")
            else:
                piece = self.pieces[color]
                if (piece.color, r, c, o) not in self.grid.pieces:
                    print("Piece not in grid")
                else:
                    self.grid.remove_piece(piece, r, c, o)
                    self.grid.cprint()
                    self.added.remove(piece.color)

    def gridprint(self):
        self.grid.cprint()

    def get_grid_match(self, big, small):
        for o in range(8):
            testgrid = np.rot90(big.colorgrid, k = o % 4)
            if o > 3:
                testgrid = np.flip(testgrid, axis = 1)
            num_true = 0
            for r in range(8):
                for c in range(8):
                    if small.colorgrid[r,c] == "--" or \
                    small.colorgrid[r,c][-2:] == testgrid[r,c]:
                        num_true += 1
            if num_true == 64:
                return(Grid([[1]*8]*8, testgrid))
        return(None)


    def match(self):
        if self.matched:
            print("Already matched")
        else:
            if not self.added:
                print("No pieces added yet")
            elif self.loaded:
                for sol_grid in self.sols:
                    result = self.get_grid_match(sol_grid, self.grid)
                    if result:
                        self.matches.append(result)
                print(str(len(self.matches)) + " matches found")
                self.matched = True
                self.show_ind = 0
            else:
                print("Not yet loaded")

    def reset(self):
        self.show_ind = 0
        self.loaded = True
        self.matched = False
        self.matches = []
        self.grid = Grid()
        self.added = []
        print("Full reset complete")

    def revert(self):
        self.matched = False
        self.matches = []
        self.show_ind = 0
        print("Matches reverted")


def main():
    bot = Bot()
    while True:
        cmd = input("[iq]> ").split(" ")
        method = cmd[0].upper()
        if method == "LOAD":
            bot.load()
        elif method == "RANDOM":
            bot.random()
        elif method == "SHOW":
            if len(cmd) > 1:
                num = int(cmd[1])
                bot.show(num)
            else:
                bot.show()
        elif method == "PIECE":
            color = cmd[1]
            orientation = int(cmd[2])
            bot.piece(color, orientation)
        elif method == "ADD":
            color = cmd[1]
            row = int(cmd[2])
            col = int(cmd[3])
            ori = int(cmd[4])
            bot.add(color, row, col, ori)
        elif method == "REMOVE":
            color = cmd[1]
            row = int(cmd[2])
            col = int(cmd[3])
            ori = int(cmd[4])
            bot.remove(color, row, col, ori)
        elif method == "GRID":
            bot.gridprint()
        elif method == "MATCH":
            bot.match()
        elif method == "RESET":
            bot.reset()
        elif method == "REVERT":
            bot.revert()
        elif method == "EXIT":
            break
        else:
            print("Not a valid command")

main()