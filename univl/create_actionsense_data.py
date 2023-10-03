import numpy as np
import pickle
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument('--feature_chunks', required=True, type=int)
parser.add_argument('--num_chunks', required=True, type=int)
args = parser.parse_args()

data = {}
for video_name in [
    "output_segment_000",
    "output_segment_001",
    "output_segment_002",
    "output_segment_003",
    "output_segment_004",
    "output_segment_005",
    "output_segment_006",
    "output_segment_007",
    "output_segment_008",
    "output_segment_009",
    "output_segment_010",
    "output_segment_011",]:
        data[video_name] = make_data(args.feature_chunks, args.num_chunks)

with open('data/actionsense/actionsense_data.pickle', 'wb') as file:
    pickle.dump(data, file)