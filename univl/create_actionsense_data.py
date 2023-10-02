import numpy as np
import pickle

def make_data(feature_chunks, num_chunks):
    """
    feature_chunks: number of features per start/end interval
    num_chunks: number of feature chunks total
    # each feature is 3.2s of video with my settings (32 frames, 10fps)
    total # frames is 32*feature_chunks*num_chunks, assuming 32 frames per feature
    """

    PLACEHOLDER_WORD = "cut"

    return {
        'start': np.array([feature_chunks*i for i in range(num_chunks)]),
        'end': np.array([feature_chunks*i for i in range(1,num_chunks+1)]),
        'text': np.array([PLACEHOLDER_WORD for _ in range(num_chunks)], dtype=object),
        'transcript': np.array(['none' for _ in range(num_chunks)], dtype=object)
    }

data = {
    "S03_split2": make_data(10, 10)
}

with open('data/actionsense/actionsense_data.pickle', 'wb') as file:
    pickle.dump(data, file)