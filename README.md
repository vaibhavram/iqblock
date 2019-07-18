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

<img src="https://raw.githubusercontent.com/vaibhavram/iqblock/master/solver/hand_solutions/IMG_0387.jpg" width="200" height="200">

<img src="https://raw.githubusercontent.com/vaibhavram/iqblock/master/solver/hand_solutions/IMG_0388.jpg" width="200" height="200">

## Literature

I searched online for answers to my questions and found a nicely-detailed article by [Hartmut Blessing](http://www.prismenfernglas.de/aboutme.html) located here: <http://www.prismenfernglas.de/iqblock_e.htm>. Mr. Blessing asserts that there are 12,724 unique solutions (rotations and reflections notwithstanding). However, I could not find any code or solution list to verify this quantity.

I searched some more and though I could find some YouTube videos (<https://www.youtube.com/watch?v=6jt93h7nRe4>) showing various solutions, I could find no other research into the number of solutions to this puzzle.

## Solutions
