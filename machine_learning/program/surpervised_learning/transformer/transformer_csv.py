from sklearn.model_selection import train_test_split


class TransformerCsv(object):
    def __init__(self, data_df):
        self.data_df = data_df

    def fill_nan(self):
        self.data_df = self.data_df.fillna(self.data_df.mean())

    def drop_nan_row(self):
        self.data_df = self.data_df.dropna(how='any', axis=0)

    def drop_nan_col(self):
        self.data_df = self.data_df.dropna(how='any', axis=1)

    def calc_moving_ave(self, param, window=3):
        self.data_df = self.data_df[param].rolling(window=window).mean()
