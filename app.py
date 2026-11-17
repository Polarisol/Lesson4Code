import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.months_list = []
        self.rainfall_list = []


        self.setWindowTitle("File Plotter")
        self.filename = None

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_file)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Month", "Rainfall [mm]"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.load_button)
        left_layout.addWidget(self.canvas)

        layout = QHBoxLayout()
        layout.addLayout(left_layout, 2)
        layout.addWidget(self.table, 1)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.draw_graph()

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if filename:
            self.filename = filename

            self.months_list = []
            self.rainfall_list = []
            with open(filename, 'r') as f:
                next(f)
                for line in f:
                    parts = line.split(',')  # ['Apr', '67\n']
                    self.months_list.append(parts[0])
                    self.rainfall_list.append(int(parts[1]))

            self.draw_graph()
            self.fill_table()

    def fill_table(self):
        self.table.setRowCount(len(self.months_list))
        for row, (month, rainfall) in enumerate(
            zip(self.months_list, self.rainfall_list)
        ):
            self.table.setItem(row, 0, QTableWidgetItem(str(month)))
            self.table.setItem(row, 1, QTableWidgetItem(str(rainfall)))

    def draw_graph(self):
        self.ax.clear()
        self.ax.bar(self.months_list, self.rainfall_list)
        self.ax.set_title(self.filename or "Example graph")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
