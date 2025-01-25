# Ender 3 Control GUI

A Python-based graphical user interface for controlling Ender 3 3D printers using PyQt6. This application provides an intuitive interface for common printer operations including movement control, temperature management, and homing functions.

## Features

- Real-time printer status monitoring
- Axis movement controls (X, Y, Z)
- Temperature control for hotend and bed
- Adjustable movement step sizes
- Auto-connection to printer via CH340 serial interface
- Position tracking
- Homing controls
- Live temperature readings

## Requirements

- Python 3.6+
- PyQt6 (<=6.8.0)
- PySerial (<=3.5)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bradselph/ender3-control-gui.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The application will automatically attempt to connect to your Ender 3 printer via the CH340 USB serial interface.

## License

This project is licensed under the GNU Affero General Public License v3 (AGPL-3.0). See the LICENSE file for details.

## Author

Brad Selph (https://github.com/bradselph)