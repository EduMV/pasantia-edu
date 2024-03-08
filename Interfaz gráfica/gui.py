import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
from PyQt5 import uic
import time
import json
import os
import glob
import bitalino


class Plotter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("plotter.ui", self)
        self.setWindowTitle("Proyecto1")
        #self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.fs = 1000
        self.adq_time = 5
        self.recording = False
        pg.setConfigOption('foreground', '#000000')
        self.mac_address = "98:D3:71:FD:62:1F"
        self.device = bitalino.BITalino(self.mac_address)
        

        self.plot_widget = pg.PlotWidget()
        self.plot_lay.addWidget(self.plot_widget)
        self.data = []
        self.time = np.linspace(0, self.adq_time, self.fs*self.adq_time)
        self.pen = pg.mkPen(color=(0, 0, 255))
        self.curve = self.plot_widget.plot(self.time, self.data, pen=self.pen)
        
        self.plot_widget.setBackground((240,240,240))
        self.plot_widget.setLabel('left', 'Amplitud (mV)')
        self.plot_widget.setLabel('bottom', 'Tiempo (s)')
        self.plot_widget.showGrid(x=True, y=True)
        self.timer = QtCore.QTimer()

        self.start_b.setEnabled(True)
        self.start_b.clicked.connect(self.start_aq)
        self.timer.timeout.connect(self.update)
        self.selected_file = ""


        self.timer.start(3)




    def start_aq(self):
        if not self.recording:
            self.recording = True
            self.start_b.setEnabled(True)
            self.device.start(1000, [1])
            self.start_b.setText("Detener Adquisición 🛑")
        else:
            self.recording = False
            self.start_b.setEnabled(False)
            self.device.stop()
            self.start_b.setText("Iniciar adquisición ▶")



    def update(self): 
        
        if self.recording:
            samples = self.device.read(100)
            last_values = samples[:, -1]
            try:
                # Desplazar los datos existentes hacia adelante y actualizar los últimos 100 valores
                # Esto preserva la longitud total de self.data como 275
                self.data.extend(last_values.tolist())
                
                if len(self.data) > self.adq_time*self.fs:
                    self.curve.setData(self.time, self.data[-self.fs*self.adq_time:], pen=self.pen)
                else:
                    self.time = np.linspace(0, len(self.data)/self.fs,len(self.data))
                    self.curve.setData(self.time, self.data, pen=self.pen)

                print(len(self.data))
                
                # Ejemplo de actualización de texto
            except ValueError as e:
                print(f"Error al actualizar la gráfica: {e}")



def main():
    app = QtWidgets.QApplication(sys.argv)
    plotter = Plotter()
    plotter.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
