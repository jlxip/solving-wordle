#!/usr/bin/env python3

# Try it: ./winrate.py SimplestSolver

import sys
from game import Wordle
from alive_progress import alive_bar
import solvers, random, common

# If your algorithm is slow, you might want to enable this
SUBSET = False
# In case you want to see the process
DEBUG = False

def play(word, solver, debug=False):
	game = Wordle(word)
	solver.reset()

	ctr = 0
	while True:
		x = solver.get()
		if debug: print('Trying', x)
		g = game.run(x)
		ctr += 1
		if g is None:
			# Lost!
			if debug: print('Lost!')
			return False, ctr

		if debug: print('Got', g)
		if g == '22222':
			if debug: print('Won!')
			return True, ctr

		s = solver.set(g)
		if s is None:
			print('Not in dictionary! This is absolutely impossible!')
			assert False
		elif s == True:
			if debug: print('Only one left!')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: ./winrate.py <solver>')
		exit(1)

	words = common.words()
	if SUBSET:
		random.shuffle(words)
		words = words[:100]

	# Really insecure, but who cares. If you make this a service you deserve to be pwned
	solver = eval('solvers.'+sys.argv[1])
	solver = solver(common.DICT, debug=DEBUG)
	tries = 0 # Words required to win
	wins = 0
	loses = 0
	with alive_bar(len(words)) as bar:
		for i in words:
			result, ctr = play(i, solver)
			if result:
					tries += ctr
					wins += 1
			else: loses += 1
			bar()
	tries /= wins

	wr = (100*wins)/(wins+loses)
	print('Win rate:  %.2f%%' % wr)
	print('Avg tries: %.2f' % tries)
