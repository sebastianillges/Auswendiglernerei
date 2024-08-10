import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('Sie haben den Knopf gedrückt!')
    alert.exec_()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 Beispiel')
window.setGeometry(0, 0, 300, 300)

button = QPushButton('Klick mich', window)
button.clicked.connect(on_button_clicked)
# button.move(80, 20)

window.show()
sys.exit(app.exec_())
