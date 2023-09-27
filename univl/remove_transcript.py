import pickle

# Load the pickle file
with open('data/youcookii/youcookii_data.no_transcript.pickle', 'rb') as f:
    data = pickle.load(f)

# Modify the 'transcript' entries
for key, value in data.items():
    if 'transcript' in value:
        if all(item == 'none' for item in value['transcript']):
            value['transcript'] = []

# Save the modified data back to the pickle file
with open('data/youcookii/new_youcookii_data.no_transcript.pickle', 'wb') as f:
    pickle.dump(data, f)

print("Modification complete.")