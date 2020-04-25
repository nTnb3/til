import lightgbm as lgb
from sklearn.metrics import accuracy_score

class LgbClassifier(object):
    def __init__(self, model_params, target_col, use_model_param_config=False):
        self.target = target_col
        params = {}
        if use_model_param_config:
            params = model_params
        self._build(params)

    def _build(self, params):
        self.model = lgb.LGBMClassifier(**params)

    def _predict(self, test_data):
        return self.model.predict(test_data)

    def eval(self, test_data):
        y_data = test_data[self.target]
        x_data = test_data.drop(columns=self.target)

        predict = self._predict(x_data)
        acc_score = accuracy_score(y_data, predict)

        return acc_score


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
