import os
import logging
from openpyxl import load_workbook
import config
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("1-0_merge_series_for_same_country.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

SOURCE_DIRECTORY = './raw_data/security_daily_return'

files_by_group = {}

for root_directory, directories, files in os.walk(SOURCE_DIRECTORY):
    if root_directory != SOURCE_DIRECTORY:
        continue

    for file_name in files:
        if not file_name.endswith('.xlsm') or file_name.startswith('~'):
            continue
            
        filename_match = config.FILENAME_PATTERN.match(file_name)
        if not filename_match:
            continue
        
        file_info = filename_match.groupdict()
        country = file_info.get("country") or file_info.get("category")
        company_str = file_info.get("company")
        part_number = int(company_str) if company_str else 1
        
        start_year = file_info.get("start_year")
        end_year = file_info.get("end_year") or start_year
        if end_year and start_year != end_year:
            time_period = f"{start_year}-{end_year}"
        else:
            time_period = f"{start_year}"
        
        if not country:
            continue
            
        group_key = (country, time_period)
        if group_key not in files_by_group:
            files_by_group[group_key] = []
            
        file_path = os.path.join(root_directory, file_name)
        files_by_group[group_key].append((part_number, file_path))

for (country, time_period), file_list in files_by_group.items():
    if len(file_list) <= 1:
        logging.info(f"Skipping {country} {time_period}, no multiple files to merge.")
        continue
        
    file_list.sort(key=lambda x: x[0])
    
    base_file_path = file_list[0][1]
    logging.info(f"Loading base file: {base_file_path}")
    
    base_workbook = load_workbook(base_file_path, keep_vba=True)
    
    for part_number, part_file_path in file_list[1:]:
        logging.info(f"Merging part file: {part_file_path}")
        part_workbook = load_workbook(part_file_path, data_only=False)
        
        request_sheet_base = base_workbook["REQUEST_TABLE"]
        request_sheet_part = part_workbook["REQUEST_TABLE"]
        
        for row_index in range(7, request_sheet_part.max_row + 1):
            part_value = request_sheet_part.cell(row=row_index, column=5).value
            if part_value:
                base_cell = request_sheet_base.cell(row=row_index, column=5)
                if base_cell.value:
                    base_cell.value = f"{base_cell.value},{part_value}"
                else:
                    base_cell.value = part_value

        sheet_1_base = base_workbook.worksheets[1]
        sheet_1_part = part_workbook.worksheets[1]
        
        base_max_row = sheet_1_base.max_row
        for row_index in range(2, sheet_1_part.max_row + 1):
            for col_index in range(1, sheet_1_part.max_column + 1):
                cell_value = sheet_1_part.cell(row=row_index, column=col_index).value
                sheet_1_base.cell(row=base_max_row + row_index - 1, column=col_index, value=cell_value)

        for sheet_index in range(2, 7):
            sheet_base = base_workbook.worksheets[sheet_index]
            sheet_part = part_workbook.worksheets[sheet_index]
            
            base_max_column = sheet_base.max_column
            for row_index in range(1, sheet_part.max_row + 1):
                for col_index in range(2, sheet_part.max_column + 1):
                    cell_value = sheet_part.cell(row=row_index, column=col_index).value
                    sheet_base.cell(row=row_index, column=base_max_column + col_index - 1, value=cell_value)

    output_directory = os.path.join(SOURCE_DIRECTORY, country)
    os.makedirs(output_directory, exist_ok=True)
    
    output_filename = f"{country}_{time_period}.xlsm"
    output_path = os.path.join(output_directory, output_filename)
    
    logging.info(f"Saving merged file: {output_path}")
    base_workbook.save(output_path)

logging.info("All files merged successfully.")
