'''
Heuristic solver
Score system: most diverse (number of different letters)
First, try the most diverse
Then, try words with as many non-used letters as possible, until there's few candidates
Finally, try the candidates
'''

import itertools
from . import base

unique = lambda x : len(set(list(x)))

def getMostDiverse(words):
	ret = words[0]
	better = unique(ret)

	for i in words:
		u = unique(i)
		if u == 5:
			# Best case: 5 letters
			return i
		else:
			if u > better:
				better = u
				ret = i
	return ret

# Explore that word space, gathering as much information as possible,
# in order to find all the letters
def search(known, knownnot, words):
	# It would be best to try 5 different, not in known
	# Zero different (words as-is) is not allowed (same results!)
	# Also, ideally, it would be a word with no letters in 'knownnot'
	pool = known | knownnot
	for keep in range(len(pool)-1):
		discard = len(pool) - keep
		for i in itertools.combinations(pool, r=discard):
			#aux = [j for j in words if all([k not in j for k in i])]
			#aux = [j for j in words if all([k not in i for k in j])]
			iset = set(i)
			aux = [j for j in words if not any([k in iset for k in j])]
			if aux: return getMostDiverse(aux)
	print('Is this even possible?')
	exit(69)

class HeuristicSolver(base.BaseSolver):
	def __init__(self, path, debug=False):
		super().__init__(path, debug)
		self.current = getMostDiverse(self.words)

	def alg(self):
		# Any unknown? If only two possibilities, it's not worth to go this way
		if len(self.known) < 5 and len(self.words) > 2:
			# Yep. Just start blasting letters to find the remaining
			# Would be best if no letters were in 'known' in order to maximize information gathered
			# But it might not be the case!
			self.debug('There are unknown letters, let\'s explore')
			ret = search(self.known, self.knownnot, self.origwords)
			return ret

		# Just a matter of bruteforce now
		return self.words[0]
