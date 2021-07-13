import unittest

import parse_options

class TestParseOptions(unittest.TestCase):

	def test_flag(self):
		options = ["@0:F:backprop=yes"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--backprop")

	def test_skip(self):
		options = ["@0:F:backprop=yes", "@1:S:deletion=yes", "@1:S:Geo:aryrestarts=2"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--backprop")

	def test_argument(self):
		options = ["@0:backprop=yes", "@1:deletion=yes", "@1:aryrestarts=2"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--backprop=yes --deletion=yes --aryrestarts=2")

	def test_multiple_arguments(self):
		options = ["@0:1:backprop=yes", "@0:2:backprop=no", "@0:3:backprop=heh"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--backprop=yes,no,heh")

		# args with extra syntactic sugar
		options = ["@0:1:backprop=yes", "@0:2:sugar:backprop=no", "@0:4:somemoresugar:backprop=heh"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--backprop=yes,no,heh")


	def test_special_no_arguments(self):
		options = ["@0:no:eq=0", "@1:No:contraction=no"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--eq=0 --no-contraction")

	def test_special_cases(self):
		options = ["@0:No:vsids-progress=no"]
		res = parse_options.parse_options(options)

		self.assertEqual(res.strip(), "--vsids-progress=no")