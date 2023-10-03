from openpyxl import styles
import pandas as pd


def create_xlsx_report(data, title, time_period):
    # Ensure title is a string
    if isinstance(title, list) and len(title) == 1:
        title = title[0]
    elif not isinstance(title, str):
        raise ValueError("Title should be a string")
    # Convert data to DataFrame if it's a list of DataFrames
    if isinstance(data, list) and all(isinstance(i, pd.DataFrame) for i in data):
        data = pd.concat(data)

    xlsx_file = f"{title} {time_period}.xlsx"
    with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer: # pylint: disable=abstract-class-instantiated
        data.to_excel(writer, index=False, startrow=2)  # Start writing CSV data from the third row
        
        # Get the active worksheet
        sheet = writer.sheets['Sheet1']
        
        # Set column widths
        for column in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            sheet.column_dimensions[column[0].column_letter].width = max_length
        
        # Define a cell style for bold and larger font
        bold_large_font = styles.Font(bold=True, size=14)
        
        # Insert the title, time period, and total count in the specified cells
        title_cell = sheet['B1']
        title_cell.value = title
        title_cell.font = bold_large_font
        
        date_cell = sheet['D1']
        date_cell.value = time_period
        date_cell.font = bold_large_font
        
        total_cell = sheet['F1']
        total_cell.value = f"Total Count: {len(data)}"
        total_cell.font = bold_large_font
        
    return [xlsx_file]


def create_xlsx_report_multi(dataframes, titles, time_period):
    files = []
    for data, title in zip(dataframes, titles):
        # Ensure data is a DataFrame
        if isinstance(data, list):
            raise ValueError("Each item in dataframes should be a DataFrame")

        xlsx_file = f"{title} {time_period}.xlsx"
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer: # pylint: disable=abstract-class-instantiated
            data.to_excel(writer, index=False, startrow=2)
            sheet = writer.sheets['Sheet1']

        xlsx_file = f"{title} {time_period}.xlsx"
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer: # pylint: disable=abstract-class-instantiated
            data.to_excel(writer, index=False, startrow=2)
            sheet = writer.sheets['Sheet1']
            # Set column widths
        for column in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            sheet.column_dimensions[column[0].column_letter].width = max_length
        
        # Define a cell style for bold and larger font
        bold_large_font = styles.Font(bold=True, size=14)
        
        # Insert the title, time period, and total count in the specified cells
        title_cell = sheet['B1']
        title_cell.value = title
        title_cell.font = bold_large_font
        
        date_cell = sheet['D1']
        date_cell.value = time_period
        date_cell.font = bold_large_font
        
        total_cell = sheet['F1']
        total_cell.value = f"Total Count: {len(data)}"
        total_cell.font = bold_large_font
        files.append(xlsx_file)

    return files
