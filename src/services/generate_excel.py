import pandas as pd
import os

class GenerateExcel:
    def run():
        files = 'src/result/filler'
        excel_writer = pd.ExcelWriter('src/result/filler/can_filler.xlsx', engine='openpyxl')

        for filename in os.listdir(files):
            if filename.endswith('.csv'):
                file_path = os.path.join(files, filename)
                df = pd.read_csv(file_path)

                # add df to excel file as a tab
                sheet_name = os.path.splitext(filename)[0]
                df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

        excel_writer.close()