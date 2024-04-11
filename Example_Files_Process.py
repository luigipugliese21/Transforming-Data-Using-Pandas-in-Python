import pandas as pd
import os
from datetime import datetime

# Directory containing the input .xlsx files
input_directory_path = "Enter Input Path..."

# Path and filename for the output CSV file
output_csv_path = "Enter Output Path..."

# Define the expected headers
expected_headers = [
   "file headers..."]

def process_csv_files(input_directory_path, output_csv_path):
    combined_df = pd.DataFrame()

    for file_name in os.listdir(input_directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_directory_path, file_name)
            
            # Read the CSV file using row 12 as the header
            df = pd.read_csv(file_path, header=11)  # header=11 because pandas is 0-indexed
            
            # Check if the actual headers match the expected headers
            actual_headers = df.columns.tolist()
            if actual_headers != expected_headers:
                raise ValueError(f"Header mismatch in file: {file_name} \nExpected headers: {expected_headers} \nFound headers: {actual_headers}")
            
            # Add 'INT PRM' column between position 19 and 20
            df.insert(19, 'INT PRM', pd.NA)
            
            # Convert file name date to 'AccountingCycle'
            file_date_str = file_name[:8]
            accounting_cycle_date = datetime.strptime(file_date_str, '%m.%d.%y').strftime('%m/%d/%Y')
            df['AccountingCycle'] = accounting_cycle_date
            
            # Append processed DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Save the combined DataFrame to the specified CSV file
    combined_df.to_csv(output_csv_path, index=False)
    print(f"All files processed and combined data saved to {output_csv_path}")

# Run the function with the specified paths
process_csv_files(input_directory_path, output_csv_path)
