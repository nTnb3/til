import lightgbm as lgb


class LgbClassifier(object):
    def __init__(self, model_params={}, use_model_param_config=False):
        params = {}
        if use_model_param_config:
            params = model_params
        self._build(params)

    def _build(self, params):
        self.model = lgb.LGBMClassifier(**params)

    def eval(self, test_data):
        return self.model.predict(test_data)


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
