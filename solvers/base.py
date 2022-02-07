import sys, common

'''
Base solver for Wordle. Anyone who inherits:
  - Must override alg(). Called when knowledge is updated.
    Must return a word. Assume that, when called, there are at least two candidate words.
  - Must override constructor, setting "self.current".
'''

class BaseSolver:
	# Reset state of the solver, so a new one doesn't need to be created (and the dictionary read)
	def reset(self):
		self.words = self.origwords[:]

		self.known = set() # Green/yellow
		self.result = ['' for _ in range(5)] # Green
		self.forbidden = [set() for _ in range(5)] # Yellow/gray
		self.knownnot = set() # Gray

	def __init__(self, path, debug=False):
		self.debugEnabled = debug
		self.origwords = common.words(path)
		self.reset()

		# You should set initial current here!

	# Wrapper around print()
	def debug(self, *args):
		if self.debugEnabled: print(*args)

	finished = lambda self : all([i for i in result])
	get = lambda self : self.current

	# Update knowledge from a result
	def learn(self, word, code):
		for idx in range(5):
			cur = word[idx]

			if code[idx] == '2':
				# Known, there
				self.debug('%c is known to be in position %d' % (cur.upper(), idx+1))
				self.result[idx] = cur
				self.known.add(cur)
			elif code[idx] == '1':
				# Known, not there
				self.debug('There\'s a %c, not in position %d' % (cur.upper(), idx+1))
				self.known.add(cur)
				self.forbidden[idx].add(cur)
			else:
				# Forbidden there
				self.forbidden[idx].add(cur)
				# Everywhere?
				if all([code[i] == '0' for i in range(5) if word[i] == cur]):
					self.debug('%c never appears' % cur.upper())
					self.knownnot.add(cur)
				else:
					self.debug('There\'s a %c, not in position %d' % (cur.upper(), idx+1))

	# Update candidates with new knowledge
	def updateWords(self, sort=True):
		# Words with known letters
		for i in self.known:
			self.words = [j for j in self.words if i in j]
		# Words with green letters
		for idx, i in enumerate(self.result):
			if i != '':
				self.words = [j for j in self.words if j[idx] == i]
		# Do not repeat old mistakes
		for idx, i in enumerate(self.forbidden):
			self.words = [j for j in self.words if j[idx] not in i]
		# Exclude words with gray letters
		for i in self.knownnot:
			self.words = [j for j in self.words if all([k not in j for k in self.knownnot])]
		# Must make it deterministic you know
		if sort: self.words.sort()

	def set(self, code):
		self.learn(self.current, code)
		self.debug('\tKnown:', self.known)
		self.debug('\tResult:', self.result)
		self.debug('\tForbidden:', self.forbidden)
		self.debug('\tKnown not:', self.knownnot)
		self.updateWords()
		self.debug('Possible words:', len(self.words))
		if len(self.words) == 1:
			self.current = self.words[0]
			return True
		elif not self.words: return None

		self.current = self.alg()
		return False
