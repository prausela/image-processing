from ui import Ui_MainWindow
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6 import QtWidgets
from logic import new_phantom, new_ellipse, add_ellipse, calculate_radon_transform, calculate_inverse_radon_transform
from plots import plot_phantom, plot_radon_transform, plot_inverse_radon, plot_single_degree_radon_transform


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ellipses = dict()
        self.draw_phantom()

        self.ui.desdeLineEdit.setText("0")
        self.ui.pasoLineEdit.setText("10")
        self.ui.hastaLineEdit.setText("180")
        self.calculate_radon_transform()

        self.iradon_filters = {
            "Ram-Lak": "ramp",
            "Shepp-Logan": "shepp-logan",
            "Cosine": "cosine",
            "Hamming": "hamming",
            "Hann": "hann",
            "None": None
        }

        self.calculate_iradon_transform()

        self.ui.agregarButton.clicked.connect(self.add_ellipse)
        self.ui.borrarButton.clicked.connect(self.remove_ellipse)
        self.ui.actualizarButton.clicked.connect(self.draw_phantom)

        self.ui.calcularButton.clicked.connect(self.calculate_radon_transform)
        self.ui.iCalcularButton.clicked.connect(self.calculate_iradon_transform)
        self.ui.verButton.clicked.connect(self.draw_angle)
        

    def add_ellipse(self):
        try:
            I = float(self.ui.intensidadLineEdit.text())
            A = float(self.ui.inclinacionLineEdit.text())
            X = float(self.ui.semiEjeXLineEdit.text())
            Y = float(self.ui.semiEjeYLineEdit.text())
            CX = float(self.ui.centroXLineEdit.text())
            CY = float(self.ui.centroYLineEdit.text())
            ellipse = new_ellipse(self.phantom, I, A, X, Y, CX, CY)
            ellipse_key = f"I={I}, X={X}, Y={Y}, Cx={CX}, Cy={CY}, A={A}"
            self.ellipses[ellipse_key] = ellipse
            self.ui.listWidget.addItem(ellipse_key)
        except:
            pass

    def draw_phantom(self):
        self.phantom = new_phantom()
        for ellipse in self.ellipses.values():
            self.phantom = add_ellipse(self.phantom, ellipse)
        plot_phantom(self.ui.phantomCanvas.figure, self.phantom)
        self.ui.phantomCanvas.draw()


    def remove_ellipse(self):
        idxs = self.ui.listWidget.selectedIndexes()
        for idx in idxs:
            item = self.ui.listWidget.takeItem(idx.row())
            self.ellipses.pop(item.text())

    def calculate_radon_transform(self):
        try:
            start = int(self.ui.desdeLineEdit.text())
            step = int(self.ui.pasoLineEdit.text())
            end = int(self.ui.hastaLineEdit.text())
            radon_transform, theta = calculate_radon_transform(self.phantom, start, step, end)
            self.radon_transform = radon_transform
            self.theta = theta

            self.ui.iDesdeLineEdit.setText(str(start))
            self.ui.iPasoLineEdit.setText(str(step))
            self.ui.hastaLineEdit_2.setText(str(end))

            plot_radon_transform(self.ui.radonCanvas.figure, self.radon_transform, self.theta)
            self.ui.radonCanvas.draw()
        except:
            pass

    def calculate_iradon_transform(self):
        try:
            iradon_filter = self.ui.filtroComboBox.currentText()
            iradon_interpolation = self.ui.interpolacionComboBox.currentText()

            iphantom = calculate_inverse_radon_transform(self.radon_transform, self.theta, iradon_interpolation, self.iradon_filters[iradon_filter])
            plot_inverse_radon(self.ui.iradonCanvas.figure, iphantom)
            self.ui.iradonCanvas.draw()
        except:
            pass

    def draw_angle(self):
        try:
            angle = int(self.ui.anguloLineEdit.text())
            plot_single_degree_radon_transform(self.ui.radonCanvas.figure, self.radon_transform, angle, self.theta)
            self.ui.radonCanvas.draw()
        except:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()