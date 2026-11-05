## Merge series for same country
The script identifies and merges fragmented `.xlsm` files belonging to the same country and time period (e.g., `Germany1`, `Germany2`) into a single, consolidated `.xlsm` workbook. It automates structural alignment across different worksheets to ensure data integrity.

- **Input:** Multi-part `.xlsm` files located in `./raw_data/security_daily_return/`
- **Output:** Merged `.xlsm` files saved to a designated country subdirectory `./raw_data/security_daily_return/{country}/` (e.g., `{country}_{year}.xlsm` or `{country}_{start_year}-{end_year}.xlsm`)

**Data Merging Rules:**
- **REQUEST_TABLE**: Merges query variables in Column E (starting from row 7 downwards). Values from secondary files are appended and concatenated with a comma (e.g., combining `FGER1` and `FGER2` into `FGER1,FGER2`).
- **工作表1**: Appends data vertically (row-wise). The top header row of secondary files is ignored to maintain a single continuous header row.
- **工作表2 ~ 工作表6**: Appends data horizontally (column-wise). The first column (Column A) of secondary files is ignored to prevent duplicating the shared date/index column.

## Merge datatype for security daily return
The script extracts and merges daily security data across multiple worksheets within each `.xlsm` file into a unified dataset. It automatically maps geographical codes and aligns time-series variables for each company.

- **Input:** `.xlsm` files located in `./raw_data/security_daily_return/`
- **Output:** Merged `.csv` files saved to `./merge_datatype_sas/security_daily_return/` (e.g., `{country}_sec_ret_2015_2025.csv`)

**Data Mapping & Extraction Rules:**
* **DSCD**: Extracted horizontally starting from cell B2 in Worksheet 2.
* **date**: Extracted vertically starting from cell A3 in Worksheet 2 (dates are structurally aligned across Worksheets 2 through 6).
* **year**: Derived directly from the `date` field and stored as a numeric value.
* **country**: Parsed directly from the source filename.
* **country_code1 & country_code2**: Mapped from the parsed `country` name using the `./raw_data/country_code.xlsx` reference file.
* **ri (Stock return index)**: Mapped from Worksheet 2 based on the corresponding `date` and `DSCD`.
* **li (Local market return index)**: Mapped from Worksheet 3.
* **mv (Market Value)**: Mapped from Worksheet 4.
* **cso (Common shares outstanding)**: Mapped from Worksheet 5.
* **vo (Daily trading volume)**: Mapped from Worksheet 6.

**Processing Rules & Exception Handling:**
- **Pre-processed Data Priority:** Skips files with numeric suffixes (e.g., `Germany1`) if a base folder (e.g., `Germany/`) in `./raw_data/security_daily_return/` exists, ensuring we use the merged files by `1-0_merge_series_for_same_country.py` instead.
- **Deduplication:** For overlapping time periods across multiple files, the script removes duplicate rows based on company (`DSCD`) and `date`, retaining only the latest entry.
- **Workspace Error Handling (Missing Values):** If the script encounters a Workspace error string starting with `$$ER` in the first data row (row 3) for a specific company, it automatically replaces all subsequent data points for that company with a `.` to represent missing values consistently. Handled errors include:
  - `$$ER: E100,NO WORLDSCOPE DATA FOR THIS CODE`
  - `$$ER: 2311,NO DATA AVAILABLE`
  - `$$ER: 2361,NO DATA AVAILABLE`
  - `$$ER: 2380,NO DATA IN REQUESTED PERIOD`

## Merge country market returns
The script extracts time-series data from a consolidated workbook and merges individual country worksheets into a single `.csv` file. It automates structural mapping to align all countries chronologically.

- **Input:** A multi-sheet `.xlsm` file located in `./raw_data/market_daily_return/market-return_2000-2025.xlsm`
- **Output:** A single merged `.csv` file saved to `./merge_country_csv/market_daily_return/market-return_2000-2025.csv`

**Data Merging Rules:**
- **REQUEST_TABLE**: Serves as a mapping directory. Reads Column K and Column M (starting from row 7 downwards) to dynamically link each worksheet (e.g., `工作表1`) to its respective country (e.g., `Australia`).
- **工作表1, 工作表2, ...**: Appends data horizontally (column-wise) based on an outer join of the shared `Date` column. The top header row of each sheet is ignored to start reading strictly from the time-series data, and the value column is renamed to the mapped country name.
