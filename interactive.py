#!/usr/bin/env python3

import sys, solvers

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: ./winrate.py <solver> <dictionary>')
		exit(1)

	# Again, extremely insecure. Go read winrate.py.
	solver = eval('solvers.'+sys.argv[1])
	solver = solver(sys.argv[2], True)
	while True:
		cur = solver.get()
		print(cur)
		res = solver.set(input('>: '))
		if res:
			print('Got it! Word is:', solver.get())
			break
		elif res is None:
			print('Word is not in the dictionary. You\'re on your own. Good luck.')
			break
