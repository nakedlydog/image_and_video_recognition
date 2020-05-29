import unittest

from tkinter import *
from calculator import Application


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.calculator = Tk()
        self.calculator.title("Calculator")
        self.calculator.resizable(0, 1)
        self.app = Application(self.calculator)
        self.app.grid()

    def test_sum(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "2+2")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "4", "2+2 should have been 4")

    def test_sum_float(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "2.5+2.1")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "4.6", "2.5+2.1 should have been 4.6")


    def test_sub(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "4-2")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "2", "4-2 should have been 2")

    def test_sub_float(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "4-2.1")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "1.9", "4-2.1 should have been 1.9")

    def test_div(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "4/4")
        self.app.calculateExpression()
        self.assertEqual(int(float(self.app.display.get())), 1, "4/4 should have been 1")

    def test_mul(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "4*4")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "16", "4 * 4 should have been 16")

    def test_mul_float(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "4*4.5")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "18.0", "4 * 4.5 should have been 18.0")

    def test_percentage(self):
        self.app.display.delete(0)
        self.app.display.insert(0, "20%")
        self.app.calculateExpression()
        self.assertEqual(self.app.display.get(), "0.2", "20% should have been 0.2")

    def test_c(self):
        self.app.display.insert(0, "20%")
        self.app.clearButton.invoke()
        self.assertEqual(self.app.display.get(), "0", "After 'C' click text should have been reset to '0'")

    def test_all_num_buttons(self):
        test_cases = {
            "oneButton" : "1", "twoButton" : "2", "threeButton" : "3",
            "fourButton" : "4", "fiveButton" : "5", "sixButton" : "6",
            "sevenButton" : "7", "eightButton" : "8", "nineButton" : "9",
            "zeroButton" : "0", "plusButton" : "+", "dotButton" : ".",
            "minusButton" : "-", "percentageButton" : "%", "divideButton" : "/",
            "timesButton" : "*"
        }
        for key in test_cases:
            self.app.display.delete(0)
            getattr(self.app, key).invoke()
            self.assertEqual(self.app.display.get(), test_cases[key], "After click on " + key + " text should have been" + test_cases[key])



if __name__ == '__main__':
    unittest.main()
