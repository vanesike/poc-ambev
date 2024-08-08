import pandas as pd
from openpyxl import load_workbook

class ProcessSheet:
    def __init__(self, file_path, sheet_name, column_letters):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.column_letters = column_letters

    def extract_info(self):
        # Load workbook and sheet
        wb = load_workbook(self.file_path, data_only=True)
        sheet = wb[self.sheet_name]

        # Read column names from row 15
        column_names = [sheet[f'{col}15'].value for col in self.column_letters]

        # Initialize a dictionary to store the data
        data = {col: [] for col in column_names}

        # Extract values from each column, ignoring the first 13 cells and row 15
        for col_letter, column_name in zip(self.column_letters, column_names):
            column_data = [cell.value for cell in sheet[col_letter] if cell.row > 13]
            # Add data to the corresponding list
            data[column_name] = column_data

        # Find the maximum length of the lists
        max_length = max(len(lst) for lst in data.values())

        # Standardize the length of the lists with missing values (None)
        for key in data:
            while len(data[key]) < max_length:
                data[key].append(None)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data)

        return df
