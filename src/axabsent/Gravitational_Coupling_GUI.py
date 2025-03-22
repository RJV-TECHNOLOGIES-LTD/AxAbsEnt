
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QDoubleSpinBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GravityFieldSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = 3
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gravitational Coupling Field (SDI/SRI Control)')
        layout = QGridLayout()

        self.sdi_inputs = []
        self.sri_inputs = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                sdi_label = QLabel(f'SDI({i},{j})')
                sdi_spin = QDoubleSpinBox()
                sdi_spin.setRange(0.1, 1.0)
                sdi_spin.setSingleStep(0.05)
                sdi_spin.setValue(0.3)
                self.sdi_inputs.append(sdi_spin)

                sri_label = QLabel(f'SRI({i},{j})')
                sri_spin = QDoubleSpinBox()
                sri_spin.setRange(0.1, 1.0)
                sri_spin.setSingleStep(0.05)
                sri_spin.setValue(0.6)
                self.sri_inputs.append(sri_spin)

                layout.addWidget(sdi_label, i*2, j)
                layout.addWidget(sdi_spin, i*2+1, j)
                layout.addWidget(sri_label, i*2+2, j)
                layout.addWidget(sri_spin, i*2+3, j)

        self.plot_button = QPushButton('Plot Gravitational Coupling')
        self.plot_button.clicked.connect(self.plot_gravity_field)
        layout.addWidget(self.plot_button, 10, 1, 1, 2)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 0, self.grid_size + 1, self.grid_size * 2, 4)

        self.setLayout(layout)
        self.show()

    def plot_gravity_field(self):
        SDI = np.array([spin.value() for spin in self.sdi_inputs]).reshape(self.grid_size, self.grid_size)
        SRI = np.array([spin.value() for spin in self.sri_inputs]).reshape(self.grid_size, self.grid_size)
        Coupling = np.tanh(5 * SRI / (SDI + 0.1))

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(np.arange(self.grid_size), np.arange(self.grid_size))
        ax.plot_surface(X, Y, Coupling, cmap='coolwarm')
        ax.set_title("Gravitational Coupling Field")
        ax.set_xlabel("Node X")
        ax.set_ylabel("Node Y")
        ax.set_zlabel("Coupling Intensity")
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GravityFieldSimulator()
    sys.exit(app.exec_())
