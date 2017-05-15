import os

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.externals import joblib


if __name__ == "__main__":
    # Load Iris Data
    iris_data = load_iris()
    features = iris_data.data
    feature_names = iris_data.feature_names
    target = iris_data.target
    target_names = iris_data.target_names

    knn = KNeighborsClassifier(n_neighbors=3)  # replace with your own ML model here
    knn.fit(features, target)

    _CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    _SERIALIZATION_DIR = os.path.join(_CUR_DIR, "models")
    if not os.path.exists(_SERIALIZATION_DIR):
        os.makedirs(_SERIALIZATION_DIR)

    joblib.dump(knn, os.path.join(_SERIALIZATION_DIR, 'iris_model.pkl'))
