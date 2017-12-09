"""
Compare Bellwether XTREEs with other threshold based learners.
"""

from __future__ import print_function, division

import os
import sys
from pdb import set_trace

# Update path
root = os.path.join(os.getcwd().split('project')[0], 'project')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from data.GetData import get_all_projects
from Utils.FileUtil import list2dataframe
from commons.XTREE import xtree
from Utils.StatsUtils.CrossVal import TrainTestValidate

import warnings
warnings.filterwarnings("ignore")


def planning():
    data = get_all_projects()
    results = dict()
    for proj, paths in data.iteritems():
        results.update({proj: []})
        heeded = []
        for train, test, validation in TrainTestValidate.split(paths.data):
            "Convert to pandas type dataframe"
            train = list2dataframe(train).dropna(axis=0).reset_index(drop=True)
            test = list2dataframe(test).dropna(axis=0).reset_index(drop=True)
            validation = list2dataframe(validation).dropna(
                axis=0).reset_index(drop=True)


            "Recommend changes with XTREE"
            new = xtree(train[train.columns[1:]], test)


            """
            Have the changes been implemented?"
            """

            "Create a smaller dframe of all non-defective modules in validation set"
            closed_in_validation = validation[validation['bugs'].isin([0])]

            "Group the smaller dframe and the patched dframe by their file names"
            modules = list(set(closed_in_validation["name"].tolist()))
            
            for module_name in modules:
                count = []
                module_name_new = new[new["name"].isin([module_name])]
                module_name_act = train[train["name"].isin([module_name])]
                module_name_val = closed_in_validation[closed_in_validation["name"].isin([module_name])]
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
        try:
            percentiles = np.percentile(results[proj], [25, 50, 75])
            print("{}\t{:0.2f}\t{:0.2f}\t{:0.2f}".format(proj[:5], percentiles[0], percentiles[1], percentiles[2]))
            "Find the deltas between patched and smaller validation dframe"
        except:
            pass
def get_data_details():
    import pandas as pd
    data = get_all_projects()
    for proj, p_path in data.iteritems():
        ver = len(p_path.data)
        samples = []
        defective = []
        for d in p_path.data:
            data = pd.read_csv(d).dropna(axis=0).reset_index(drop=True)
            samples.append(len(data))
            defective.append(int(sum([0 if dd == 0 else 1 for dd in data["bugs"]])))
        print("{},{},{},{}".format(proj, int(ver/3), int(sum(
            samples)/3), int(sum(defective) *100 / sum(samples))))

    set_trace()
    
if __name__ == "__main__":
    # planning()
    get_data_details()

