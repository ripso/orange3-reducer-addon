from AnyQt.QtWidgets import QSizePolicy, QLabel, QListView, QToolTip
from AnyQt.QtGui import QColor, QPen, QBrush, QPainter, QPicture, QPalette, QIntValidator
from Orange.widgets import gui, report, settings
from Orange.widgets.settings import ContextSetting
from Orange.widgets.utils import itemmodels
from Orange.data import Table
from AnyQt.QtCore import Qt
from Orange.widgets.widget import OWWidget, AttributeList, Msg, Input
from decimal import *

class MyWidget(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Reducer"
    icon = "icons/mywidget.svg"
    methods = ["count", "min", "max", "average", "sum"]
    reducer = ContextSetting(0)
    column = ContextSetting(None)
    result = 0

    def __init__(self):
        super().__init__()

        self.data = None

        common_options = dict(
            labelWidth=60, orientation=Qt.Horizontal,
            valueType=str, contentsLength=14
        )

        box = gui.vBox(self.controlArea, "Reducer configuration")

        gui.comboBox(box, self, "reducer",
            items=self.methods, callback=self.cb_reducer_onchange,
            label="Method :", **common_options)


        dmod = itemmodels.DomainModel
        self.column_model = itemmodels.DomainModel(dmod.MIXED, valid_types=dmod.PRIMITIVE)
        self.cb_column = gui.comboBox(
            box, self, "column", label="Column :", callback=self.cb_column_onchange,
            model=self.column_model, **common_options)

        gui.rubber(self.controlArea)


        self.content = gui.vBox(self.mainArea)
        self.content.setStyleSheet("background-color:white;font-size:32px;padding:10px;")

        self.resultText = gui.QLabel()
        self.content.layout().addWidget(self.resultText, 0, alignment=Qt.AlignCenter | Qt.AlignVCenter)
        self.resultText.setText(str(self.result))

    def _reducer_count(self):
        if (self.data is not None) :
            return len(self.data)
        return 0

    def _reducer_min(self):
        if (self.data is not None) :
            return min(map(lambda x: x[self.column], self.data))
        return 0

    def _reducer_max(self):
        if (self.data is not None) :
            return max(map(lambda x: x[self.column], self.data))
        return 0

    def _reducer_average(self):
        if (self.data is not None) :
            values = map(lambda x: Decimal(str(x[self.column])), self.data)
            return sum(values) / len(self.data)
        return 0

    def _reducer_sum(self):
        if (self.data is not None) :
            return sum(map(lambda x: Decimal(str(x[self.column])), self.data))
        return 0

    def calculate_result(self):
        if self.data and len(self.data):
            _reducer = getattr(self, '_reducer_' + self.methods[self.reducer])
            self.result = _reducer()
            self.resultText.setText(str(self.result))

    def cb_reducer_onchange(self):
        self.calculate_result()

    def cb_column_onchange(self):
        self.calculate_result()

    class Inputs:
        data = Input("Data", Table)

    @Inputs.data
    def set_dataset(self, data=None):
        self.data = data
        domain = data.domain if data and len(data) else None
        self.column_model.set_domain(domain)
        self.column = self.column_model[0] if self.column_model else None
        self.calculate_result()
