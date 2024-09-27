from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
import sys


ui, _ = loadUiType('id_gen.ui')


class MainApp(QMainWindow, ui):
    """
    Main application window, inheriting from QMainWindow and the loaded UI.
    """
    def __init__(self) -> None:
        """
        Initializes the main application window and sets up the UI.
        """
        QMainWindow.__init__(self)
        self.setup_ui(self)


def main() -> None:
    """
    Main function to run the application.
    Creates an instance of QApplication, the main window,
    and starts the event loop.
    """
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
