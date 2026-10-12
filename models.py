from abc import ABC, abstractmethod
from datetime import datetime, timedelta

FMT = "%d.%m.%Y %H:%M:%S"
DAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]


# абстрактный класс
class Entity(ABC):
    @abstractmethod
    def info(self):
        pass


# общая пара, от нее наследуются виды пар
class Lesson(Entity):
    def __init__(self, start, subject, teacher):
        self.start = start
        self.subject = subject
        self.teacher = teacher

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if value.strip() == "":
            raise ValueError("введите предмет")
        self._subject = value.strip()

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, value):
        self._teacher = value.strip()

    @abstractmethod
    def kind(self):
        pass

    def important(self):
        return False

    def end(self):
        return self.start + timedelta(minutes=90)

    def info(self):
        day = DAYS[self.start.weekday()]
        t = self.start.strftime("%d.%m.%y") + ", " + day + "  " + self.start.strftime("%H:%M") + "-" + self.end().strftime("%H:%M")
        s = f"{t}  {self.subject} ({self.kind()}) - {self.teacher}"
        if self.important():
            s += "  (!)"
        return s

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"{type(self).__name__}({self.start}, '{self.subject}')"

    def __eq__(self, other):
        if not isinstance(other, Lesson):
            return False
        return self.start == other.start

    # сравнение по времени начала
    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __hash__(self):
        return hash(self.start)


class Lecture(Lesson):
    def kind(self):
        return "лекция"


class Exam(Lesson):
    def kind(self):
        return "зачет"

    def important(self):
        return True


class Retake(Lesson):
    def kind(self):
        return "пересдача"

    def important(self):
        return True


class User(Entity):
    def __init__(self, login):
        self.login = login
        self.time_in = datetime.now()
        self.time_out = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        if value.strip() == "":
            raise ValueError("введите логин")
        self._login = value.strip()

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def info(self):
        return f"{self.login} зашел в {self.time_in.strftime(FMT)}"

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"User('{self.login}')"

    def __eq__(self, other):
        return isinstance(other, User) and self.login == other.login

    def __lt__(self, other):
        return self.time_in < other.time_in

    def __gt__(self, other):
        return self.time_in > other.time_in

    def __hash__(self):
        return hash(self.login)


# свой словарь вместо dict
class MyMap:
    def __init__(self):
        self._keys = []
        self._values = []

    def __setitem__(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)
        return self._values[self._keys.index(key)]

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._keys

    def __eq__(self, other):
        return isinstance(other, MyMap) and self._keys == other._keys and self._values == other._values

    def __str__(self):
        return ", ".join([f"{k}: {v}" for k, v in zip(self._keys, self._values)])

    def __repr__(self):
        return f"MyMap({self})"

    def keys(self):
        return list(self._keys)


class Schedule(Entity):
    def __init__(self):
        self._lessons = []

    @property
    def lessons(self):
        return self._lessons

    @lessons.setter
    def lessons(self, value):
        self._lessons = list(value)

    def add(self, lesson):
        if lesson in self._lessons:
            return False
        self._lessons.append(lesson)
        return True

    def remove(self, lesson):
        self._lessons.remove(lesson)

    # kind тут это класс: Lecture, Exam, Retake или Lesson (все)
    def get(self, kind):
        res = [l for l in self._lessons if isinstance(l, kind)]
        return sorted(res)

    def next_lesson(self):
        future = [l for l in self._lessons if l.start > datetime.now()]
        if len(future) == 0:
            return None
        return min(future)

    def info(self):
        n = self.next_lesson()
        if n is None:
            return f"всего пар: {len(self)}, больше пар нет"
        return f"всего пар: {len(self)}, следующая: {n.subject} {n.start.strftime('%d.%m %H:%M')}"

    @staticmethod
    def default():
        s = Schedule()
        s.add(Exam(datetime(2026, 10, 12, 19, 0), "Объектно-ориентированное программирование", "Красильников А.В."))
        s.add(Retake(datetime(2026, 10, 14, 19, 0), "Теория вероятностей и математическая статистика", "Буланова А.Н."))
        s.add(Retake(datetime(2026, 10, 15, 19, 0), "Программные и аппаратные средства информационной безопасности", "Георгиевский А.Д."))
        s.add(Lecture(datetime(2026, 10, 16, 19, 0), "Теория информационных процессов и систем", "Горобинский Л.В."))
        s.add(Lecture(datetime(2026, 10, 16, 20, 40), "Теория информационных процессов и систем", "Горобинский Л.В."))
        s.add(Retake(datetime(2026, 10, 19, 19, 0), "Безопасность жизнедеятельности", "Юнусова М.К."))
        s.add(Exam(datetime(2026, 10, 20, 19, 0), "Дискретная математика", "Каракулова И.В."))
        s.add(Retake(datetime(2026, 10, 21, 19, 0), "Технология программирования", "Поляченко Е.Ю."))
        s.add(Lecture(datetime(2026, 10, 22, 19, 0), "Системный анализ в экономике", "Закирова Э.Р."))
        s.add(Lecture(datetime(2026, 10, 22, 20, 40), "Системный анализ в экономике", "Закирова Э.Р."))
        s.add(Lecture(datetime(2026, 10, 23, 19, 0), "Теория информации и кодирования", "Здольник В.В."))
        s.add(Lecture(datetime(2026, 10, 23, 20, 40), "Теория информации и кодирования", "Здольник В.В."))
        s.add(Lecture(datetime(2026, 10, 26, 19, 0), "Управление данными", "Воробьев А.А."))
        s.add(Lecture(datetime(2026, 10, 26, 20, 40), "Управление данными", "Воробьев А.А."))
        return s

    def __len__(self):
        return len(self._lessons)

    def __iter__(self):
        return iter(self._lessons)

    def __getitem__(self, i):
        return self._lessons[i]

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Schedule({len(self)})"

    def __eq__(self, other):
        return isinstance(other, Schedule) and self._lessons == other._lessons


class Report:
    @staticmethod
    def save(user, path="report.txt"):
        t_in = user.time_in.strftime(FMT)
        t_out = user.time_out.strftime(FMT)
        w1 = max(len("login"), len(user.login)) + 4
        w2 = len(t_in) + 4
        head = "|" + "login".center(w1) + "|" + "time_in".center(w2) + "|" + "time_out".center(w2) + "|"
        line = "|" + "-" * w1 + "|" + "-" * w2 + "|" + "-" * w2 + "|"
        row = "|" + user.login.center(w1) + "|" + t_in.center(w2) + "|" + t_out.center(w2) + "|"
        border = "+" + "-" * (len(row) - 2) + "+"
        with open(path, "a", encoding="utf-8") as f:
            f.write(border + "\n" + head + "\n" + line + "\n" + row + "\n" + border + "\n\n")
