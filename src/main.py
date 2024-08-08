from definitions.can_filler import can_filler_sections
from services.process_sheet import ProcessSheet
from services.index_sheet import IndexSheet
from services.df_classifier import DfClassifier
from services.calc_scores import CalcScores
from services.generate_excel import GenerateExcel

import streamlit as st

file_path_khs = 'files/KHS.xlsx'
file_path_krones = 'files/KRONES.xlsx'
file_path_sidel = 'files/SIDEL.xlsx'
sheet_filler = 'CAN Filler'
column_filler = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

st.title("GTS Technical Equalization")
uploaded_file = st.file_uploader("Choose a supplier file:", type=["xlsx"])

if uploaded_file is not None:
    # tratamento das planilhas
    process_sheet = ProcessSheet(uploaded_file, sheet_filler, column_filler)
    df = process_sheet.extract_info()
    index_sheet = IndexSheet(can_filler_sections, df)
    sections = index_sheet.run()

    # classificação com llm
    df_performance = DfClassifier.separate_df_performance(df, sections, "1.0 PERFORMANCE and WARRANTY")
    df_process = DfClassifier.separate_df(df, sections, "3.0 PROCESS")

    st.subheader("PERFORMANCE AND WARRANTY:")
    st.write(df_performance)
    st.divider()
    st.subheader("PROCESS:")
    st.write(df_process)
    st.divider()

    # cálculo de score
    scores = CalcScores()
    df_scores = scores.run()
    st.subheader("SCORES:")
    st.write(df_scores)
