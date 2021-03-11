from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import functools

class YearTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, column, last_year=None):
        self.column = column
        self.last_year = last_year

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.last_year is None:
            # seems to invalid values
            self.last_year = int(pd.to_datetime(X['date']).max().year)
        X.loc[:, self.column] = self.last_year - X[self.column]
        return X

class ColumnToDateFormat(BaseEstimator, TransformerMixin):

    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X[self.column] = pd.to_datetime(X[self.column]).dt.date
        return X

class NormalizeAreaByPrice(BaseEstimator, TransformerMixin):

    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y):
        X['normalized_' + self.column] = X[self.column] / X['price']
        X.drop(columns=self.column)
        return X


class Drop33Rooms(BaseEstimator, TransformerMixin):
    """
    quite unrepresantive data
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.drop(X[X['bedrooms'] == 33].index, axis=0)
        return X

class DropColumns(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.drop(columns=self.columns)
        return X

class DummyTransform(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = pd.get_dummies(data=X, columns=self.columns)
        return X


