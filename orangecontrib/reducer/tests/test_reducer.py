import unittest
from Orange.widgets.tests.base import WidgetTest

from orangecontrib.reducer.widgets.mywidget import MyWidget


class ReducerTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)


class TestMyWidget(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(MyWidget)

    def test_addition(self):
        self.assertEqual(1 + 1, 2)
