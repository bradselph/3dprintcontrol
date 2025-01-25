import serial.tools.list_ports
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import serial
import time


class Ender3GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.initUI()
        self.connect_printer()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Movement controls
        movement = QGroupBox("Movement")
        move_layout = QGridLayout()

        move_buttons = {
            (0, 1): ("↑", lambda: self.move('Y', 10)),
            (1, 0): ("←", lambda: self.move('X', -10)),
            (1, 2): ("→", lambda: self.move('X', 10)),
            (2, 1): ("↓", lambda: self.move('Y', -10)),
            (0, 3): ("Z↑", lambda: self.move('Z', 10)),
            (1, 3): ("Z↓", lambda: self.move('Z', -10))
        }

        for pos, (text, func) in move_buttons.items():
            btn = QPushButton(text)
            btn.clicked.connect(func)
            move_layout.addWidget(btn, *pos)

        movement.setLayout(move_layout)

        # Step size controls
        step_control = QGroupBox("Step Size")
        step_layout = QHBoxLayout()
        self.step_size = QComboBox()
        self.step_size.addItems(['0.1', '1', '10', '50', '100'])
        self.step_size.setCurrentText('10')
        step_layout.addWidget(QLabel("Step (mm):"))
        step_layout.addWidget(self.step_size)
        step_control.setLayout(step_layout)

        # Temperature controls
        temp = QGroupBox("Temperature")
        temp_layout = QGridLayout()


        self.hotend_temp = QSpinBox()
        self.bed_temp = QSpinBox()
        self.hotend_temp.setRange(0, 250)
        self.bed_temp.setRange(0, 100)

        temp_layout.addWidget(QLabel("Hotend:"), 0, 0)
        temp_layout.addWidget(self.hotend_temp, 0, 1)
        temp_layout.addWidget(QPushButton("Set", clicked=self.set_hotend_temp), 0, 2)

        temp_layout.addWidget(QLabel("Bed:"), 1, 0)
        temp_layout.addWidget(self.bed_temp, 1, 1)
        temp_layout.addWidget(QPushButton("Set", clicked=self.set_bed_temp), 1, 2)

        temp.setLayout(temp_layout)

        # Status controls
        status = QGroupBox("Status")
        status_layout = QGridLayout()

        # Temperature displays
        self.current_hotend_temp = QLabel("0°C")
        self.current_bed_temp = QLabel("0°C")
        status_layout.addWidget(QLabel("Current Hotend:"), 0, 0)
        status_layout.addWidget(self.current_hotend_temp, 0, 1)
        status_layout.addWidget(QLabel("Current Bed:"), 1, 0)
        status_layout.addWidget(self.current_bed_temp, 1, 1)

        # Position displays
        self.position_x = QLabel("X: 0.0")
        self.position_y = QLabel("Y: 0.0")
        self.position_z = QLabel("Z: 0.0")
        status_layout.addWidget(self.position_x, 2, 0)
        status_layout.addWidget(self.position_y, 2, 1)
        status_layout.addWidget(self.position_z, 2, 2)

        status.setLayout(status_layout)

        # Connection test button
        test_connection_btn = QPushButton("Test Connection")
        test_connection_btn.clicked.connect(self.test_connection)

        # Home controls
        home = QGroupBox("Home")
        home_layout = QHBoxLayout()

        home_buttons = [
            ("Home All", self.home_all),
            ("Home X", self.home_x),
            ("Home Y", self.home_y),
            ("Home Z", self.home_z)
        ]

        for text, func in home_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            home_layout.addWidget(btn)

        home.setLayout(home_layout)

        # Add all components to main layout
        layout.addWidget(movement)
        layout.addWidget(step_control)
        layout.addWidget(temp)
        layout.addWidget(status)
        layout.addWidget(home)
        layout.addWidget(test_connection_btn)

        # Start update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)

        self.setWindowTitle('Ender 3 Control')
        self.setGeometry(300, 300, 400, 300)

    def connect_printer(self):
        try:
            import serial.tools.list_ports
            ports = list(serial.tools.list_ports.comports())

            ch340_port = None
            for port in ports:
                if "CH340" in port.description or "USB2.0-Serial" in port.description:
                    ch340_port = port.device
                    break

            if ch340_port:
                self.ser = serial.Serial(
                    port=ch340_port,
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1,
                    write_timeout=1
                )
                time.sleep(2)
                print(f"Connected to {ch340_port}")
                QMessageBox.information(self, "Success", f"Connected to printer at {ch340_port}")
            else:
                print("CH340 device not found")
                print("Available ports:", ports)
                QMessageBox.warning(self, "Error", "CH340 device not found\nAvailable ports: " + str(ports))

        except Exception as e:
            print(f"Connection error: {str(e)}")
            QMessageBox.warning(self, "Error", f"Connection error: {str(e)}")

    def test_connection(self):
        if self.ser and self.ser.is_open:
            try:
                # Send M115 command to get firmware info
                self.ser.write(b"M115\n")
                response = self.ser.readline().decode('utf-8', errors='ignore')
                print("Printer response:", response)
                return True
            except Exception as e:
                print(f"Test connection error: {str(e)}")
                return False
        return False

    def update_status(self):
        if self.ser and self.ser.is_open:
            try:
                # Get temperatures
                self.ser.write(b"M105\n")
                temp_response = self.ser.readline().decode('utf-8', errors='ignore')
                if 'T:' in temp_response:
                    hotend = temp_response.split('T:')[1].split()[0]
                    bed = temp_response.split('B:')[1].split()[0]
                    self.current_hotend_temp.setText(f"{hotend}°C")
                    self.current_bed_temp.setText(f"{bed}°C")

                # Get position
                self.ser.write(b"M114\n")
                pos_response = self.ser.readline().decode('utf-8', errors='ignore')
                if 'X:' in pos_response:
                    x = pos_response.split('X:')[1].split()[0]
                    y = pos_response.split('Y:')[1].split()[0]
                    z = pos_response.split('Z:')[1].split()[0]
                    self.position_x.setText(f"X: {x}")
                    self.position_y.setText(f"Y: {y}")
                    self.position_z.setText(f"Z: {z}")

            except Exception as e:
                print(f"Status update error: {str(e)}")

    def move(self, axis, direction):
        if self.ser:
            distance = float(self.step_size.currentText()) * direction
            command = f"G91\nG1 {axis}{distance} F1500\nG90\n"
            self.ser.write(command.encode())

    def set_hotend_temp(self):
        if self.ser:
            self.ser.write(f"M104 S{self.hotend_temp.value()}\n".encode())

    def set_bed_temp(self):
        if self.ser:
            self.ser.write(f"M140 S{self.bed_temp.value()}\n".encode())

    def home_all(self):
        if self.ser:
            self.ser.write(b"G28\n")

    def home_x(self):
        if self.ser:
            self.ser.write(b"G28 X\n")

    def home_y(self):
        if self.ser:
            self.ser.write(b"G28 Y\n")

    def home_z(self):
        if self.ser:
            self.ser.write(b"G28 Z\n")

    def closeEvent(self, event):
        if self.ser and self.ser.is_open:
            self.ser.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ender3GUI()
    ex.show()
    sys.exit(app.exec())