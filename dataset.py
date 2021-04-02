import numpy as np
import pandas as pd

def make_dataset(n_cands, n_spots, n_voters, name="out.csv", seed=90210):
    np.random.seed(seed)

    np_data = [np.random.choice(np.arange(n_cands), n_spots, replace=False)]
    for i in range(n_voters-1):
        np_data = np.append(np_data, [np.random.choice(np.arange(n_cands), n_spots, replace=False)], axis=0)

    names = np.zeros((n_voters,), dtype='object')
    for i in range(len(names)):
        names[i] = 'phil'
    names = np.array([names]).T

    info = np.concatenate((names, np_data), axis=1)
    data = pd.DataFrame(data=info)
    data.to_csv(name, index=False)