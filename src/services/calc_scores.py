import os
import pandas as pd

class CalcScores:
    def run(self):
        df = self.process_files()
        df_scores = self.generate_scores_df(df)
        return df_scores

    def process_files(self):
        files = 'src/result/filler'
        comment_column = []

        for filename in os.listdir(files):
            if filename.endswith('.csv'):
                filepath = os.path.join(files, filename)
                df = pd.read_csv(filepath)
                col = df.iloc[:, -1]
                comment_column.append(col)

        comments = pd.concat(comment_column, axis=0).reset_index(drop=True)
        df_comments = pd.DataFrame(comments)
        return df_comments

    def generate_scores_df(self, df_comments):
        comment_column = df_comments['COMMENT']

        total_comments = len(df_comments)
        total_ok = df_comments[comment_column == 'OK'].count()
        total_nok = df_comments[comment_column == 'NOK'].count()
        total_not_enough = df_comments[comment_column == 'Not enough information'].count()

        percentage_ok = float((total_ok / total_comments) * 100)
        percentage_nok = float((total_nok / total_comments) * 100)
        percentage_not_enough = float((total_not_enough / total_comments) * 100)

        scores = {
            "OK": f'{percentage_ok:.2f}%',
            "NOK": f'{percentage_nok:.2f}%',
            "NOT ENOUGH INFO": f'{percentage_not_enough:.2f}%'
        }

        df = pd.DataFrame(list(scores.items()), columns=['Category', 'Percentage'])
        return df