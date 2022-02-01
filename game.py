#!/usr/bin/env python3

import collections, random, common

class Wordle:
	def __init__(self, word, spoiler=False):
		self.word = word
		self.letters = collections.defaultdict(int)
		for i in word: self.letters[i] += 1
		self.tries = 0
		if spoiler: print('Spoiler:', self.word)

	def run(self, w):
		if self.tries == 6: return None

		assert len(w) == 5
		ret = []
		ctr = collections.defaultdict(int)

		for i in range(5):
			if self.word[i] == w[i]:
				# Good job
				ret.append('2')
			elif w[i] in self.word:
				# Letter is in the word. How many times?
				if ctr[w[i]] < self.letters[w[i]]:
					ret.append('1')
					ctr[w[i]] += 1
				else:
					# Oops, too many!
					ret.append('0')
			else:
				# u suck
				ret.append('0')

		self.tries += 1
		return ''.join(ret)

# In case you wanna test it
if __name__ == '__main__':
	with open(common.DICT, 'r') as f:
		words = f.read().splitlines()
	words = [i for i in words if len(i) == 5]
	words = [i for i in words if all([j in common.GOOD for j in i])]
	word = random.choice(words)

	game = Wordle(word)
	print('Good luck')
	while True:
		 a = input('>: ')
		 x = game.run(a)
		 if x is None:
		 	print('Better luck next time!')
		 	break
		 elif x == '22222':
		 	print('Congrats!')
		 	break
		 print(x)

