import errno
import os
import sys

import configparser
import pandas as pd

sys.path.append('../')
from transformer.transformer_csv import TransformerCsv
from model.lightGBM import LgbClassifier
from trainer.trainer import Trainer
# from utils.plot_classification_result import PlotClassificationResult


def load_config(config_file_name):
    config_dir = "../configs"
    config_path = os.path.join(config_dir, config_file_name)
    config_file = configparser.ConfigParser()
    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_file.read(config_path)

    return config_file


def load_data(data_file_name):
    data_dir = "../dataset"
    data_path = os.path.join(data_dir, data_file_name)
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        print("FileNotFoundError")
    return data


def titanic_data_transform(transformer):
    """
    transformerクラスのモジュールを用いてデータの整形など前処理を実施

    :param transformer:データ前処理クラス
    :return:titanic_training.csvを用いた生存予測を実施するための前処理済みデータ
    """

    drop_list = ["Name", "Ticket", "Cabin"]
    label_encoding_list = ["Pclass"]
    categorical_list = ["Survived", "Sex", "Embarked"]

    transformer.fill_nan_mean()  # 欠損値の補完
    transformer.drop_columns(drop_list)

    transformer.split_train_test_data()
    train_data, test_data = transformer.plot_data()

    return train_data, test_data


def main():
    config = load_config(config_file_name="lgb_titanic_config.ini")
    data = load_data(data_file_name="titanic_training.csv")

    transformer = TransformerCsv(data_df=data, )

    lgb_model = LgbClassifier(model_params=config.get('model_params', 'lgb_params'))

    train_data, test_data = titanic_data_transform(transformer)

    lgb_trainer = Trainer(config=config)
    lgb_model.model = lgb_trainer.fit(model=lgb_model.model, train_data_df=train_data)

    pred_result = lgb_model.eval(test_data=test_data)

    ploter = PlotClassificationResult(result=pred_result)
    print("test acc:", ploter.calc_acc)


if __name__ == '__main__':
    main()
