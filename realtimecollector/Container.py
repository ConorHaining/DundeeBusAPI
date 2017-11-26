class Container(object):

	""""""
	container = None

	"""docstring for Container"""
	def __init__(self):
		super(Container, self).__init__()
		self.container = {
			"container": self
		}

	def add(self, name, thing):
		
		self.container[name] = thing

		pass

	def get(self, name):

		if name in self.container:
			return self.container[name]
		else:
			raise LookupException('Key not found in container.')
			pass

		pass
		