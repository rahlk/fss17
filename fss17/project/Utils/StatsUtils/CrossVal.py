from __future__ import print_function, division

from pdb import set_trace

import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import LeaveOneOut

from itertools import islice


class TrainTestValidate:
    def __init__(self):
        pass

    @classmethod
    def split(cls, datapaths):
        """
        Generate a train, test, validate set from data paths
        
        :param datapaths: list for file paths. Ex: ["path/to/file1.csv", "path/to/file2.csv", "path/to/file3.csv"
                                                                            , "path/to/file4.csv", "path/to/file5.csv"]
        :return: a sliding window (of width 3) over datapath
        s -> (s0,s1,s2), (s1,s2,s3), (s2, s3, s4), ...         
        
        Courtesy: https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator-in-python
        """

        it = iter(datapaths)
        result = tuple(islice(it, 3))
        if len(result) == 3:
            yield result
        else:
            for elem in it:
                result = result[1:] + (elem,)
                yield result


class CrossValidation:
    def __init__(self):
        pass

    @classmethod
    def split(cls, dframe, ways=5):
        col = dframe.columns
        X = dframe
        y = dframe[dframe.columns[-1]]
        skf = StratifiedKFold(n_splits=ways, shuffle=True)
        for train_idx, test_idx in skf.split(X, y):
            yield pd.DataFrame(X.values[train_idx], columns=col), \
                  pd.DataFrame(X.values[test_idx], columns=col)


class LeaveOneOutValidation:
    def __init__(self):
        pass

    @classmethod
    def split(cls, dframe, ways=5):
        col = dframe.columns
        X = dframe
        y = dframe[dframe.columns[-1]]
        loo = LeaveOneOut()
        for train_idx, test_idx in loo.split(X, y):
            yield pd.DataFrame(X.values[train_idx], columns=col), \
                  pd.DataFrame(X.values[test_idx], columns=col)
