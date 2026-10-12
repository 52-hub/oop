import sys

from PyQt5.QtWidgets import QApplication, QDialog

from windows import LoginWindow, MainWindow


class App:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        login = LoginWindow()
        if login.exec_() == QDialog.Accepted:
            win = MainWindow(login.user)
            win.show()
            sys.exit(app.exec_())


if __name__ == "__main__":
    App.run()
