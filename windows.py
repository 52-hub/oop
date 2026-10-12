from datetime import datetime

from PyQt5.QtWidgets import *

from models import *
from widgets import *


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("вход")
        self.setFixedSize(280, 130)
        self.user = None

        self.edit = MyLineEdit("логин")
        self.btn = MyButton("войти")
        self.btn.clicked.connect(self.login)

        lay = QVBoxLayout()
        lay.addWidget(MyLabel("введите логин:"))
        lay.addWidget(self.edit)
        lay.addWidget(self.btn)
        self.setLayout(lay)

    def login(self):
        try:
            self.user = User(self.edit.text())
        except ValueError as e:
            MyMessage.show_error(str(e))
            return
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.schedule = Schedule.default()
        self.shown = []

        self.filters = MyMap()
        self.filters["все"] = Lesson
        self.filters["лекции"] = Lecture
        self.filters["зачеты"] = Exam
        self.filters["пересдачи"] = Retake

        self.kinds = MyMap()
        self.kinds["лекция"] = Lecture
        self.kinds["зачет"] = Exam
        self.kinds["пересдача"] = Retake

        self.setWindowTitle("Расписание")
        self.resize(750, 550)
        self.make_ui()
        self.update_list()

    def make_ui(self):
        self.info_label = MyLabel()
        self.filter_box = MyCombo(self.filters.keys())
        self.list = MyList()

        self.date_edit = MyDateEdit()
        self.time_edit = MyTimeEdit()
        self.subject_edit = MyLineEdit("предмет")
        self.teacher_edit = MyLineEdit("преподаватель")
        self.kind_box = MyCombo(self.kinds.keys())
        self.add_btn = MyButton("добавить пару")
        self.del_btn = MyButton("удалить пару")

        self.filter_box.currentIndexChanged.connect(self.update_list)
        self.add_btn.clicked.connect(self.add_lesson)
        self.del_btn.clicked.connect(self.delete_lesson)

        top = QHBoxLayout()
        top.addWidget(MyLabel("пользователь: " + self.user.login))
        top.addStretch()
        top.addWidget(MyLabel("показать:"))
        top.addWidget(self.filter_box)

        form = QFormLayout()
        form.addRow(MyLabel("дата:"), self.date_edit)
        form.addRow(MyLabel("время:"), self.time_edit)
        form.addRow(MyLabel("предмет:"), self.subject_edit)
        form.addRow(MyLabel("преподаватель:"), self.teacher_edit)
        form.addRow(MyLabel("вид:"), self.kind_box)

        btns = QHBoxLayout()
        btns.addWidget(self.add_btn)
        btns.addWidget(self.del_btn)

        lay = QVBoxLayout()
        lay.addLayout(top)
        lay.addWidget(self.list)
        lay.addWidget(self.info_label)
        lay.addLayout(form)
        lay.addLayout(btns)

        w = QWidget()
        w.setLayout(lay)
        self.setCentralWidget(w)

    def update_list(self):
        kind = self.filters[self.filter_box.currentText()]
        self.shown = self.schedule.get(kind)
        self.list.fill(self.shown)
        self.info_label.setText(self.schedule.info())

    def add_lesson(self):
        d = self.date_edit.date()
        t = self.time_edit.time()
        start = datetime(d.year(), d.month(), d.day(), t.hour(), t.minute())
        cls = self.kinds[self.kind_box.currentText()]
        try:
            l = cls(start, self.subject_edit.text(), self.teacher_edit.text())
        except ValueError as e:
            MyMessage.show_error(str(e))
            return
        if not self.schedule.add(l):
            MyMessage.show_error("на это время уже есть пара")
            return
        self.subject_edit.clear()
        self.teacher_edit.clear()
        self.update_list()

    def delete_lesson(self):
        row = self.list.currentRow()
        if row == -1:
            MyMessage.show_error("выберите пару")
            return
        self.schedule.remove(self.shown[row])
        self.update_list()

    # при закрытии сохраняем отчет
    def closeEvent(self, event):
        self.user.time_out = datetime.now()
        Report.save(self.user)
        event.accept()
