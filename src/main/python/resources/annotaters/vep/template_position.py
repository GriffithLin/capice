from src.main.python.resources.annotaters.vep.template import Template
from abc import abstractmethod
import pandas as pd
import numpy as np


class TemplatePosition(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplatePosition, self).__init__(
            name=name,
            usable=usable
        )

    @property
    @abstractmethod
    def columns(self):
        return [None, None]

    @property
    def pos_col(self):
        return self.columns[0]

    def process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = dataframe[self.name].str.split(
            '/',
            expand=True
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace(
            '?-',
            '',
            regex=False
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace(
            '-?',
            '',
            regex=False
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.split(
            '-', expand=True)[0]

        for column in self.columns:
            dataframe.loc[
                dataframe[dataframe[column] == ''].index,
                column
            ] = np.nan
            dataframe[column] = dataframe[column].astype(float)
        return dataframe
