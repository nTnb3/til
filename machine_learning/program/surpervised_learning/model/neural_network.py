import tensorflow as tf


class NeuralNetworkClassifier(object):
    def __init__(self, input_layer_num=3, middle_layer_list=[16,16], output_layer_num=1):
        self.input_layer_num = input_layer_num
        self.middle_layer_list = middle_layer_list
        self.output_layer_num = output_layer_num
        self._build()

    def _build(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(self.middle_layer_list[0],  activation="relu", input_shape=(self.input_layer_num,)))
        for layer in self.middle_layer_list[1:]:
            model.add(tf.keras.layers.Dense(layer, activation="relu"))
        model.add(tf.keras.layers.Dense(self.output_layer_num)


