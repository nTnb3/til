from sklearn.model_selection import train_test_split


class TransformerCsv(object):
    def __init__(self, data_df, config):
        self.data_df = data_df
        self.config = config

    def fill_nan_mean(self):
        self.data_df = self.data_df.fillna(self.data_df.mean())

    def drop_nan_row(self):
        self.data_df = self.data_df.dropna(how='any', axis=0)

    def drop_nan_col(self):
        self.data_df = self.data_df.dropna(how='any', axis=1)

    def calc_moving_ave(self, param, window=3):
        self.data_df = self.data_df[param].rolling(window=window).mean()

    def drop_columns(self, drop_list):
        for drop_col in drop_list:
            self.data_df = self.data_df.drop(drop_col)

    def encode_category_to_ordinal_int(self, encode_ordinal_map_dict):
        for ordinal_categorical_param, ordinal_map in encode_ordinal_map_dict.item():
            self.data_df[ordinal_categorical_param] = self.data_df[ordinal_categorical_param].map(ordinal_map)

    def encode_category_to_int(self, categorical_list):
        for categorical_param in categorical_list:
            self.data_df[categorical_param] = self.data_df[categorical_param].astype('category').cat.codes

    def split_train_test_data(self, test_size=0.4, shuffle=False):
        self.train_df, self.test_df = train_test_split(self.data_df, test_size=test_size, shuffle=shuffle)

    def plot_data(self):
        return self.train_df, self.test_df

