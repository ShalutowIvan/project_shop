class Asd:

	def __init__(self, *, a=0):
		self.a = a


q = Asd(b=2, a=1)


print(q.__dict__)


