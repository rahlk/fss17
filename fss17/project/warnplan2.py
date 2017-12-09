"""
Compare Bellwether XTREEs with other threshold based learners.
"""

from __future__ import print_function, division

import os
import sys
from pdb import set_trace

# Update path
root = os.path.join(os.getcwd().split('')[0], '/')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from data.GetData import get_all_projects
from Utils.FileUtil import list2dataframe
from commons.XTREE import xtree
from Utils.StatsUtils.CrossVal import TrainTestValidate
from commons.FeatureSelection import rfe_select

import warnings
warnings.filterwarnings("ignore")


def planning():
    data = get_all_projects(features="all")
    results = dict()
    for proj, paths in data.iteritems():
        results.update({proj: []})
        for train, test, validation in TrainTestValidate.split(paths.data):

            "Find overlaping columns"
            train = list2dataframe(train)
            test = list2dataframe(test)
            validation =list2dataframe(validation)
            columns = set(train.columns)
            for s in [test.columns, validation.columns]:
                columns.intersection_update(s)

            columns = list(columns)

            for i, f in enumerate(columns):
                if f == 'Name':
                    columns.insert(0, columns.pop(i))
                if f == 'category':
                    columns.append(columns.pop(i))

            train = train[columns]
            test = train[columns]
            validation = train[columns]

            "Convert to pandas type dataframe"
            train = rfe_select(train)
            test = test[train.columns]
            validation = validation[train.columns]

            "Recommend changes with XTREE"
            new = xtree(train[train.columns[1:]], test)

            """
                " Have the changes been implemented? 
            """

            "Create a smaller dframe of all closed issues in validation set"
            closed_in_validation = validation[validation['category'].isin([0])]

            "Group the smaller dframe and the patched dframe by their file names"
            modules = list(set(closed_in_validation["Name"].tolist()))

            heeded = []
            for module_name in modules:
                count = []
                module_name_new = new[new["Name"].isin([module_name])]
                module_name_act = train[train["Name"].isin([module_name])]
                module_name_val = closed_in_validation[closed_in_validation["Name"].isin([module_name])]
                for col_name in module_name_val.columns[1:-1]:
                    aa = module_name_new[col_name]
                    bb = module_name_val[col_name]
                    try:
                        ranges = sorted(eval(aa.values.tolist()[0]))
                        count.append(any([abs(ranges[0]) <= bbb <= abs(ranges[1]) for bbb in bb.tolist()]))
                    except TypeError:
                        count.append(any([bbb == aa.values[0] for bbb in bb.tolist()]))
                    except IndexError:
                        pass
                if len(count) > 0:
                    heeded.append(sum(count)/len(count))
        results[proj]= heeded
        percentiles = np.percentile(results[proj], [25, 50, 75])
        print("{}\t{:0.2f}\t{:0.2f}\t{:0.2f}".format(proj[:5], percentiles[0], percentiles[1], percentiles[2]))
        "Find the deltas between patched and smaller validation dframe"

if __name__ == "__main__":
    planning()
