import sys

sys.path.append('../')
from transformer.transformer_csv import TransformerCsv
from model.lightGBM import LgbClassifier
from trainer.trainer import Trainer
from utils.set_randomseed import set_randomseed
from utils.plot_result import PlotClassificationResult
from utils.load_file import load_data, load_config


def titanic_data_transform(transformer):
    """
    transformerクラスのモジュールを用いてデータの整形など前処理を実施

    :param transformer:データ前処理クラス
    :return:titanic_training.csvを用いた生存予測を実施するための前処理済みデータ
    """
    drop_list = ["Name", "Ticket", "Cabin"]
    categorical_list = ["Sex", "Embarked"]

    transformer.fill_nan_mean()  # 欠損値の補完
    transformer.drop_columns(drop_list)
    transformer.encode_category_to_int(categorical_list=categorical_list)
    transformer.split_train_test_data(test_size=0.2)
    train_data, test_data = transformer.plot_train_test_data()

    return train_data, test_data


def main():
    config = load_config(config_file_name="lgb_titanic_config.ini")
    data = load_data(data_file_name="titanic_training.csv")
    set_randomseed()

    transformer = TransformerCsv(data_df=data)

    lgb_model = LgbClassifier(model_params_path=config.get('model_params', 'lgb_params_path'),
                              target_col=config.get('data_columns', 'target_col'))

    train_data, test_data = titanic_data_transform(transformer)

    lgb_trainer = Trainer()
    lgb_model = lgb_trainer.fit(model_class=lgb_model, train_data_df=train_data)

    eval_dict = lgb_model.eval(test_data=test_data)

    print("test acc:", eval_dict["acc"])
    print("conf_matrix", eval_dict["conf_matrix"])
    result_ploter = PlotClassificationResult()
    result_ploter.plot_roc_curve(roc_tapple=eval_dict["roc_curve"], plot_show=False)


if __name__ == '__main__':
    main()
