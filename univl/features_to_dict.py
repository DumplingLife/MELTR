import numpy as np
import pickle

input_file = "data/actionsense/actionsense_features_array.pickle"
output_file = "data/actionsense/actionsense_features.pickle"

with open(input_file, "rb") as file:
    features = pickle.load(file)
new_data = {"S03_split2": features}
with open(output_file, 'wb') as f:
    pickle.dump(new_data, f)