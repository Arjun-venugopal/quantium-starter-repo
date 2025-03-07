import pandas as pd
import glob

# Get all CSV files from the data folder
data_files = glob.glob('data/*.csv')

# Load and process each file
dataframes = []

for file in data_files:
    try:
        df = pd.read_csv(file) 
        
        # Ensure 'product' column exists
        if 'product' not in df.columns:
            print(f"Warning: 'product' column not found in {file}. Skipping this file.")
            continue
        
        # Filter for only "pink morsel" (case-insensitive)
        df = df[df['product'].str.lower() == 'pink morsel']
        
        # Clean the price column by removing '$' and converting to numeric
        df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

        # Ensure quantity and price are numeric
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Calculate sales (quantity * price)
        df['sales'] = df['quantity'] * df['price']
        
        # Keep only relevant columns
        df = df[['sales', 'date', 'region']]
        
        # Add processed dataframe to list
        dataframes.append(df)
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Combine all data
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)
    
    # Group by date and region and sum sales if needed
    final_df = final_df.groupby(['date', 'region'], as_index=False).sum()
    
    # Save to a new CSV file
    final_df.to_csv('data/processed_data.csv', index=False)
    print("Data processing complete! 'processed_data.csv' has been created.")
else:
    print("No valid data found to process.")
