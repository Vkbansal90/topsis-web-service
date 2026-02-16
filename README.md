# Topsis-vishesh-102316085

A Python package implementing TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) for multi-criteria decision making.

## Description

TOPSIS is a multi-criteria decision analysis method. It helps in ranking alternatives based on their distance from the ideal solution. This package provides both a Python library and a command-line interface for performing TOPSIS analysis.

you can try it on - https://topsis-web-service-swbs.onrender.com/

## Installation

### From PyPI (after publishing)
```bash
pip install Topsis-vishesh-102316085
```

### From source
```bash
git clone https://github.com/yourusername/topsis.git
cd topsis
pip install .
```

## Usage

### Command Line

After installation, you can use the `topsis` command:

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

**Example:**
```bash
topsis data.csv "1,1,1,2" "+,+,-,+" output.csv
```

**Parameters:**
- `InputDataFile`: Path to CSV file containing the decision matrix (first column should be alternative names)
- `Weights`: Comma-separated weights for each criterion (e.g., "1,1,1,2")
- `Impacts`: Comma-separated impacts for each criterion, either '+' (benefit) or '-' (cost) (e.g., "+,+,-,+")
- `OutputResultFileName`: Path where the result CSV will be saved

### Python Library

```python
from Topsis_vishesh_102316085 import topsis

# Perform TOPSIS analysis
result_df = topsis(
    input_file='data.csv',
    weights_str='1,1,1,2',
    impacts_str='+,+,-,+',
    output_file='output.csv'
)

print(result_df)
```

## Input File Format

The input CSV file should have:
- First column: Names/IDs of alternatives
- Remaining columns: Numeric criteria values

**Example (data.csv):**
```
Fund Name,P1,P2,P3,P4,P5
M1,0.84,0.71,6.7,42.1,12.59
M2,0.91,0.83,7.0,31.7,10.11
M3,0.79,0.62,4.8,46.7,13.23
```

## Output

The output CSV file will contain:
- All original columns
- `Topsis Score`: Calculated TOPSIS score for each alternative
- `Rank`: Rank of each alternative (1 being the best)

## Validation

The package performs comprehensive validation:
- Correct number of parameters
- File existence check
- Minimum 3 columns requirement
- Numeric values validation (from 2nd column onwards)
- Equal number of weights, impacts, and criteria
- Valid impact values (+ or -)
- Comma-separated format for weights and impacts

## Sample Example

Reference implementation: https://pypi.org/project/topsis-3283/

## License

MIT License

## Author

Vishesh (Roll No: 102316085)
