"""
TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
Command-line implementation with comprehensive validation
"""

import sys
import pandas as pd
import numpy as np
import os


def validate_inputs(args):
    """Validate command-line arguments and input data"""
    
    # Check number of parameters
    if len(args) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        sys.exit(1)
    
    input_file = args[1]
    weights_str = args[2]
    impacts_str = args[3]
    output_file = args[4]
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Read the input file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error: Unable to read file '{input_file}'. {str(e)}")
        sys.exit(1)
    
    # Check if file has at least 3 columns
    if df.shape[1] < 3:
        print("Error: Input file must contain at least three columns.")
        sys.exit(1)
    
    # Check if columns from 2nd to last contain numeric values only
    numeric_cols = df.iloc[:, 1:]
    try:
        numeric_data = numeric_cols.apply(pd.to_numeric, errors='coerce')
        if numeric_data.isnull().any().any():
            print("Error: From 2nd to last columns must contain numeric values only.")
            sys.exit(1)
    except Exception:
        print("Error: From 2nd to last columns must contain numeric values only.")
        sys.exit(1)
    
    # Parse weights and impacts
    try:
        weights = [float(w.strip()) for w in weights_str.split(',')]
    except ValueError:
        print("Error: Weights must be numeric values separated by commas.")
        sys.exit(1)
    
    impacts = [i.strip() for i in impacts_str.split(',')]
    
    # Check if number of weights, impacts, and columns match
    num_criteria = df.shape[1] - 1  # Excluding first column (name/id)
    
    if len(weights) != num_criteria:
        print(f"Error: Number of weights ({len(weights)}) must be equal to number of criteria ({num_criteria}).")
        sys.exit(1)
    
    if len(impacts) != num_criteria:
        print(f"Error: Number of impacts ({len(impacts)}) must be equal to number of criteria ({num_criteria}).")
        sys.exit(1)
    
    # Validate impacts (must be either +ve or -ve)
    for impact in impacts:
        if impact not in ['+', '-', '+ve', '-ve']:
            print(f"Error: Impacts must be either '+' or '-' (or '+ve' or '-ve'). Found: '{impact}'")
            sys.exit(1)
    
    # Normalize impacts to + or -
    impacts = ['+' if i in ['+', '+ve'] else '-' for i in impacts]
    
    return df, weights, impacts, output_file


def normalize_matrix(df):
    """Normalize the decision matrix"""
    numeric_data = df.iloc[:, 1:].values
    
    # Calculate normalized matrix
    norm_matrix = numeric_data / np.sqrt((numeric_data ** 2).sum(axis=0))
    
    return norm_matrix


def calculate_topsis(df, weights, impacts):
    """Calculate TOPSIS scores and rankings"""
    
    # Step 1: Normalize the decision matrix
    norm_matrix = normalize_matrix(df)
    
    # Step 2: Calculate weighted normalized matrix
    weighted_matrix = norm_matrix * weights
    
    # Step 3: Determine ideal best and ideal worst
    ideal_best = np.zeros(len(weights))
    ideal_worst = np.zeros(len(weights))
    
    for i in range(len(weights)):
        if impacts[i] == '+':
            ideal_best[i] = weighted_matrix[:, i].max()
            ideal_worst[i] = weighted_matrix[:, i].min()
        else:
            ideal_best[i] = weighted_matrix[:, i].min()
            ideal_worst[i] = weighted_matrix[:, i].max()
    
    # Step 4: Calculate Euclidean distances
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    
    # Step 5: Calculate TOPSIS score
    topsis_score = dist_worst / (dist_best + dist_worst)
    
    # Step 6: Rank the alternatives
    rank = topsis_score.argsort()[::-1].argsort() + 1
    
    return topsis_score, rank


def main():
    """Main function to execute TOPSIS"""
    
    # Validate inputs
    df, weights, impacts, output_file = validate_inputs(sys.argv)
    
    # Calculate TOPSIS
    topsis_score, rank = calculate_topsis(df, weights, impacts)
    
    # Add results to dataframe
    result_df = df.copy()
    result_df['Topsis Score'] = topsis_score
    result_df['Rank'] = rank
    
    # Save to output file
    try:
        result_df.to_csv(output_file, index=False)
        print(f"Success! Results saved to '{output_file}'")
    except Exception as e:
        print(f"Error: Unable to write to file '{output_file}'. {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
