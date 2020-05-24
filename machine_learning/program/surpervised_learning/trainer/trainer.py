class Trainer(object):
    def __init__(self):
        pass

    def fit(self, model_class, train_data_df):
        y_train = train_data_df[model_class.target]
        x_train = train_data_df.drop(columns=model_class.target)
        model_class.model.fit(x_train, y_train)

        return model_class


class TrainerNeuralNetwork(Trainer):
    def __init__(self):
        super().__init__()

    def fit(self,
            model_class,
            train_data_df,
            epoch=20,
            batch_size=32,
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'],
            validation_split=0.2):

        y_train = train_data_df[model_class.target]
        x_train = train_data_df.drop(columns=model_class.target)
        model_class.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model_class.history = model_class.model.fit(x_train, y_train, epoch=epoch,
                                                    batch_size=batch_size, validation_split=validation_split)

        return model_class