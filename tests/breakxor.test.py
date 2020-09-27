import unittest
from sys import path
path.insert(1, '/home/gavin/Development/repeatkey/src/')
from break_repeat_key import crack_xor

class TesterBreakKey(unittest.TestCase):

	def test_break_key(self):
		expected = 'Terminator X: Bring the noise'
		self.assertEqual(expected, crack_xor('./6.txt'))

if __name__ == "__main__":
	unittest.main()
