import sys


import tensorflow as tf


sys.path.append('../')
from model.neural_network import NeuralNetworkClassifier
from transformer.transformer_csv import TransformerCsv
from trainer.trainer import Trainer
from utils.set_randomseed import set_randomseed
from utils.plot_result import PlotClassificationResult
from utils.load_file import load_data, load_config


def iris_data_transform(transformer):
    """
    transformerクラスのモジュールを用いてデータの整形など前処理を実施

    :param transformer:データ前処理クラス
    :return:titanic_training.csvを用いた生存予測を実施するための前処理済みデータ
    """
    transformer.encode_one_hot(encode_col="Name")
    transformer.split_train_test_data(test_size=0.2)
    train_data, test_data = transformer.plot_train_test_data()

    return train_data, test_data


def main():
    # config = load_config(config_file_name="lgb_titanic_config.ini")
    data = load_data(data_file_name="iris.csv")
    set_randomseed()
    transformer = TransformerCsv(data_df=data)
    nn_model = NeuralNetworkClassifier()
    train_data, test_data = iris_data_transform(transformer)
    nn_trainer = Trainer()
    nn_model = nn_trainer.fit(model_class=nn_model, train_data_df=train_data)


if __name__ == '__main__':
    main()
