class Trainer(object):
    def __init__(self, config):
        self.target =config.get('train_params', 'target_param')

    def fit(self, model, train_data):