import tensorflow as tf

from trainer import Trainer

class TrainerNeuralNetwork(Trainer):
    def __init__(self):
        super().__init__()

    def _callbacks(self, ):
        earlystopping = tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)
        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
                 '../data/temp/mnist_sequential_{epoch:03d}_{val_loss:.4f}.h5',
                 save_best_only=True

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