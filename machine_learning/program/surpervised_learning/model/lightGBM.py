import lightgbm as lgb


class LgbClassifier(object):
    def __init__(self, model_params={}, use_model_param_config=False):
        if use_model_param_config:
            self.params = model_params
        self.build()

    def build(self):
        self.lgb_classifier = lgb.LGBMClassifier(**self.params)


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
