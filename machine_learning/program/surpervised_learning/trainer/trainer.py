class Trainer(object):
    def __init__(self):
        pass

    def fit(self, model_class, train_data_df):
        y_train = train_data_df[model_class.target]
        x_train = train_data_df.drop(columns=model_class.target)
        model_class.model.fit(x_train, y_train)

        return model_class

    def fit_tf_nn(self, model_class, train_data_df):
        model_class.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])