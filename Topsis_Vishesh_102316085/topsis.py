"""
TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
Package module
"""

import pandas as pd
import numpy as np
import os
import sys


def validate_inputs(input_file, weights_str, impacts_str):
    """Validate input parameters and data"""
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found.")
    
    # Read the input file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Unable to read file '{input_file}'. {str(e)}")
    
    # Check if file has at least 3 columns
    if df.shape[1] < 3:
        raise ValueError("Input file must contain at least three columns.")
    
    # Check if columns from 2nd to last contain numeric values only
    numeric_cols = df.iloc[:, 1:]
    try:
        numeric_data = numeric_cols.apply(pd.to_numeric, errors='coerce')
        if numeric_data.isnull().any().any():
            raise ValueError("From 2nd to last columns must contain numeric values only.")
    except Exception:
        raise ValueError("From 2nd to last columns must contain numeric values only.")
    
    # Parse weights and impacts
    try:
        weights = [float(w.strip()) for w in weights_str.split(',')]
    except ValueError:
        raise ValueError("Weights must be numeric values separated by commas.")
    
    impacts = [i.strip() for i in impacts_str.split(',')]
    
    # Check if number of weights, impacts, and columns match
    num_criteria = df.shape[1] - 1  # Excluding first column (name/id)
    
    if len(weights) != num_criteria:
        raise ValueError(f"Number of weights ({len(weights)}) must be equal to number of criteria ({num_criteria}).")
    
    if len(impacts) != num_criteria:
        raise ValueError(f"Number of impacts ({len(impacts)}) must be equal to number of criteria ({num_criteria}).")
    
    # Validate impacts (must be either +ve or -ve)
    for impact in impacts:
        if impact not in ['+', '-', '+ve', '-ve']:
            raise ValueError(f"Impacts must be either '+' or '-' (or '+ve' or '-ve'). Found: '{impact}'")
    
    # Normalize impacts to + or -
    impacts = ['+' if i in ['+', '+ve'] else '-' for i in impacts]
    
    return df, weights, impacts


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


def topsis(input_file, weights_str, impacts_str, output_file):
    """
    Main TOPSIS function
    
    Parameters:
    -----------
    input_file : str
        Path to input CSV file
    weights_str : str
        Comma-separated weights (e.g., "1,1,1,2")
    impacts_str : str
        Comma-separated impacts (e.g., "+,+,-,+")
    output_file : str
        Path to output CSV file
    """
    
    # Validate inputs
    df, weights, impacts = validate_inputs(input_file, weights_str, impacts_str)
    
    # Calculate TOPSIS
    topsis_score, rank = calculate_topsis(df, weights, impacts)
    
    # Add results to dataframe
    result_df = df.copy()
    result_df['Topsis Score'] = topsis_score
    result_df['Rank'] = rank
    
    # Save to output file
    try:
        result_df.to_csv(output_file, index=False)
        return result_df
    except Exception as e:
        raise IOError(f"Unable to write to file '{output_file}'. {str(e)}")


def main():
    """Command-line interface"""
    
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]
    
    try:
        topsis(input_file, weights_str, impacts_str, output_file)
        print(f"Success! Results saved to '{output_file}'")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
