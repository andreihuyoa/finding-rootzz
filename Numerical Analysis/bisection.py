import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
import math

def f(x):
    return x**3 + 2*x**2 + x - 3

def bisection_method(a, b, tol, iteration_callback=None):
    iteration = 0
    while (b - a) / 2 > tol or abs(f((a+b)/2)) > tol:
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

        self.setFixedWidth(300)

        self.form = QFormLayout()

        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.tol_input = QLineEdit("0.001")

        self.form.addRow("A", self.a_input)
        self.form.addRow("B", self.b_input)
        self.form.addRow("Tolerance", self.tol_input)

        layout.addLayout(self.form)

        self.result_label = QLabel("Results will be displayed here")
        layout.addWidget(self.result_label)

        self.iterations_table = QTableWidget()
        self.iterations_table.setColumnCount(7)
        self.iterations_table.setHorizontalHeaderLabels(["N", "a", "b", "f(a)", "f(b)", "c", "f(c)"])
        header = self.iterations_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.iterations_table)

        self.calculate_btn = QPushButton("Calculate")
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
#andreicute
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BisectionApp()
    ex.show()
    sys.exit(app.exec_())
