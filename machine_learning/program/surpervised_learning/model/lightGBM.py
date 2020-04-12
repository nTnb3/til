import lightgbm as lgb


class LgbClassification(object):
    def __init__(self, config):
        self.params = config.get('model_params', 'lgb_params')
        if self.params is None:
            self.params = {}

        self.build()

    def build(self):
        lgb_classifier = lgb.LGBMClassifier(**self.params)

        return lgb_classifier


class LgbRegression(object):
    def __init__(self):
        raise NotImplementedError
