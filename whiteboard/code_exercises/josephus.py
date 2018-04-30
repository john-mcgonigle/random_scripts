def josephus(n, k):
	people = list(range(n))
	current = k-1
	return kill_captives(people, k, current)

def kill_captives(captives, k, i):
	if len(captives) == 1:
		return captives
	elif len(captives) >1:
		del(captives[i])
		print(captives)
		i += k
		if i > len(captives):
			i = i-(len(captives)+2)
		return kill_captives(captives, k, i)
	else:
		return []


