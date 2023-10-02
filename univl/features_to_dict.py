import numpy as np
import pickle

input_file = "data/actionsense/actionsense_features_array.pickle"
output_file = "data/actionsense/actionsense_features.pickle"

data = np.load(input_file)
new_data = {"S03_split2": data}
with open(output_file, 'wb') as f:
    pickle.dump(new_data, f)