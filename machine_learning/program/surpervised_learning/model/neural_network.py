from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve

import tensorflow as tf


class NeuralNetworkClassifier(object):
    def __init__(self, target_col, input_layer_num=3, middle_layer_list=[16,16], output_layer_num=1):
        self.target_col = target_col
        self.input_layer_num = input_layer_num
        self.middle_layer_list = middle_layer_list
        self.output_layer_num = output_layer_num
        self.histry = None
        self.model = self._build()

    def _build(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(self.middle_layer_list[0],  activation="relu", input_shape=(self.input_layer_num,)))
        for layer in self.middle_layer_list[1:]:
            model.add(tf.keras.layers.Dense(layer, activation="relu"))
        model.add(tf.keras.layers.Dense(self.output_layer_num, activation='softmax'))

        return model

    def _predict(self, test_data):
        predict = self.model.predict(test_data)
        predict_proba = self.model.predict_proba(test_data, batch_size=32, verbose=0)
        return predict, predict_proba

    def _calc_acc(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)

    def _calc_conf_matrix(self, y_true, y_pred):
        return confusion_matrix(y_true, y_pred)

    def _calc_roc_curve(self, y_ture, y_pred):
        return roc_curve(y_ture, y_pred, drop_intermediate=False)

    def eval(self, test_data):
        eval_dict = {}
        y_data = test_data[self.target]
        x_data = test_data.drop(columns=self.target)
        predict, predict_prob = self._predict(x_data)
        eval_dict["acc"] = self._calc_acc(y_true=y_data, y_pred=predict)
        eval_dict["conf_matrix"] = self._calc_conf_matrix(y_true=y_data, y_pred=predict)
        eval_dict["roc_curve"] = self._calc_roc_curve(y_ture=y_data, y_pred=predict)
        eval_dict["pred_prob"] = predict_prob

        return eval_dict
