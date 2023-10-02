import numpy as np
import pickle

input_file = "input.npy"
output_file = "output.pickle"

data = np.load(input_file)
with open(output_file, 'wb') as f:
    pickle.dump(data, f)

print(f"Converted {input_file} to {output_file}")