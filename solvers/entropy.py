'''
Entropy solver
Choses the word that best splits the wordspace, that is,
  the one that maximizes entropy
'''

from . import base
import copy, itertools, collections
import numpy as np
import game

class EntropySolver(base.BaseSolver):
	filter = lambda self, a, b : game.Wordle(a).run(b)

	# Cache for P
	# Original idea: iterate self.words and get how many
	#   result in res.
	# That can be precomputed as an inverse lookup function.
	def getNRes(self, word, res):
		if self.last != word:
			self.last = word
			self.lastRes = collections.defaultdict(int)
			for i in self.words:
				self.lastRes[self.filter(i, word)] += 1
		return self.lastRes[res]

	P = lambda self, word, res : self.getNRes(word, res) / len(self.words)

	def entropy(self, word):
		curve = []
		for i in itertools.product('012', repeat=5):
			x = ''.join(i)
			x = self.P(word, x)
			# Please, non-zero probabilities
			if x != 0:
				curve.append(x)
		curve = np.float32(curve)
		curve = -curve * np.log2(curve)
		return np.sum(curve)

	def alg(self):
		# Must be initialized on each word
		self.last = None
		results = {i: self.entropy(i) for i in self.words}
		return sorted(results.items(), key=lambda x : x[1])[-1][0]

	def __init__(self, path, debug=False):
		super().__init__(path, debug)

		try:
			with open(path+'.first', 'r') as f:
				self.current = f.read().lower()
		except:
			print('Don\'t know which is the best start. Computing now.')
			self.current = self.alg()
			with open(path+'.first', 'w') as f:
				f.write(self.current)
