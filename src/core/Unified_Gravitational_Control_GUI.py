
import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QDoubleSpinBox, QPushButton, QTabWidget, QVBoxLayout, QScrollArea
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CouplingTab(QWidget):
    def __init__(self, grid_size):
        super().__init__()
        self.grid_size = grid_size
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        self.sdi_inputs = []
        self.sri_inputs = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                sdi_spin = QDoubleSpinBox()
                sdi_spin.setRange(0.1, 1.0)
                sdi_spin.setSingleStep(0.05)
                sdi_spin.setValue(0.3)
                self.sdi_inputs.append(sdi_spin)

                sri_spin = QDoubleSpinBox()
                sri_spin.setRange(0.1, 1.0)
                sri_spin.setSingleStep(0.05)
                sri_spin.setValue(0.6)
                self.sri_inputs.append(sri_spin)

                grid_layout.addWidget(QLabel(f'SDI({i},{j})'), i*2, j)
                grid_layout.addWidget(sdi_spin, i*2+1, j)
                grid_layout.addWidget(QLabel(f'SRI({i},{j})'), i*2+2, j)
                grid_layout.addWidget(sri_spin, i*2+3, j)

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(grid_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.plot_button = QPushButton('Plot Gravitational Coupling')
        self.plot_button.clicked.connect(self.plot_gravity_field)
        layout.addWidget(self.plot_button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

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

class CEFTTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_ceft()

    def plot_ceft(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x = np.linspace(-5, 5, 200)
        y = np.exp(-0.2 * x**2) * np.sin(2 * np.pi * x)
        ax.plot(x, y, label='Entropy Flux Projection')
        ax.set_title("Curvature Entropy Flux Tensor Field (Simulated)")
        ax.set_xlabel("Force Space Axis")
        ax.set_ylabel("Entropy Flow")
        ax.legend()
        self.canvas.draw()

class ForceModTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_force_modulation()

    def plot_force_modulation(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        theta = np.linspace(0, 2 * np.pi, 500)
        mod = 1 + 0.2 * np.sin(3 * theta)
        ax.plot(theta, mod, label='Force Differentiation Angle')
        ax.set_title("Force Modulation via FDT (Simulated)")
        ax.set_xlabel("Phase Angle (θ)")
        ax.set_ylabel("Differentiation Modulation")
        ax.legend()
        self.canvas.draw()

class UnifiedModelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified Model: Gravitational Control Interface")
        layout = QVBoxLayout()
        tabs = QTabWidget()

        self.coupling_tab = CouplingTab(grid_size=10)
        self.ceft_tab = CEFTTab()
        self.forcemod_tab = ForceModTab()

        tabs.addTab(self.coupling_tab, "SDI/SRI Gravitational Coupling")
        tabs.addTab(self.ceft_tab, "CEFT Field Visualization")
        tabs.addTab(self.forcemod_tab, "Force Modulation (FDT)")

        layout.addWidget(tabs)
        self.setLayout(layout)
        self.resize(1400, 800)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UnifiedModelApp()
    window.show()
    sys.exit(app.exec_())
