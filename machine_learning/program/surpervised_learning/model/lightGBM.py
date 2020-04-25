import lightgbm as lgb


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
        self.model.predict(test_data)

    def eval(self, test_data):
        y_data = test_data[]
        x_data =
        return self.model.predict(test_data)


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
