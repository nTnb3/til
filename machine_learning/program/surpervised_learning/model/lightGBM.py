import lightgbm as lgb


class LgbClassifier(object):
    def __init__(self, model_params={}, use_model_param_config=False):
        params = {}
        if use_model_param_config:
            params = model_params
        self.build(params)

    def build(self, params):
        self.model = lgb.LGBMClassifier(**params)


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
