"""
What are we testing
"""

class StocksTestCase(TestCase):
	def test_stupid(self):
		"""Describe test"""
		a = 1
		b = 2
		self.assertEqual(a+b,3)