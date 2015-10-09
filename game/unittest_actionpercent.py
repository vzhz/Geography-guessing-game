import unittest

class Actiontest(unittest.TestCase):
	def test_action_percent(self):
		yousuck = action_based_on_precent(30)
		self.assertEqual(yousuck, "Keep trying! You'll get it!")

def action_based_on_precent(percent):
	if percent <= 20:
		return "Keep trying! You'll get it!" #can return and unit tests
	if percent >= 60:
		return "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"

if __name__ == '__main__':
	unittest.main()