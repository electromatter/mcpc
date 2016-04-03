class Base:
	@classmethod
	def decode(cls, ptr):
		raise NotImplementedError('tried to decode base type')

	def __init__(self):
		raise NotImplementedError('tried to create non-terminal type')

	def encode(self):
		raise NotImplementedError('tried to encode non-terminal type')

