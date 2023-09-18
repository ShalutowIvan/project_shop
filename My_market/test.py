def aaa():
	q = 1
	print(q)
	def qwe():
		nonlocal q
		q = 11
		print(q)
		b = 2
		
	qwe()

	# def zxc():
	# 	nonlocal q
	# 	q = q + 5
	# 	w = 2
	# 	return q + w



aaa()