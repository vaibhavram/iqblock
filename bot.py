import numpy as np
from iqutils import Grid, Piece

class Bot():
    def __init__(self):
        self.loaded = False
        self.matched = False
        self.matches = []
        self.matchindices = []
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
        if not self.loaded:
            print("Not yet loaded")
        else:
            index = np.random.randint(0, self.size())
            if self.matched:
                solset = self.matches
            else:
                solset = self.sols
            result = solset[index]
            if self.matched:
                print("Solution " + str(self.matchindices[index]) + ":")
                result.cprint()
            else:
                print("Solution " + str(index) + ":")
                orientation = np.random.randint(0, 8)
                result.colorgrid = np.rot90(result.colorgrid, k = orientation % 4)
                if orientation > 3:
                    result.colorgrid = np.flip(result.colorgrid, axis = 1)
                result.cprint()

    def show(self, num = 1):
        if num > 1000:
            print("Number too high")
        elif self.loaded:
            if self.matched:
                solset = self.matches
            else:
                solset = self.sols
            result = solset[self.show_ind:(self.show_ind + num)]
            for i in range(min(num, len(result))):
                if not self.matched:
                    print("Solution " + str(self.show_ind + i) + ":")
                else:
                    print("Solution " + str(self.matchindices[self.show_ind + i]) + ":")
                result[i].cprint()
            self.show_ind += num
            if self.show_ind >= self.size():
                self.show_ind = 0
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
                piece.pprint(orientation)
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
                    print("Invalid addition")

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
            answer = input("Matches exist. Do you want to unmatch and re-match? [y]/n: ")
            if answer == "" or answer == "y":
                self.unmatch()
                self.match()
            else:
                print("Did not unmatch")
        else:
            if not self.added:
                print("No pieces added yet, cannot match")
            else:
                if not self.loaded:
                    self.load()
                for s in range(len(self.sols)):
                    sol_grid = self.sols[s]
                    result = self.get_grid_match(sol_grid, self.grid)
                    if result:
                        # result.cprint()
                        self.matches.append(result)
                        self.matchindices.append(s)
                print(str(len(self.matches)) + " matches found")
                self.matched = True
                self.show_ind = 0

    def reset(self):
        self.show_ind = 0
        self.loaded = True
        self.matched = False
        self.matches = []
        self.matchindices = []
        self.grid = Grid()
        self.added = []
        print("Full reset complete")

    def unmatch(self):
        self.matched = False
        self.matches = []
        self.matchindices = []
        self.show_ind = 0
        print("Matches reverted")

def main():
    bot = Bot()
    while True:
        cmd = input("[iq]> ").strip().split(" ")
        method = cmd[0].upper()
        if method == "HELP":
            print("""List of Commands:
    LOAD - load all solutions
    RANDOM - show random solution or match
    SHOW [int NUM] - show next NUM solutions (default 1)
    PIECE str COL [int O] - show piece of color COL in orientation O (default 0)
    GRID - show current state of grid
    ADD str COL int X int Y int O - add piece of color COL to grid at position X, Y in orientation O
    REMOVE str COL int X int Y int O - remove piece of color COL to grid at position X, Y in orientation O
    MATCH - find and save all solutions that match current grid state
    UNMATCH - clear all matches, preserving current grid state
    RESET - clear all matches and grid state
    EXIT - close program

    Pieces: BLue PUrple YEllow ORange PInk AQua LightGreen BRown DarkGreen WHite""")
        elif method == "LOAD":
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
            if len(cmd) < 2:
                print("Please enter a color")
            else:
                color = cmd[1]
                if len(cmd) < 3:
                    bot.piece(color, 0)
                else:
                    orientation = int(cmd[2])
                    bot.piece(color, orientation)
        elif method == "ADD":
            if len(cmd) < 5:
                print("Not enough arguments. See HELP")
            else:
                color = cmd[1]
                try:
                    row = int(cmd[2])
                    col = int(cmd[3])
                    ori = int(cmd[4])
                    bot.add(color, row, col, ori)
                except ValueError:
                    print("Incorrect argument type. See HELP")
        elif method == "REMOVE":
            if len(cmd) < 4:
                print("Not enough arguments. See HELP")
            else:
                color = cmd[1]
                try:
                    row = int(cmd[2])
                    col = int(cmd[3])
                    ori = int(cmd[4])
                    bot.remove(color, row, col, ori)
                except ValueError:
                    print("Incorrect argument type. See HELP")
        elif method == "GRID":
            bot.gridprint()
        elif method == "MATCH":
            bot.match()
        elif method == "RESET":
            bot.reset()
        elif method == "UNMATCH":
            bot.unmatch()
        elif method == "EXIT":
            break
        else:
            print("Not a valid command")

main()