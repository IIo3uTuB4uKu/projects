from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QLocale
from models import mainserver, server


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gomain()

    def gosettings(self):
        self.gui = server.Ui_MainWindow().setupUi(self)
        self.ConnectButtons()
        self.showMaximized()

    def gomain(self):
        self.gui = mainserver.Ui_MainWindow().setupUi(self)
        self.ConnectButtons()
        self.showMaximized()

    def ConnectButtons(self):
        self.gui.main.pressed.connect(self.gomain)
        self.gui.serversettings.pressed.connect(self.gosettings)


app = QApplication([])
window = MainWindow()
window.showMaximized()

app.exec_()
