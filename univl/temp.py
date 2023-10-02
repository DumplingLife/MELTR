import pickle

with open("data/actionsense/actionsense_features.pickle", 'rb') as file:
    print(pickle.load(file))