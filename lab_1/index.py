from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
import sys


ui, _ = loadUiType('id_gen.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setup_ui(self)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
