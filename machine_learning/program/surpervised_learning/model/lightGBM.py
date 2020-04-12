import lightgbm as lgb


class LgbClassifier(object):
    def __init__(self, model_params={}):
        assert isinstance(model_params, dict)
        self.params = model_params
        self.build()

    def build(self):
        lgb_classifier = lgb.LGBMClassifier(**self.params)

        return lgb_classifier


class LgbRegressor(object):
    def __init__(self):
        raise NotImplementedError
