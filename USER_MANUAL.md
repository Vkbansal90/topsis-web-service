# TOPSIS Assignment - User Manual

## Overview
This package provides three different ways to use TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution):
1. **Command-line program** (topsis.py)
2. **Python package** (installable via pip)
3. **Web service** (Flask web application)

---

## Part-I: Command-line Program

### Usage
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Example
```bash
python topsis.py data.csv "1,1,1,1,1" "+,+,+,+,-" output.csv
```

### Parameters
- **InputDataFile**: CSV file with alternatives in first column, criteria values in remaining columns
- **Weights**: Comma-separated numeric weights (e.g., "1,1,1,2")
- **Impacts**: Comma-separated impacts, either '+' (benefit) or '-' (cost) (e.g., "+,+,-,+")
- **OutputResultFileName**: Path for output CSV file

### Input File Format
```csv
Fund Name,P1,P2,P3,P4,P5
M1,0.84,0.71,6.7,42.1,12.59
M2,0.91,0.83,7.0,31.7,10.11
```

### Validation
The program validates:
- Correct number of parameters (4)
- File existence
- Minimum 3 columns
- Numeric values from 2nd column onwards
- Equal number of weights, impacts, and criteria
- Valid impact values (+ or -)
- Comma-separated format

---

## Part-II: Python Package

### Installation

#### From source
```bash
cd topsis
pip install .
```

#### After publishing to PyPI
```bash
pip install Topsis-vishesh-102316085
```

### Command-line Usage
After installation, use the `topsis` command:
```bash
topsis data.csv "1,1,1,2" "+,+,-,+" output.csv
```

### Python Library Usage
```python
from Topsis_vishesh_102316085 import topsis

result_df = topsis(
    input_file='data.csv',
    weights_str='1,1,1,2',
    impacts_str='+,+,-,+',
    output_file='output.csv'
)
```

### Package Structure
```
topsis/
├── Topsis_vishesh_102316085/
│   ├── __init__.py
│   └── topsis.py
├── setup.py
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Part-III: Web Service

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure email (optional)**:
Edit `app.py` and update email credentials:
```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
```

For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833).

3. **Run the application**:
```bash
python app.py
```

4. **Access the web interface**:
Open browser and navigate to: `http://localhost:5000`

### Using the Web Interface

1. **Upload CSV file**: Click "Choose a CSV file" and select your data file
2. **Enter weights**: Comma-separated values (e.g., "1,1,1,1")
3. **Enter impacts**: Comma-separated + or - (e.g., "+,+,-,+")
4. **Enter email**: Your email address to receive results
5. **Click "Calculate TOPSIS"**: Results will be displayed and emailed

### Features
- ✅ Modern, responsive UI with gradients and animations
- ✅ Real-time form validation
- ✅ File upload with drag-and-drop support
- ✅ Results displayed in interactive table
- ✅ Email delivery of results (CSV attachment)
- ✅ Comprehensive error handling

---

## Sample Data

### Input (data.csv)
```csv
Fund Name,P1,P2,P3,P4,P5
M1,0.84,0.71,6.7,42.1,12.59
M2,0.91,0.83,7.0,31.7,10.11
M3,0.79,0.62,4.8,46.7,13.23
M4,0.78,0.61,6.4,42.4,12.55
M5,0.94,0.88,3.6,62.2,16.91
M6,0.88,0.77,6.5,51.5,14.91
M7,0.66,0.44,5.3,48.9,13.83
M8,0.93,0.87,5.5,53.3,15.07
```

### Output (output.csv)
```csv
Fund Name,P1,P2,P3,P4,P5,Topsis Score,Rank
M6,0.88,0.77,6.5,51.5,14.91,0.6500,1
M8,0.93,0.87,5.5,53.3,15.07,0.6471,2
M2,0.91,0.83,7.0,31.7,10.11,0.6049,3
M1,0.84,0.71,6.7,42.1,12.59,0.5971,4
...
```

---

## Error Messages

### Common Errors
- **"Incorrect number of parameters"**: Provide exactly 4 arguments
- **"File not found"**: Check file path
- **"Must contain at least three columns"**: Add more criteria
- **"Must contain numeric values only"**: Remove non-numeric data from criteria columns
- **"Number of weights must equal number of criteria"**: Match counts
- **"Impacts must be either + or -"**: Use only + or - symbols

---

## Reference
Sample implementation: https://pypi.org/project/topsis-3283/

---

## Author
**Vishesh**  
Roll No: 102316085

## License
MIT License - See LICENSE file for details
