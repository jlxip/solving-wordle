'''
Random solver
To get a winrate baseline
The name is just so I can import 'random' lmao
'''

from . import base
import random

class RandomSolver(base.BaseSolver):
	# Notice how I use origwords instead of words
	# I don't want the smart behavior of BaseSolver
	alg = lambda self : random.choice(self.origwords)

	def __init__(self, path, debug=False):
		super().__init__(path, debug)
		self.current = self.alg()
