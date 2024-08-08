class IndexSheet:
    def __init__(self, sections, df):
        self.sections = sections
        self.df = df
    
    def run(self):
        indexes = self.get_section_index()
        return self.add_indexes(indexes)

    def is_section(self, item):
        return isinstance(item, str) and item in self.sections
    
    def get_section_index(self):
        section_indexes = self.df[self.df['ITEM'].apply(self.is_section)].index.tolist()
        section_indexes.append(len(self.df))
        return section_indexes

    def add_indexes(self, indexes):
        for i in range(len(indexes) - 1):
            start_idx = indexes[i]
            end_idx = indexes[i + 1]
            section_name = self.df.loc[start_idx, 'ITEM']
            self.sections[section_name]["start"] = start_idx + 1 
            self.sections[section_name]["end"] = end_idx
        
        return self.sections