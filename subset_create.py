import pandas as pd




def create_and_save_subsets(df, fiber_size_ranges, output_file):
    # Initialize an Excel writer object
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # For each experiment and each range, create a subset and save to an Excel sheet
        for exp_num in range(1, 5):  
            exp_data = df.filter(regex=f'EXP{exp_num}')  
            for idx, (lower_bound, upper_bound) in enumerate(fiber_size_ranges, start=1):
                # Build the column name for fiber diameter of the current experiment
                fiber_diam_col = f'FiberDiameter_EXP{exp_num}'
                # Check if the column exists in the filtered data
                if fiber_diam_col in exp_data.columns:
                    # Filter for the current range within the experiment's data
                    subset_df = exp_data[(exp_data[fiber_diam_col] >= lower_bound) & (exp_data[fiber_diam_col] <= upper_bound)]
                    # Define the sheet name based on the experiment number and subset index
                    sheet_name = f'EXP{exp_num}_Subset{idx}'
                    # Save the filtered subset to the Excel sheet
                    subset_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print("All subsets have been successfully saved to the Excel file.")


