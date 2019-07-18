import os

DIR = "solutions/"

sol_files = os.listdir(DIR)
sol_files = [file for file in sol_files if file.endswith(".txt")]

full_file = open("solutions.txt", "w+")
sol_num = 0

for file in sol_files:
    sol_file = open(DIR + file, "r")
    lines = sol_file.readlines()
    for line in lines:
        if line.startswith("Solution"):
            full_file.write("Solution " + str(sol_num) + ":\n")
            sol_num += 1
        else:
            full_file.write(line)
    sol_file.close()

full_file.close()