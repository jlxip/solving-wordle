# Valid charset
GOOD = 'abcdefghijklmñnopqrstuvwxyz'

# Dictionary path
DICT = 'dicts/es.txt'

# Do not change this
def words():
	with open(DICT, 'r') as f:
		ret = f.read().splitlines()
	ret = [i for i in ret if len(i) == 5]
	ret = [i for i in ret if all([j in GOOD for j in i])]
	return ret
