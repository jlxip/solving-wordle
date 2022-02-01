'''
Simplest solver
Always returns the first candidate
Gives a nice baseline around what BaseSolver can do
'''

from . import base

class SimplestSolver(base.BaseSolver):
	alg = lambda self : self.words[0]

	def __init__(self, path, debug=False):
		super().__init__(path, debug)
		self.current = self.alg()
