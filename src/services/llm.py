import os
from dotenv import load_dotenv

import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import AzureChatOpenAI

load_dotenv()

class CallLLM:
    def run(df, section_name):
        model = AzureChatOpenAI(
            azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"],
            openai_api_key = os.environ["AZURE_OPENAI_API_KEY"],
            deployment_name = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
            api_version = "2023-09-01-preview",
            temperature = 0.0
        )

        prompt_template = """
            You are an expert at selecting suppliers that will provide equipments to the company you work for.
            The suppliers fill a spreadsheet with their machines' specifications and based on that, you check if the answers correspond to what your company requires to make them an official supplier.

            In this task, you will analyze this data:
            
            ```
            {df_data}
            ```

            For each supplier answer, you will check if the answer can fill the requirements according to the other fields and return a JSON.

            GUIDELINES:
            - In the dataframe, you must add another field called "COMMENT" and it should only contain "OK" or "NOK". "OK" in case the supplier's answer can fill the requirement or "NOK" in case the supplier's answer does not fill the requirement.
            - You must return a valid JSON structure in your response, without any additional commentary, only the JSON.
            - The JSON structure will be converted to a Dataframe, so return a structure that will make the conversion possible.
            - If there's not enough information to make the analysis, in the field "COMMENT" just write "Not enough information".
            - Don't evaluate the suppliers answers if you don't know if they fill the requirements.
        """

        parser = JsonOutputParser()

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["df_data"]
        )

        chain = prompt | model | parser

        result = chain.invoke({"df_data": df})
        result_df = pd.DataFrame(result)
        result_df.to_csv(f'src/result/filler/{section_name.replace("/", "")}.csv', index=False)
        return result_df