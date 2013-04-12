"""Some emulations of classes not available in PyJS."""

class EOFError(Exception):
	def __init__(self, msg=""):
		self.msg = msg

	def __str__(self):
		return self.msg
	__repr__ = __str__


class StringIO(object):
	"""Emulation of the builtin io.StringIO."""

	__slots__ = ['s', 'pos']

	def __init__(self, s):
		if s[-1] != '\n': s += '\n'
		self.s = s
		self.pos = 0

	def __getattr__(self, k):
		import pyjamas.Window
		pyjamas.Window.alert("undefined key: " + k)

	def read(self, maxlen=4000):
		"""Read at most n characters.

		If the argument is negative or omitted, read until EOF is reached.
		Return an empty string at EOF.
		"""
		oldpos = self.pos
		endpos = min(oldpos + maxlen, len(self.s))

		self.pos = endpos
		import pyjamas.Window
		# pyjamas.Window.alert("reading " + str(self.s[oldpos:endpos]))
		return self.s[oldpos:endpos]

	def readline(self):
		r"""Read until the next \n."""

		oldpos = self.pos
		endpos = self.pos
		while endpos < len(self.s) and self.s[endpos] != '\n':
			endpos += 1
		if endpos == len(self.s):
			if endpos == oldpos:
				return ''
			else:
				self.s.append('\n')
		else:
			endpos += 1

		self.pos = endpos
		return self.s[oldpos:endpos]