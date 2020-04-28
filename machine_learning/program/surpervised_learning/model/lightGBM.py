from csv import DictReader
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix



class LgbClassifier(object):
    def __init__(self, model_params_path, target_col, use_model_param_config=False):
        self.target = target_col
        params = {}
        if use_model_param_config:
            params = self._read_model_params(model_params_path)
        self._build(params)

    def _build(self, params):
        self.model = lgb.LGBMClassifier(**params)

    def _read_model_params(self, model_params_path):
        with open(model_params_path, newline='') as csvfile:
            model_params = DictReader(csvfile)
            return model_params

    def _predict(self, test_data):
        return self.model.predict(test_data)

    def _calc_acc(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)

    def _calc_conf_matrix(self, y_true, y_pred):
        return confusion_matrix(y_true, y_pred)

    def eval(self, test_data):
        eval_def = {}
        y_data = test_data[self.target]
        x_data = test_data.drop(columns=self.target)
        predict = self._predict(x_data)

        eval_def["acc"] = self._calc_acc(y_true=y_data, y_pred=predict)
        eval_def["conf_matrix"] = self._calc_conf_matrix(y_true=y_data, y_pred=predict)

        return eval_def


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
