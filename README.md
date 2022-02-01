# Solving Wordle

## The game
[Wordle](https://www.powerlanguage.co.uk/wordle/) is a web game in which the player tries to guess a 5-letter word in 6 tries.
If a letter matches, it turns green. If it doesn't match but it's in the word, it turns yellow. If it's not in the word, it turns gray.
Letters can appear multiple times. In that case, there will be at max as many yellow letters as there are in the word.
For instance, if word is `OCOCO` and input is `COCOC`, only the two first Cs will be in yellow, and the last will be gray.

## The solvers
Wordle is interesting from the perspective of algorithm design: it's easy enough so it can be automated. This repository contains a bedrock to try your algorithms on.

- Change `common.py` to suit your needs.
- Put your wordlists in `dicts` (depends on the language you play).
- `game.py` has a Wordle implementation.
- Put your algorithms in `solvers`. They must either inherit `BaseSolver` (you should read it) or be compatible with it (must have `reset` and `set`). Have a look at `SimplestSolver`.
- Change `solvers/__init__.py` to include your algorithm.
- `winrate.py` banchmarks your solver.

The game implementation will return a ternary string. 0 is for gray, 1 is for yellow, 2 is for green. Pretty straightforward.

`self.words`, from BaseSolver, changes on each new input. `self.origwords` doesn't.