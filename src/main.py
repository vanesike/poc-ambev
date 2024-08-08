from definitions.can_filler import can_filler_sections
from services.process_sheet import ProcessSheet
from services.index_sheet import IndexSheet
from services.df_classifier import DfClassifier
from services.calc_scores import CalcScores
from services.generate_excel import GenerateExcel

file_path_khs = 'files/KHS.xlsx'
file_path_krones = 'files/KRONES.xlsx'
file_path_sidel = 'files/SIDEL.xlsx'
sheet_filler = 'CAN Filler'
column_filler = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# tratamento das planilhas
process_sheet = ProcessSheet(file_path_khs, sheet_filler, column_filler)
df = process_sheet.extract_info()
index_sheet = IndexSheet(can_filler_sections, df)
sections = index_sheet.run()

# classificação com llm
df_performance = DfClassifier.separate_df_performance(df, sections, "1.0 PERFORMANCE and WARRANTY")
df_process = DfClassifier.separate_df(df, sections, "3.0 PROCESS")
df_accessories = DfClassifier.separate_df(df, sections, "5.0 FILLER ACCESSORIES")

# cálculo de score
scores = CalcScores()
scores.run()

# planilha final
excel = GenerateExcel.run()
