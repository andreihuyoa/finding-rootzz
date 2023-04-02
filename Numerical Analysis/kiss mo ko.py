import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton,
                             QPushButton, QMessageBox, QLineEdit, QFormLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMainWindow)
import math

def f(x):
    return x**3 + 2*x**2 + x - 3

def bisection_method(a, b, tol, iteration_callback=None):
    iteration = 0
    while (b - a) / 2 > tol or abs(f((a + b) / 2)) > tol:
        midpoint = (a + b) / 2
        if f(midpoint) == 0:
            break
        elif f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint

        iteration += 1
        if iteration_callback is not None:
            iteration_callback(iteration, a, b, midpoint)
    return (a + b) / 2

class BisectionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bisection Method')

        layout = QVBoxLayout()

        self.setFixedWidth(700)

        self.form = QFormLayout()

        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.tol_input = QLineEdit("0.001")

        self.form.addRow("A", self.a_input)
        self.form.addRow("B", self.b_input)
        self.form.addRow("Tolerance", self.tol_input)

        layout.addLayout(self.form)

        self.result_label = QLabel("Result:")
        layout.addWidget(self.result_label)

        self.iterations_table = QTableWidget()
        self.iterations_table.setColumnCount(7)
        self.iterations_table.setHorizontalHeaderLabels(["N", "a", "b", "f(a)", "f(b)", "c", "f(c)"])
        header = self.iterations_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.iterations_table)

        self.calculate_btn = QPushButton("Solve")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)

        self.setLayout(layout)

    def display_iteration(self, iteration, a, b, midpoint):
        row = self.iterations_table.rowCount()
        self.iterations_table.insertRow(row)

        self.iterations_table.setItem(row, 0, QTableWidgetItem(f"{iteration}"))
        self.iterations_table.setItem(row, 1, QTableWidgetItem(f"{a:.6f}"))
        self.iterations_table.setItem(row, 2, QTableWidgetItem(f"{b:.6f}"))
        self.iterations_table.setItem(row, 3, QTableWidgetItem(f"{f(a):.6f}"))
        self.iterations_table.setItem(row, 4, QTableWidgetItem(f"{f(b):.6f}"))
        self.iterations_table.setItem(row, 5, QTableWidgetItem(f"{midpoint:.6f}"))
        self.iterations_table.setItem(row, 6, QTableWidgetItem(f"{f(midpoint):.6f}"))

    # andreicute
    def calculate(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            tol = float(self.tol_input.text())

            fa = f(a)
            fb = f(b)

            if fa * fb >= 0:
                QMessageBox.warning(self, "Error", "f(a) and f(b) must have opposite signs")
                return

            self.iterations_table.setRowCount(0)

            result = bisection_method(a, b, tol, iteration_callback=self.display_iteration)
            self.result_label.setText(f"Result: {result:.6f}\nFunction(a) = {fa:.6f}\nFunction(b) = {fb:.6f}")

        except Exception as e:
            QMessageBox.warning(self, "Error", "Check input values")

class SecantMethodGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Secant Method')

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

        self.calculate_button = QPushButton('Solve')
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

class MethodSelectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Choose a Method')

        layout = QVBoxLayout()

        self.setFixedWidth(400)

        self.label = QLabel("Select a method to use:")
        layout.addWidget(self.label)

        self.bisection_radio = QRadioButton("Bisection Method")
        self.secant_radio = QRadioButton("Secant Method")

        layout.addWidget(self.bisection_radio)
        layout.addWidget(self.secant_radio)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_method)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def start_method(self):
        if self.bisection_radio.isChecked():
            self.bisection_app = BisectionApp()
            self.bisection_app.show()
            self.bisection_app.closeEvent = self.method_closed
            self.hide()
        elif self.secant_radio.isChecked():
            self.secant_gui = SecantMethodGUI()
            self.secant_gui.show()
            self.secant_gui.closeEvent = self.method_closed
            self.hide()
        else:
            QMessageBox.warning(self, "Error", "Please select a method")

    def method_closed(self, event):
        self.show()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    selection_app = MethodSelectionApp()
    selection_app.show()
    sys.exit(app.exec_())