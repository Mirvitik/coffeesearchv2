from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import sys
import sqlite3


class CoffeeForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.setWindowTitle('Программа Максима Алябьева')

    def run(self):
        self.statusbar.showMessage('')
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute("""DELETE FROM Coffee WHERE id = ?""", (self.spinBox.value(),))
        cur.execute(
            """INSERT INTO Coffee(id, NameOfSort, StepenObjarki, ground, description, price, obem) VALUES(?, ?, ?, ?, ?, ?, ?)""",
            (self.spinBox.value(), self.coftype.toPlainText(), self.stepobj.toPlainText(), self.ground.toPlainText(),
             self.flavdiscr.toPlainText(),
             int(self.price.toPlainText()),
             int(self.obem.toPlainText())))
        con.commit()


class Expresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.setWindowTitle('Программа Максима Алябьева')
        self.pushButton_2.clicked.connect(self.letitshow)

    def letitshow(self):
        form = CoffeeForm(self)
        form.show()

    def run(self):
        self.statusbar.showMessage('')
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute("""SELECT NameOfSort, StepenObjarki, ground, description, price, obem FROM Coffee
         WHERE id = ?""", (self.spinBox.value(),)).fetchone()
        if data is None:
            self.statusbar.showMessage('Предмета с таким id нет, попробуйте 1')
        else:
            self.coftype.setText(data[0])
            self.stepobj.setText(data[1])
            self.ground.setText('Молотый')
            self.ground.setText('В зёрнах')
            self.flavdiscr.setText(data[3])
            self.price.setText(str(data[4]))
            self.obem.setText(str(data[5]))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Expresso()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
