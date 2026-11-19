# Chart Generator App 📊

A simple desktop GUI application for generating bar, line, and pie charts. This was my solo project created to complete the **"Introduction to Programming"** course during my first year of university.

## Features

* **Chart Types:** Generate bar, line, and pie charts.
* **Manual Data Input:** Enter data using groups separated by a semicolon (`;`) and values separated by a comma (`,`).
* **File Import:** Load data directly from `.txt`, `.csv`, and `.xlsx` files.
* **Randomize Data:** Quickly generate sample data for testing.
* **Customization:** Customize the main chart color, line thickness, X and Y axis labels, and toggle the background grid.
* **Export:** Save generated charts directly to your disk.

## Technologies Used

* **Python 3**
* **Tkinter** (Graphical User Interface)
* **Matplotlib** (Chart generation and visualization)
* **Pandas** (Data parsing and `.csv`/`.xlsx` file handling)
* **Random** (Sample data generation)

## How to Run

1. Clone the repository or download the source code.
2. Install the required external libraries:
   ```bash
   pip install matplotlib pandas
   ```
3. Run the application (replace `main.py` with your actual file name):
   ```bash
   python main.py
   ```
