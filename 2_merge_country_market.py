import os
import logging
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("2_merge_country_market.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

INPUT_FILEPATH = './raw_data/market_daily_return/market-daily-return_2000-2025.xlsm'
OUTPUT_DIRECTORY = './merge_country_csv/market_daily_return'
OUTPUT_FILEPATH = f'{OUTPUT_DIRECTORY}/market-daily-return_2000-2025.csv'

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

logging.info(f"Loading excel file: {INPUT_FILEPATH}")
excel_file = pd.ExcelFile(INPUT_FILEPATH)

logging.info("Parsing REQUEST_TABLE mapping...")
request_table_df = pd.read_excel(excel_file, sheet_name='REQUEST_TABLE', header=None)

# Column K is index 10, column M is index 12, starting from row 7 (index 6)
mapping_df = request_table_df.iloc[6:, [10, 12]].dropna()
mapping_df.columns = ['sheet_reference', 'country_name']

sheet_to_country_mapping = {}
for _, row in mapping_df.iterrows():
    reference = str(row['sheet_reference'])
    country = str(row['country_name']).strip()
    
    # Extract sheet name, handling optional single quotes (e.g., "'Sheet1'!A1" or "Sheet1!A1")
    sheet_name = reference.split("!")[0].replace("'", "")
    sheet_to_country_mapping[sheet_name] = country

merged_df = None

# Process and merge sheets sequentially
for sheet_name in excel_file.sheet_names:
    if sheet_name == 'REQUEST_TABLE':
        continue
        
    country_name = sheet_to_country_mapping.get(sheet_name)
    if not country_name:
        continue
        
    logging.info(f"Processing sheet: {sheet_name} -> {country_name}")
    
    # Data starts at A3, so set header=1 to use row 2 as column names
    sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name, header=1)
    
    # Extract only the first two columns (Date and Value)
    sheet_df = sheet_df.iloc[:, :2]
    sheet_df.columns = ['Date', country_name]
    
    # Convert Date column and drop invalid rows to ensure a clean time series
    sheet_df['Date'] = pd.to_datetime(sheet_df['Date'], errors='coerce')
    sheet_df = sheet_df.dropna(subset=['Date'])
    
    if merged_df is None:
        merged_df = sheet_df
    else:
        merged_df = pd.merge(merged_df, sheet_df, on='Date', how='outer')

if merged_df is not None:
    # Sort by date to maintain chronological order
    merged_df = merged_df.sort_values('Date')
    
    logging.info(f"Saving output to: {OUTPUT_FILEPATH}")
    merged_df.to_csv(OUTPUT_FILEPATH, index=False, encoding='utf-8-sig')
    logging.info("All files saved successfully.")
else:
    logging.warning("No data was merged.")
