class Trainer(object):
    def __init__(self, config):
        self.target =config.get('train_params', 'target_param')

    def fit(self, model, train_data_df):
        y_train = train_data_df[self.target]
        x_train = train_data_df.drop(columns=self.target)
        model.fit(x_train, y_train)

        return model