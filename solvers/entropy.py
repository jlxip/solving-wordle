'''
Entropy solver
Choses the word that best splits the wordspace, that is,
  the one that maximizes entropy
'''

from . import base
import copy, itertools, collections
import numpy as np
import game, time

class EntropySolver(base.BaseSolver):
	filter = lambda self, a, b : game.Wordle(a).run(b)

	# Original idea: easier to understand
	def P(self, word, res):
		ret = 0
		for i in self.words:
			if self.filter(i, word) == res: ret += 1
		return ret / len(self.words)

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

	# Notice how the iteration in P goes through all the words for each
	#   value of "res". Instead of that, it's better to precompute an
	#   inverse lookup function. This way, self.words has to be iterated
	#   just once
	def getNRes(self, word, res):
		if 'last' not in dir(self): self.last = None

		if self.last != word:
			self.last = word
			self.lastRes = collections.defaultdict(int)
			for i in self.words:
				self.lastRes[self.filter(i, word)] += 1
		return self.lastRes[res]

	def P(self, word, res):
		return self.getNRes(word, res) / len(self.words)

	# Notice that entropy iterates through all result combinations,
	#   but they are all precomputed, so "curve" is given by the items of
	#   "self.lastRes"
	P = entropy = getNRes = None # None of the previous functions are kept
	def entropy(self, word):
		aux = collections.defaultdict(int)
		for i in self.words:
			aux[self.filter(i, word)] += 1
		curve = np.float32(list(aux.values()))

		curve = curve[np.nonzero(curve)]
		curve /= len(self.words)
		curve = -curve * np.log2(curve)
		return np.sum(curve)

	def alg(self):
		# "origwords" instead of "words". Any can be the best separator.
		results = {word: self.entropy(word) for word in self.origwords}
		# Key that maximizes value
		return sorted(results.items(), key=lambda x : x[1])[-1][0]

	def __init__(self, path, debug=False):
		super().__init__(path, debug)

		try:
			with open(path+'.first', 'r') as f:
				self.current = f.read().lower()
		except:
			print('Don\'t know which is the best start. Computing now.')

			t = time.time()
			self.current = self.alg()
			print('Best start:', self.current)
			print('Took: %.2fs' % (time.time()-t))

			with open(path+'.first', 'w') as f:
				f.write(self.current)
