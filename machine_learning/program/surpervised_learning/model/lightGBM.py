import lightgbm as lgb

class LgbClassification(object):
    def __init__(self, config):
        self.params =
        self.build()


    def build(self):
        lgb_classifer = lgb.LGBMClassifier(**self.params)

        return  lgb_classifer

