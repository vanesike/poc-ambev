import pandas as pd
from services.llm import CallLLM

class DfClassifier:
    def separate_df(df_supplier, sections, section_name):
        df = df_supplier.iloc[sections[section_name]['start']:sections[section_name]['end']].reset_index(drop=True).rename(columns={'CNV': 'Charachteristic', 'UNIT': 'Instruction/Comments'}).drop(index=0, columns=['ITEM', 'ITEM DESCRIPTION', 'INDEX', 'Instruction / Comments', None]).to_csv(index=False)
        CallLLM.run(df, section_name)

    def separate_df_performance(df_supplier, sections, section_name):
        df = df_supplier.iloc[sections[section_name]['start']:sections[section_name]['end']].reset_index(drop=True).drop(index=[0], columns=['ITEM', None]).to_csv(index=False)
        CallLLM.run(df, section_name)

    def separate_df_utilities(df_supplier, sections, section_name):
        df = df_supplier.iloc[sections[section_name]['start']:sections[section_name]['end']].reset_index(drop=True).drop(index=[0], columns=['ITEM', 'ITEM DESCRIPTION', 'Instruction / Comments']).rename(columns={'CNV': 'Characteristic', 'INDEX': 'Instruction / Comments'}).dropna(subset=['Characteristic']).to_csv(index=False)
        CallLLM.run(df, section_name)

    def separate_df_maintenance(df_supplier, sections, section_name):
        df = df_supplier.iloc[sections[section_name]['start']:sections[section_name]['end']].reset_index(drop=True).drop(index=[0], columns=['ITEM', 'INDEX', 'ITEM DESCRIPTION', 'Instruction / Comments']).rename(columns={'CNV': 'Characteristic', 'UNIT': 'Instruction', None: 'Comments'}).dropna(subset=['Characteristic']).to_csv(index=False)
        CallLLM.run(df, section_name)

    def separate_df_zone(df_supplier, sections, section_name):
        df = df_supplier.iloc[sections[section_name]['start']:sections[section_name]['end']].reset_index(drop=True).drop(index=[0], columns=['ITEM', 'UNIT', 'INDEX']).rename(columns={'CNV': 'Zone', 'ITEM DESCRIPTION': 'Detail','Instruction / Comments': 'Instruction', None: 'Comments'}).to_csv(index=False)
        CallLLM.run(df, section_name)

        