import matplotlib.pyplot as plt


class PlotClassificationResult(object):
    def __init__(self):
        pass

    def plot_roc_curve(self, roc_tapple, plot_show=False):
        tpr = roc_tapple[1]
        thresholds = roc_tapple[2]
        fpr = roc_tapple[0]

        plt.plot(fpr, tpr, marker='o')
        plt.xlabel('FPR: False positive rate')
        plt.ylabel('TPR: True positive rate')
        plt.grid()
        if plot_show:
            plt.show()


class PlotRegressionResult(object):
    def __init__(self):
        raise NotImplementedError
