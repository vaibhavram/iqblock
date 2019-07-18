# Solving the Petoy IQBlock Puzzle

I stumbled upon this neat little puzzle in my house that I had received years ago as a gift. After fumbling around with it for a few hours and arriving at over 20 solutions by hand, I wondered: how many solutions are there to this puzzle?

## Background

The IQBlock puzzle, manufactured by Petoy, is a puzzle consisting of 10 pieces. Each version has slightly different colored pieces, although the shapes themselves are the same. The pieces in my version are as shown below:

```
   Blue    Dark Green    Brown       Purple        White      
x x x        x x        x x x x     x x         x x           
    x        x x x      x x x x     x x         x x x x x     
    x x x    x x x                  x x x x                               
```

```
 Pink       Yellow      Orange    Light Green     Aqua 
x x         x           x             x            x
x x x x     x           x             x            x x
            x x x x     x x x         x x          x x
```

These pieces are to fit neatly into an 8x8 grid. Two example solutions are shown below:

<img src="https://raw.githubusercontent.com/vaibhavram/iqblock/master/hand_solutions/IMG_0387.jpg" width="200" height="200">

<img src="https://raw.githubusercontent.com/vaibhavram/iqblock/master/hand_solutions/IMG_0388.jpg" width="200" height="200">

## Literature

I searched online for answers to my questions and found a nicely-detailed article by [Hartmut Blessing](http://www.prismenfernglas.de/aboutme.html) located here: <http://www.prismenfernglas.de/iqblock_e.htm>. Mr. Blessing asserts that there are 12,724 unique solutions (rotations and reflections notwithstanding). However, I could not find any code or solution list to verify this quantity.

I searched some more and though I could find some YouTube videos (<https://www.youtube.com/watch?v=6jt93h7nRe4>) showing various solutions, I could find no other research into the number of solutions to this puzzle.

## Solutions

To replicate how I created the solutions, you would need to follow the following steps:

1. Create a folder called "solutions" and a folder called "logs" within iqblock/
2. Install the numpy package
3. Run pysolver.py. This script finds and writes solutions into multiple solutions files in the iqlock/solutions/ folder. The solutions are divided into multiple files to make it easier to start from where you left off in case the program stops midway
4. Run consolidate.py. This script consolidates all the solutions into one file

**If you would rather not run these steps, no worries! The solutions.txt file contains the fully consolidated solutions so no steps are required if you want to view all of them. As you can see there are 12,724 unique solutions, confirming Mr. Blessing's number!**

## Interactive Bot

I have also built an interactive bot so that you can play around with and find solutions under specific constraints. To run the bot, simply run bot.py in your Terminal. To view all of the commands that the bot accepts, enter 'help'. 

### Example 1
5. 

Here's an example of how one may use the bot to add 2 pieces to the grid and see how many solutions have those pieces in that configuration. Let's say the user wants to see how many solutions have the orange piece in the corner with the purple piece placed within it as so:

```
or or or -- -- -- -- -- 
or pu pu pu -- -- -- -- 
or pu pu pu -- -- -- -- 
-- -- -- pu -- -- -- -- 
-- -- -- pu -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
```

1. `load` - load all the solutions into the bot
2. `piece or 0` - see what the blue piece looks like in orientation 0. This shows the following configuration which does not match the orientation we want. 
```
1 0 0
1 0 0
1 1 1
```
3. `piece or 3` - we know that for orientations less than 4, each orientation is a counterclockwise rotation of the previous. Since we want to rotate the orange piece from orientation 0 by 3 counterclockwise orientations, we know that orientation 3 is the orientation we want.
```
1 1 1
1 0 0
1 0 0
```
4. `add or 0 0 3` - add the orange piece with position in row 0 and column 0 and in orientation 3 as discovered above.
```
or or or -- -- -- -- -- 
or -- -- -- -- -- -- -- 
or -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
```
5. `piece pu 0` - next, we view the purple piece to see which orientation we need it to be in. Looks like we need to reflect it across the y-axis to get the correct orientation.
```
1 1 1
1 1 1
1 0 0
1 0 0
```
6. `piece pu 4` - by adding 4 to the orientation, we reflect the piece along the y-axis. Now we can add the piece to the grid
```
1 1 1
1 1 1
0 0 1
0 0 1
```
7. `add pu 1 1 4` - we add the purple piece to the grid in row 1 column 1 and orientation 4. Now we are done adding the pieces we want and can look for matches.
```
or or or -- -- -- -- -- 
or pu pu pu -- -- -- -- 
or pu pu pu -- -- -- -- 
-- -- -- pu -- -- -- -- 
-- -- -- pu -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- 
```
8. `match` - look for matches. This will show how many matches there are for the current grid configuration.
`41 matches found`
9. `show 2` - show 2 of the matches.
```
Solution 1327:
or or or aq aq aq bl ye 
or pu pu pu aq aq bl ye 
or pu pu pu bl bl bl ye 
dg dg dg pu bl ye ye ye 
dg dg dg pu bl lg lg lg 
dg dg wh wh wh wh wh lg 
pi pi wh wh br br br br 
pi pi pi pi br br br br 

Solution 1648:
or or or aq aq aq bl wh 
or pu pu pu aq aq bl wh 
or pu pu pu bl bl bl wh 
lg lg lg pu bl ye wh wh 
pi pi lg pu bl ye wh wh 
pi pi ye ye ye ye dg dg 
pi br br br br dg dg dg 
pi br br br br dg dg dg 
```
10. `random` - show a random solution.
```
Solution 8528:
or or or wh wh wh wh wh 
or pu pu pu dg dg wh wh 
or pu pu pu dg dg dg ye 
br br bl pu dg dg dg ye 
br br bl pu ye ye ye ye 
br br bl bl bl lg aq aq 
br br pi pi bl lg aq aq 
pi pi pi pi bl lg lg aq 
```
11. `unmatch` - clear matches but preserve grid state
12. `exit`
