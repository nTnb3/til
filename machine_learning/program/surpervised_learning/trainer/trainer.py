class Trainer(object):
    def __init__(self):
        pass

    def fit(self, model, train_data_df):
        y_train = train_data_df[model.target]
        x_train = train_data_df.drop(columns=model.target)
        model.fit(x_train, y_train)

        return model