import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QWidget, QTableWidget, QTableWidgetItem)

class SecantMethodGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Secant Method Calculator')

        widget = QWidget()
        layout = QVBoxLayout()

        self.setFixedWidth(790)

        self.function_label = QLabel('Enter function (use x as variable):')
        layout.addWidget(self.function_label)

        self.function_input = QLineEdit()
        layout.addWidget(self.function_input)

        self.x0_label = QLabel('Enter x0:')
        layout.addWidget(self.x0_label)

        self.x0_input = QLineEdit()
        layout.addWidget(self.x0_input)

        self.x1_label = QLabel('Enter x1:')
        layout.addWidget(self.x1_label)

        self.x1_input = QLineEdit()
        layout.addWidget(self.x1_input)

        self.tolerance_label = QLabel('Enter tolerance:')
        layout.addWidget(self.tolerance_label)

        self.tolerance_input = QLineEdit()
        layout.addWidget(self.tolerance_input)

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate_secant)
        layout.addWidget(self.calculate_button)

        self.result_text = QLabel()
        layout.addWidget(self.result_text)

        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def calculate_secant(self):
        func = self.function_input.text()
        x0 = float(self.x0_input.text())
        x1 = float(self.x1_input.text())
        tolerance = float(self.tolerance_input.text())

        def f(x):
            return eval(func)

        self.table.setRowCount(0)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['I', 'x_i-1', 'x_i', 'f(x_i-1)', 'f(x_i)', 'x_i+1', '|x_i - x_i-1|'])

        i = 0
        while abs(x1 - x0) >= tolerance:
            f_x0 = f(x0)
            f_x1 = f(x1)
            x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)

            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(str(x0)))
            self.table.setItem(i, 2, QTableWidgetItem(str(x1)))
            self.table.setItem(i, 3, QTableWidgetItem(str(f_x0)))
            self.table.setItem(i, 4, QTableWidgetItem(str(f_x1)))
            self.table.setItem(i, 5, QTableWidgetItem(str(x2)))
            self.table.setItem(i, 6, QTableWidgetItem(str(abs(x1 - x0))))

            x0 = x1
            x1 = x2
            i += 1

        self.result_text.setText(f"Result: {x1}")
        self.table.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    secant_gui = SecantMethodGUI()
    secant_gui.show()
    sys.exit(app.exec_())
