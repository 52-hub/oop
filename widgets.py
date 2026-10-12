from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# свои виджеты
class MyLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setFont(QFont("Arial", 11))


class MyButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(30)
        self.setCursor(Qt.PointingHandCursor)


class MyLineEdit(QLineEdit):
    def __init__(self, hint=""):
        super().__init__()
        self.setPlaceholderText(hint)


class MyList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)

    def fill(self, items):
        self.clear()
        for i in items:
            self.addItem(str(i))


class MyCombo(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)


class MyDateEdit(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())


class MyTimeEdit(QTimeEdit):
    def __init__(self):
        super().__init__()
        self.setTime(QTime(19, 0))


class MyMessage(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("ошибка")
        self.setIcon(QMessageBox.Warning)
        self.setText(text)

    @staticmethod
    def show_error(text):
        MyMessage(text).exec_()
