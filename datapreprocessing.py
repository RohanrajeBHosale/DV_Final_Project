import os
import pandas as pd

# Path to the folder containing your datasets
data_folder = "raw datasets"  # Replace with the actual path
output_folder = "cleaned_datasets"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Dictionary to store loaded DataFrames
dataframes = {}

# Load, clean, and save each CSV file
for csv_file in csv_files:
    file_path = os.path.join(data_folder, csv_file)
    try:
        # Load dataset
        df = pd.read_csv(file_path)

        # Clean dataset (basic cleaning steps)
        df.dropna(inplace=True)  # Remove missing values
        df.reset_index(drop=True, inplace=True)  # Reset index

        # Add to dictionary with file name as key
        dataframes[csv_file] = df

        # Save cleaned dataset
        cleaned_file_path = os.path.join(output_folder, csv_file)
        df.to_csv(cleaned_file_path, index=False)

        print(f"Loaded, cleaned, and saved: {csv_file} (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

# Display keys of loaded DataFrames
print("Cleaned and saved datasets:", list(dataframes.keys()))