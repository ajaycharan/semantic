import unittest
from dates import DateService
from numbers import NumberService
from solver import MathService
from units import ConversionService
import datetime
from math import log, sin, sqrt, e, pi


class TestConversion(unittest.TestCase):
    pass


class TestMath(unittest.TestCase):

    def compareSolution(self, input, target):
        service = MathService()
        result = service.parseEquation(input)

        def close(x, y, EPSILON=1e-5):
            return abs(x - y) < EPSILON
        self.assertTrue(close(result, target))

    def testAddition(self):
        input = "five plus twenty one and a fifth"
        self.compareSolution(input, 5 + 21.2)

    def testUnary(self):
        input = "log sin eleven hundred"
        self.compareSolution(input, log(sin(1100)))

    def testPower(self):
        input = "fifteen to the eleven point five power"
        self.compareSolution(input, 15 ** 11.5)

    def testDividedBy(self):
        input = "3 divided by sqrt twenty five"
        self.compareSolution(input, 3 / sqrt(25))

    def testComplex(self):
        input = "eleven and a half divided by two hundred point two three to the sixth power"
        self.compareSolution(input, 15.25 / (200.23 ** 6))

    def testConstants(self):
        input = "E plus sqrt one plus tangent two times pi"
        self.compareSolution(input, e + 1)

    def testImplicitMultiplication(self):
        input = "eleven plus five log two hundred and six"
        self.compareSolution(input, 11 + 5 * log(206))

    def testImplicitConstantMultiplication(self):
        input = "two pie"
        self.compareSolution(input, 2 * pi)


class TestNumbers(unittest.TestCase):

    def compareNumbers(self, input, target):
        service = NumberService()
        result = service.parse(input)
        self.assertEqual(result, target)

    #
    # Float tests
    #

    def testFloatFracSpecial(self):
        input = "two and a quarter"
        self.compareNumbers(input, 2.25)

    def testFloatFrac(self):
        input = "two and two fifths"
        self.compareNumbers(input, 2.4)

    def testTwoAnds(self):
        input = "twelve thousand and eleven and one third"
        self.compareNumbers(input, 12011 + 1.0 / 3)

    def testFloatPoint(self):
        input = "five hundred and ten point one five"
        self.compareNumbers(input, 510.15)

    #
    # Integer tests
    #

    def testBigInt(self):
        input = "a hundred and fifty six thousand two hundred and twelve"
        self.compareNumbers(input, 156212)

    def testInt(self):
        input = "fifty one million and eleven"
        self.compareNumbers(input, 51000011)


class TestDate(unittest.TestCase):

    def compareDate(self, input, target):
        service = DateService()
        result = service.parseDate(input)
        self.assertEqual(result.month, target.month)
        self.assertEqual(result.day, target.day)

    def compareTime(self, input, target):
        service = DateService()
        result = service.parseDate(input)
        self.assertEqual(result.hour, target.hour)
        self.assertEqual(result.minute, target.minute)

    #
    #  Date Tests
    #

    def testExactWords(self):
        input = "Remind me on January Twenty Sixth"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testExactWordsDash(self):
        input = "Remind me on January Twenty-Sixth"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testExactNums(self):
        input = "Remind me on January 26"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testWeekFromExact(self):
        input = "Do x y and z a week from January 26"
        target = datetime.datetime(2014, 1, 26) + datetime.timedelta(days=7)
        self.compareDate(input, target)

    def testNextFriday(self):
        input = "Next Friday, go to the grocery store"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=7 + num_days_away)
        self.compareDate(input, target)

    def testTomorrow(self):
        input = "Tomorrow morning, go to the grocery store"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(input, target)

    def testToday(self):
        input = "Send me an email some time today if you can"
        target = datetime.datetime.today()
        self.compareDate(input, target)

    def testThis(self):
        input = "This morning, I went to the gym"
        target = datetime.datetime.today()
        self.compareDate(input, target)

    #
    #  Time Tests
    #

    def testExactTime(self):
        input = "Let's go to the park at 12:51pm tomorrow"
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        target = datetime.datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 12, 51)
        self.compareTime(input, target)

if __name__ == "__main__":
    for runner in (TestConversion, TestMath, TestNumbers, TestDate):
        suite = unittest.TestLoader().loadTestsFromTestCase(runner)
        unittest.TextTestRunner(verbosity=2).run(suite)
