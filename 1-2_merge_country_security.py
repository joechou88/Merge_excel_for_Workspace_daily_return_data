import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("1-2_merge_country_security.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

START_YEAR = 2015
END_YEAR = 2025
INPUT_DIRECTORY = './merge_datatype_csv/security_daily_return'
OUTPUT_DIRECTORY = './merge_country_csv/security_daily_return'

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

csv_files = [file_name for file_name in os.listdir(INPUT_DIRECTORY) if file_name.endswith('.csv')]
csv_files.sort()

output_filepath = os.path.join(OUTPUT_DIRECTORY, f"security-daily-return_{START_YEAR}-{END_YEAR}.csv")
is_first_file = True

logging.info(f"Starting to merge {len(csv_files)} files...")

try:
    with open(output_filepath, 'w', encoding='utf-8-sig') as output_file:
        for file_name in csv_files:
            file_path = os.path.join(INPUT_DIRECTORY, file_name)
            logging.info(f"Processing: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8-sig') as input_file:
                header_line = input_file.readline()
                
                # Keep the header only for the very first file
                if is_first_file:
                    output_file.write(header_line)
                    is_first_file = False
                
                # Append the rest of the file directly, effectively skipping the header
                for line in input_file:
                    output_file.write(line)

    logging.info(f"All files saved successfully. Final output: {output_filepath}")
except Exception as error:
    logging.error(f"An error occurred during merging: {error}")
