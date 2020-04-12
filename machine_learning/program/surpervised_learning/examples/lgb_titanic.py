import os
import sys

import configparser
import pandas as pd

sys.path.append("..")
from transformaer.transformer_csv import TransformerCsv
from model.lightGBM import LgbClassifer
from trainer.trainer import Trainer
from utils.plot_classification_result import PlotClassificationResult


def load_config(config_file_name):
    config_dir = "../configs"
    config_path = os.path.join(config_dir, config_file_name)

    config_file = configparser.ConfigParser()
    config_file.read(config_path)

    return config_file


def load_data(data_file_name):
    data_dir = "../dataset"
    data_path = os.path.join(data_dir, data_file_name)

    data = pd.read_csv(data_path)

    return data


def titanic_data_transform(transformer):
    """
    transformerクラスのモジュールを用いてデータの整形など前処理を実施

    :param transformer:データ前処理クラス
    :return:titanic_training.csvを用いた生存予測を実施するための前処理済みデータ
    """
    transformer.fillna # 欠損値の補完
    train_data, test_data = transformer.plot_data()

    return train_data, test_data


def main():
    config = load_config(config_file_name="lgb_titanic.ini")
    data = load_data(data_file_name="titanic_training.csv")
    lgb_model = LgbClassifer(config=config)

    transformer = TransformerCsv(data=data, config=config)

    train_data, test_data = titanic_data_transform(transformer)

    lgb_trainer = Trainer(config=config)
    lgb_model = lgb_trainer.fit(model=lgb_model, train_data=train_data)

    pred_result = lgb_model.eval(test_data=test_data)

    ploter = PlotClassificationResult(result=pred_result)
    print("test acc:", ploter.calc_acc)


if __name__ == '__main__':
    main()
