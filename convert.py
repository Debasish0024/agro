import pandas as pd

# Load the datasets
price_data = pd.read_excel('Agmarknet_Price_Report.xlsx')
rainfall_data_2021 = pd.read_excel('Blockwise Daily Rainfall 2021.xlsx', skiprows=2)
rainfall_data_2022 = pd.read_excel('Blockwise Daily Rainfall 2022.xlsx', skiprows=2)
rainfall_data_2023 = pd.read_excel('Blockwise Daily Rainfall 2023.xlsx', skiprows=2)

# Clean and format the price data by setting proper headers
price_data.columns = price_data.iloc[0]
price_data = price_data.drop(0).reset_index(drop=True)

# Extract relevant columns and remove 'Market Name', 'Grade', 'Variety'
price_data_cleaned = price_data[['District Name', 'Modal Price (Rs./Quintal)', 'Price Date']]

# Convert 'Price Date' to datetime format
price_data_cleaned['Price Date'] = pd.to_datetime(price_data_cleaned['Price Date'])

# Extract month and year from 'Price Date'
price_data_cleaned['Month'] = price_data_cleaned['Price Date'].dt.month
price_data_cleaned['Year'] = price_data_cleaned['Price Date'].dt.year

# Reshape rainfall data to have a single 'Month' column and corresponding 'Rainfall' values
rainfall_data_2021_melted = rainfall_data_2021.melt(id_vars=['District'], 
                                                    var_name='Month', 
                                                    value_name='Rainfall')
rainfall_data_2022_melted = rainfall_data_2022.melt(id_vars=['District'], 
                                                    var_name='Month', 
                                                    value_name='Rainfall')
rainfall_data_2023_melted = rainfall_data_2023.melt(id_vars=['District'], 
                                                    var_name='Month', 
                                                    value_name='Rainfall')

# Convert month names to numeric format to match the price data's 'Month' column
month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 
                 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
                 'November': 11, 'December': 12}

rainfall_data_2021_melted['Month'] = rainfall_data_2021_melted['Month'].map(month_mapping)
rainfall_data_2022_melted['Month'] = rainfall_data_2022_melted['Month'].map(month_mapping)
rainfall_data_2023_melted['Month'] = rainfall_data_2023_melted['Month'].map(month_mapping)

# Add 'Year' column
rainfall_data_2021_melted['Year'] = 2021
rainfall_data_2022_melted['Year'] = 2022
rainfall_data_2023_melted['Year'] = 2023

# Merge the rainfall data into a single DataFrame
rainfall_data_combined = pd.concat([rainfall_data_2021_melted, rainfall_data_2022_melted, rainfall_data_2023_melted], ignore_index=True)

# Merge the price data with the rainfall data based on 'District Name', 'Year', and 'Month'
merged_data = pd.merge(price_data_cleaned, 
                       rainfall_data_combined[['District', 'Year', 'Month', 'Rainfall']], 
                       how='left', 
                       left_on=['District Name', 'Year', 'Month'], 
                       right_on=['District', 'Year', 'Month'])

# Handle cases where rainfall data for a specific year isn't available (e.g., 2024)
merged_data['Rainfall'] = merged_data['Rainfall'].fillna('NULL')

# Drop unnecessary columns: 'District', 'Price Date', 'Month', 'Year'
merged_data = merged_data.drop(columns=['District', 'Month', 'Year'])

# Convert 'Price Date' to store only the date part (without time)
merged_data['Date'] = merged_data['Price Date'].dt.date

# Drop the original 'Price Date' column
merged_data = merged_data.drop(columns=['Price Date'])

# Save the merged dataset to an Excel file
merged_data.to_excel('Merged_Price_Rainfall_Data3.xlsx', index=False)

# Print a confirmation message
print("Merged dataset saved as 'Merged_Price_Rainfall_Data2.xlsx'")
