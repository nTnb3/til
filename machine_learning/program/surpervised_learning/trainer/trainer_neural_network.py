import os

import numpy as np
import tensorflow as tf
from trainer.trainer import Trainer


class TrainerNeuralNetwork(Trainer):
    def __init__(self):
        self.model_path = "../data/models/"
        super().__init__()

    def _callbacks(self,
                   task_name,
                   is_earlystopping=True,
                   is_model_checkpoint=True,
                   is_lr_scheduler=True,
                   monitor='val_loss',
                   patience=2,
                   verbose=0,
                   restore_best_weights=True,
                   lr_start=0.03,
                   lr_end=0.001,
                   nb_epoch=1000):

        earlystopping = self._early_stopping(is_earlystopping=is_earlystopping, monitor=monitor, patience=patience,
                                            verbose=verbose, restore_best_weights=restore_best_weights)
        model_checkpoint = self._model_checkpoint(is_model_checkpoint=is_model_checkpoint, task_name=task_name)
        lr_scheduler = self._lr_scheduler(is_lr_scheduler=is_lr_scheduler, start=lr_start, stop=lr_end, nb_epoch=nb_epoch)

        callbacks = [earlystopping, model_checkpoint, lr_scheduler]
        return callbacks

    def _early_stopping(self, is_earlystopping, monitor, patience, verbose, restore_best_weights):
        if not is_earlystopping:
            return None
        earlystopping = tf.keras.callbacks.EarlyStopping(monitor=monitor, patience=patience,
                                                         verbose=verbose, restore_best_weights=restore_best_weights)
        return earlystopping

    def _model_checkpoint(self, is_model_checkpoint, task_name ,save_best_only=True):
        if not is_model_checkpoint:
            return None

        if not os.path.exists(self.model_path):
            os.mkdir(self.model_path)
        model_path = os.path.join(self.model_path, task_name, '{epoch:03d}_{val_loss:.4f}.h5')

        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=model_path, save_best_only=save_best_only)
        return model_checkpoint

    def _lr_scheduler(self, is_lr_scheduler, start, stop, nb_epoch):
        if not is_lr_scheduler:
            return None
        learning_rates = np.linspace(start, stop, nb_epoch)
        lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: float(learning_rates[epoch]))
        return lr_scheduler

    def fit(self,
            model_class,
            train_data_df,
            task_name,
            epoch=20,
            batch_size=32,
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'],
            validation_split=0.2):

        y_train = train_data_df[model_class.target_col]
        x_train = train_data_df.drop(columns=model_class.target_col)
        model_class.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model_class.history = model_class.model.fit(x_train, y_train, epoch=epoch,
                                                    batch_size=batch_size, validation_split=validation_split,
                                                    callbacks=self._callbacks(task_name=task_name))

        return model_class